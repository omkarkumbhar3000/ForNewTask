#!/usr/bin/env python3
"""optimize_media.py - make the lesson media lighter without changing a single path (FUN-E29, FUN-E32).

Runs after tools/extract_content.py, on the media library it produced:
  * pictures over 100 KB are resized to at most twice their display size (a lesson card shows a picture at
    160 px, so 320 px; a video poster spans the lesson, so 1280 px) and re-encoded in their own format;
    a result is kept only when it is at least 20% smaller, so a picture is never made worse for nothing
  * MP4/M4A files whose index sits after the data are remuxed with the index first ("faststart"): the same
    audio and video streams, copied bit for bit, so playback can start before the whole file has arrived
  * media/OPTIMISED.csv records every file changed: path,operation,source_bytes,source_sha256,bytes,sha256

File names and formats never change, so the course JSON, the database rows and the pages stay valid.
Re-running is safe: a file whose bytes match its recorded result is skipped; an original restored by
extract_content.py (which accepts the recorded results as already placed) is optimised again.

Needs Pillow and ffmpeg/ffprobe; tools/mediatool.Dockerfile provides both. From "Updated Project":
  docker build -f tools/mediatool.Dockerfile -t cc-mediatool .
  docker run --rm -v "${PWD}:/work" -w /work cc-mediatool python tools/optimize_media.py [--dry-run]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent            # "Updated Project"
MEDIA = ROOT / "media"
CONTENT = ROOT / "app" / "src" / "main" / "resources" / "content"
MANIFEST = MEDIA / "OPTIMISED.csv"
FIELDS = ["path", "operation", "source_bytes", "source_sha256", "bytes", "sha256"]

MAX_SIDE = {"card": 320, "poster": 1280}                 # twice the display size (css/app.css .card .pic)
MIN_BYTES = 100 * 1024                                    # smaller pictures are left alone
MIN_SAVING = 0.20                                         # keep a re-encoded picture only if 20% smaller
DURATION_TOLERANCE = 0.1                                  # seconds; a remux must not change the length


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def picture_roles() -> dict[str, str]:
    """media path -> 'card' or 'poster', from the course JSON (a picture beside a video is its poster)."""
    roles: dict[str, str] = {}
    for f in sorted(CONTENT.glob("*.json")):
        course = json.loads(f.read_text(encoding="utf-8"))
        for lesson in course.get("lessons", []):
            for item in lesson.get("items", []):
                if item.get("image"):
                    roles[item["image"]] = "poster" if item.get("video") else "card"
    return roles


def encode(im: Image.Image, fmt: str) -> bytes:
    buf = io.BytesIO()
    if fmt == "JPEG":
        im.convert("RGB").save(buf, "JPEG", quality=82, optimize=True, progressive=True)
    elif fmt == "PNG":
        im.save(buf, "PNG", optimize=True)
    elif fmt == "WEBP":
        im.save(buf, "WEBP", quality=80, method=6)
    elif fmt == "AVIF":
        im.save(buf, "AVIF", quality=60, speed=6)
    else:
        raise ValueError(f"unsupported picture format {fmt}")
    return buf.getvalue()


def smaller_picture(path: Path, role: str) -> tuple[bytes, str] | None:
    """The re-encoded picture and a description, or None when it would not be worth it."""
    original = path.stat().st_size
    with Image.open(path) as src:
        fmt = src.format
        im = ImageOps.exif_transpose(src)                 # keep the picture upright once EXIF is dropped
        w, h = im.size
        limit = MAX_SIDE[role]
        if max(w, h) > limit:
            im = im.copy()
            im.thumbnail((limit, limit), Image.Resampling.LANCZOS)
        data = encode(im, fmt)
        size = im.size
    if len(data) > original * (1 - MIN_SAVING):
        return None
    with Image.open(io.BytesIO(data)) as check:            # the result must decode, at the expected size
        check.load()
        if check.size != size or check.format != fmt:
            raise RuntimeError(f"{path}: re-encoded picture does not read back as {fmt} {size}")
    return data, f"picture {w}x{h} -> {size[0]}x{size[1]} {fmt.lower()}"


def top_level_boxes(path: Path) -> list[str]:
    boxes = []
    with path.open("rb") as f:
        while True:
            head = f.read(8)
            if len(head) < 8:
                break
            size, kind = struct.unpack(">I4s", head)
            header = 8
            if size == 1:
                size = struct.unpack(">Q", f.read(8))[0]
                header = 16
            boxes.append(kind.decode("latin-1"))
            if size == 0:
                break
            f.seek(size - header, 1)
    return boxes


def index_after_data(path: Path) -> bool:
    boxes = top_level_boxes(path)
    return "moov" in boxes and "mdat" in boxes and boxes.index("mdat") < boxes.index("moov")


def probe(path: Path) -> tuple[float, list[str]]:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name",
                          "-of", "json", str(path)], check=True, capture_output=True, text=True).stdout
    info = json.loads(out)
    return float(info["format"]["duration"]), [s.get("codec_name", "?") for s in info["streams"]]


def faststart(path: Path, tmp: Path) -> str:
    """Remux with the index first into tmp; the streams are copied, never re-encoded."""
    base = ["ffmpeg", "-v", "error", "-y", "-i", str(path)]
    tail = ["-c", "copy", "-map_metadata", "0", "-movflags", "+faststart", str(tmp)]
    if subprocess.run(base + ["-map", "0"] + tail, capture_output=True).returncode != 0:
        # a data track ffmpeg cannot write back (a timecode, say) is dropped; audio and video are kept
        subprocess.run(base + ["-map", "0:v?", "-map", "0:a?"] + tail, check=True, capture_output=True)
    before, after = probe(path), probe(tmp)
    if abs(before[0] - after[0]) > DURATION_TOLERANCE or before[1] != after[1]:
        raise RuntimeError(f"{path}: remux changed the media ({before} -> {after})")
    if index_after_data(tmp):
        raise RuntimeError(f"{path}: remux did not move the index first")
    return f"faststart {'+'.join(after[1])} {after[0]:.1f}s"


def read_manifest() -> dict[str, dict[str, str]]:
    if not MANIFEST.exists():
        return {}
    with MANIFEST.open(encoding="utf-8", newline="") as f:
        return {row["path"]: row for row in csv.DictReader(f)}


def write_manifest(rows: dict[str, dict[str, str]]) -> None:
    buf = io.StringIO()
    w = csv.DictWriter(buf, FIELDS, lineterminator="\n")
    w.writeheader()
    for path in sorted(rows):
        w.writerow(rows[path])
    data = buf.getvalue().encode("utf-8")
    if not MANIFEST.exists() or MANIFEST.read_bytes() != data:
        MANIFEST.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="report what would change; write nothing")
    args = parser.parse_args()

    manifest = read_manifest()
    roles = picture_roles()
    work = [(p, "picture") for p in sorted(roles)]
    work += [(f.relative_to(MEDIA).as_posix(), "faststart")
             for f in sorted(MEDIA.rglob("*")) if f.suffix.lower() in (".mp4", ".m4a")]

    changed = skipped = done = 0
    saved = 0
    for rel, kind in work:
        path = MEDIA / rel
        if not path.is_file():
            continue
        digest = sha256_file(path)
        record = manifest.get(rel)
        if record and record["sha256"] == digest:
            done += 1                                   # already optimised on an earlier run
            continue
        source_bytes = path.stat().st_size
        if kind == "picture":
            if roles[rel] not in MAX_SIDE or source_bytes <= MIN_BYTES:
                continue
            result = smaller_picture(path, roles[rel])
            if result is None:
                skipped += 1
                print(f"  kept     {rel} (re-encoding would save under {MIN_SAVING:.0%})")
                continue
            data, what = result
            if args.dry_run:
                print(f"  would    {rel}: {what}, {source_bytes // 1024} KB -> {len(data) // 1024} KB")
                changed += 1
                saved += source_bytes - len(data)
                continue
            tmp = path.with_name(path.name + ".part")
            tmp.write_bytes(data)
        else:
            if not index_after_data(path):
                continue
            if args.dry_run:
                print(f"  would    {rel}: faststart")
                changed += 1
                continue
            tmp = path.with_name(path.stem + ".part" + path.suffix)
            try:
                what = faststart(path, tmp)
            except Exception:
                tmp.unlink(missing_ok=True)
                raise
        new_digest = sha256_file(tmp)
        new_bytes = tmp.stat().st_size
        os.replace(tmp, path)
        if sha256_file(path) != new_digest:
            raise RuntimeError(f"{path}: bytes changed after placing the result")
        # the source is the file as it was before this run: what extract_content.py placed
        manifest[rel] = {"path": rel, "operation": what, "source_bytes": str(source_bytes),
                         "source_sha256": digest, "bytes": str(new_bytes), "sha256": new_digest}
        changed += 1
        saved += source_bytes - new_bytes
        print(f"  changed  {rel}: {what}, {source_bytes // 1024} KB -> {new_bytes // 1024} KB")

    if not args.dry_run:
        write_manifest(manifest)
    verb = "would change" if args.dry_run else "changed"
    print(f"{verb} {changed} files ({saved / 1024 / 1024:.2f} MB smaller); {done} already optimised; "
          f"{skipped} pictures kept as they are")
    return 0


if __name__ == "__main__":
    sys.exit(main())
