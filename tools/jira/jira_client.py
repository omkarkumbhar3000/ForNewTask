#!/usr/bin/env python3
"""Minimal Jira Cloud REST client - shared by the discovery and create scripts.

Auth is HTTP Basic: JIRA_EMAIL as username, JIRA_API_TOKEN as password. Credentials
come from tools/jira/.env, which is gitignored. Nothing here prints or persists the token.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV_FILE = HERE / ".env"
SSL_CTX = ssl.create_default_context()


def load_env() -> dict:
    if not ENV_FILE.exists():
        raise SystemExit(f"missing {ENV_FILE} - copy .env.sample and fill it in")
    cfg = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()
    missing = [k for k in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN",
                           "JIRA_PROJECT_KEY") if not cfg.get(k)]
    if missing:
        raise SystemExit(f"missing keys in .env: {', '.join(missing)}")
    cfg["JIRA_BASE_URL"] = cfg["JIRA_BASE_URL"].rstrip("/")
    return cfg


class Jira:
    def __init__(self, cfg: dict):
        self.base = cfg["JIRA_BASE_URL"]
        self.project = cfg["JIRA_PROJECT_KEY"]
        raw = f"{cfg['JIRA_EMAIL']}:{cfg['JIRA_API_TOKEN']}".encode()
        self._auth = "Basic " + base64.b64encode(raw).decode()

    # ------------------------------------------------------------------ transport
    def _request(self, method: str, path: str, *, body=None, headers=None,
                 raw_body: bytes | None = None) -> tuple[int, object]:
        url = path if path.startswith("http") else f"{self.base}{path}"
        h = {"Authorization": self._auth, "Accept": "application/json"}
        data = raw_body
        if body is not None:
            data = json.dumps(body).encode()
            h["Content-Type"] = "application/json"
        if headers:
            h.update(headers)
        req = urllib.request.Request(url, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=120, context=SSL_CTX) as r:
                text = r.read().decode("utf-8", "replace")
                status = r.status
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")
            status = e.code
        try:
            return status, json.loads(text) if text else None
        except json.JSONDecodeError:
            return status, text

    def get(self, path):
        return self._request("GET", path)

    def post(self, path, body):
        return self._request("POST", path, body=body)

    def put(self, path, body):
        return self._request("PUT", path, body=body)

    # -------------------------------------------------------------------- helpers
    def myself(self):
        return self.get("/rest/api/3/myself")

    def project_info(self):
        return self.get(f"/rest/api/3/project/{self.project}")

    def createmeta_types(self):
        return self.get(f"/rest/api/3/issue/createmeta/{self.project}/issuetypes")

    def createmeta_fields(self, issue_type_id):
        return self.get(
            f"/rest/api/3/issue/createmeta/{self.project}/issuetypes/{issue_type_id}")

    def fields(self):
        return self.get("/rest/api/3/field")

    def attach(self, issue_key: str, file_path: Path) -> tuple[int, object]:
        """multipart/form-data upload. Jira requires the X-Atlassian-Token header."""
        boundary = f"----jira{uuid.uuid4().hex}"
        ctype = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        pre = (f"--{boundary}\r\n"
               f'Content-Disposition: form-data; name="file"; '
               f'filename="{file_path.name}"\r\n'
               f"Content-Type: {ctype}\r\n\r\n").encode()
        post = f"\r\n--{boundary}--\r\n".encode()
        payload = pre + file_path.read_bytes() + post
        return self._request(
            "POST", f"/rest/api/3/issue/{issue_key}/attachments",
            raw_body=payload,
            headers={"X-Atlassian-Token": "no-check",
                     "Content-Type": f"multipart/form-data; boundary={boundary}"})
