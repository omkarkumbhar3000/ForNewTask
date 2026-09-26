#!/usr/bin/env python3.11
"""extract_content.py - migrate the CleverCubs baseline content into course JSON and a media library.

Reads the old site (read-only), writes:
  * one JSON file per course            -> app/src/main/resources/content/<slug>.json
  * the referenced media, renamed       -> media/<slug>/<normalised-name>, media/brand/logo.png
  * media/MEDIA-MAP.csv                 -> course,new_path,original_name,bytes,sha256
  * tools/extraction-report.md          -> counts, fixes, missing and excluded files, disk space

Guarantees: the baseline is only ever opened for reading; the output is deterministic (same input, same
bytes); every copied file is verified by sha256 against its source; only the tool's own outputs are written.

Stdlib only. Run with:  python3.11 tools/extract_content.py [--dry-run]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path

TOOL = "tools/extract_content.py"
GIB = 1024 ** 3
MIB = 1024 ** 2
MIN_FREE_AFTER = int(1.5 * GIB)          # abort if less than 1.5 GiB would remain on the media drive
PASS_MARK = 70                           # D62 / DD-18: the lesson-linked quiz family's 70% pass mark
MAX_LESSON_ITEMS = 5                     # D60: lessons of about five items
EN_DASH = "\u2013"


class ExtractionError(Exception):
    """A loud, fatal problem: the tool stops before writing anything further."""


def fail(msg: str) -> None:
    raise ExtractionError(msg)


# ----------------------------------------------------------------------------------------------------
# Course definitions (the only hand-written mapping; everything else is read from the baseline)
# ----------------------------------------------------------------------------------------------------
# field sources for a card:  h2 = <h2> text, p0/p1 = first/second <p>, alt = <img alt>
TOPIC_COURSES = [
    dict(slug="alphabets", title="Alphabets", page="alphabets_voice.html", quiz="alphabets_quize.html",
         reserve="alphabets_qq.html", hub="alphabets", label="h2", word="p0", emoji=None,
         subject={"letter", "letters", "alphabet"},
         describe=lambda it: f"Meet the {len(it)} letters from {it[0]['label']} to {it[-1]['label']}, "
                             f"each with a picture and a spoken word."),
    dict(slug="numbers", title="Numbers", page="number_voice.html", quiz="num_quiz.html",
         reserve=None, hub="numbers", label="h2", word="p0", emoji="p1",
         subject={"number", "numbers"},
         describe=lambda it: f"Count from {it[0]['label']} to {it[-1]['label']} with emoji pictures "
                             f"and spoken number names."),
    dict(slug="animals", title="Animals", page="animal_voice.html", quiz="animal_quize.html",
         reserve="animal_qq.html", hub="animals", label="word", word="h2", emoji=None,
         subject={"animal", "animals"},
         describe=lambda it: f"Meet {len(it)} animals and hear the sounds they make."),
    dict(slug="birds", title="Birds", page="birds_voice.html", quiz="birds_quize.html",
         reserve="birds_qq.html", hub="birds", label="word", word="h2", emoji=None,
         subject={"bird", "birds"},
         describe=lambda it: f"Meet {len(it)} birds and hear the sounds they make."),
    dict(slug="fruits", title="Fruits", page="frutis_voice.html", quiz="frutis_quize.html",
         reserve="fruits_qq.html", hub="fruits", label="word", word="h2", emoji=None,
         subject={"fruit", "fruits"},
         describe=lambda it: f"Watch videos of {len(it)} fruits."),
    dict(slug="vegetables", title="Vegetables", page="vegitables voice.html", quiz="vegitables_quize.html",
         reserve="vegitables_qq.html", hub="vegetables", label="word", word="alt", emoji=None,
         subject={"vegetable", "vegetables"},
         describe=lambda it: f"See {len(it)} vegetables in pictures and videos."),
    dict(slug="flowers", title="Flowers", page="flowers_voice.html", quiz="flowers_quize.html",
         reserve="flowers_qq.html", hub="flowers", label="word", word="p0", emoji=None,
         subject={"flower", "flowers"},
         describe=lambda it: f"See {len(it)} flowers and hear their names."),
    dict(slug="colours", title="Colours", page="color_voice.html", quiz="colors_quize.html",
         reserve="colors_qq.html", hub="colours", label="word", word="p0", emoji=None,
         subject={"color", "colors", "colour", "colours"},
         describe=lambda it: f"See {len(it)} colours and hear their names."),
    dict(slug="body-parts", title="Body Parts", page="body_parts_voice.html", quiz="body_part_quize.html",
         reserve="body_qq.html", hub="body", label="word", word="hotspot", emoji=None,
         subject={"body", "part", "parts"},
         describe=lambda it: f"Explore {len(it)} body parts on a picture and read what each one does."),
]
MEDIA_COURSES = [
    dict(slug="rhymes", title="Rhymes", page="poem_video2.html", js="poems", card_key="data-poem",
         describe=lambda it: f"Watch {len(it)} nursery rhymes and read along with the words."),
    dict(slug="stories", title="Stories", page="story.html", js="stories", card_key="data-story",
         describe=lambda it: f"Watch {len(it)} stories told in video."),
]
LEARNING_PAGE = "second_page.html"      # course order and cover images
QUIZ_HUB_PAGE = "quize_page.html"       # subject icons
LOGO = "logo.png"
EXCLUDED_BY_NAME = {"CleverCubs.pptx": "the authors' slide deck, not site content"}

# Spelling corrections for displayed item words. Applied only where the intended word is unambiguous;
# the raw baseline text is always kept in `sourceWord`. Key: (course slug, raw text lower-cased).
WORD_FIXES = {
    ("fruits", "blackbarray"): ("Blackberry", "video file 'blackbarray video.mp4'"),
    ("fruits", "bluekbarray"): ("Blueberry", "onclick argument 'bluebarray'; fruits_qq.html:62 'Blueberry'"),
    ("fruits", "cocunet"): ("Coconut", "fruits_qq.html:61,64 'Coconut'"),
    ("fruits", "cheress"): ("Cherries", "fruits_qq.html:57 'Cherry'"),
    ("fruits", "custed apple"): ("Custard Apple", "video file 'custed apple video.mp4'"),
    ("fruits", "dragenfrutis"): ("Dragon Fruit", "video file 'dragenfruti video.mp4'"),
    ("fruits", "honydew"): ("Honeydew", "video file 'honydew video.mp4'"),
    ("fruits", "jackfruti"): ("Jackfruit", "video file 'jackfurtis.mp4'"),
    ("fruits", "loqute"): ("Loquat", "video file 'loqute.mp4'"),
    ("fruits", "paer"): ("Pear", "fruits_qq.html:58,64 'Pear'"),
    ("fruits", "pech"): ("Peach", "fruits_qq.html:60 'Peach'"),
    ("fruits", "pinapal"): ("Pineapple", "fruits_qq.html:60 'Pineapple'"),
    ("fruits", "stobary"): ("Strawberry", "frutis_quize.html:165, fruits_qq.html:62 'Strawberry'"),
    ("fruits", "tengaris"): ("Tangerine", "video file 'tengaris video.mp4'"),
    ("fruits", "watermelan"): ("Watermelon", "frutis_quize.html:160, fruits_qq.html:60-61 'Watermelon'"),
    ("flowers", "hibiseus"): ("Hibiscus", "audio file 'Hibiscus sound.mp4'"),
    ("flowers", "rosmary"): ("Rosemary", "audio file 'Rosemerry sound.mp4'"),
    ("flowers", "blue bell"): ("Bluebell", "image file 'Bluebell photo.jpg'; flowers_qq.html:63 'Bluebell'"),
}
# Raw words that look misspelt but whose intended word is not certain: kept (capitalised), flagged.
UNRESOLVED_WORDS = {
    ("fruits", "rosebary"): "possibly 'Raspberry'; confirm by watching rosebary.mp4",
}
TITLE_TYPOS = [(re.compile(r"\btort toise\b", re.I), "tortoise")]
TITLE_SMALL_WORDS = {"a", "an", "and", "the", "of", "on", "in", "to", "for", "at", "by", "or"}

STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "was", "of", "on", "in", "to", "and", "or", "do", "does", "did",
    "we", "you", "your", "us", "our", "it", "its", "what", "which", "how", "who", "when", "where", "can",
    "has", "have", "had", "be", "called", "known", "as", "with", "for", "at", "by", "very", "this", "that",
    "there", "use", "used", "using", "help", "helps", "many", "much", "always", "often", "most",
}

MEDIA_EXT = {"png", "jpg", "jpeg", "webp", "avif", "gif", "svg", "mp4", "m4a", "mp3", "wav", "ogg", "webm"}


# ----------------------------------------------------------------------------------------------------
# Baseline access (read-only)
# ----------------------------------------------------------------------------------------------------
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(MIB), b""):
            h.update(chunk)
    return h.hexdigest()


class Baseline:
    def __init__(self, root: Path):
        if not root.is_dir():
            fail(f"baseline folder not found: {root}")
        self.root = root
        self.names = sorted(p.name for p in root.iterdir() if p.is_file())
        self.name_set = set(self.names)
        self.lower_map: dict[str, list[str]] = {}
        for n in self.names:
            self.lower_map.setdefault(n.lower(), []).append(n)
        self._text: dict[str, str] = {}

    def text(self, name: str) -> str:
        if name not in self._text:
            if name not in self.name_set:
                fail(f"baseline page missing: {name}")
            raw = (self.root / name).read_bytes()
            try:
                self._text[name] = raw.decode("utf-8-sig")
            except UnicodeDecodeError as exc:
                fail(f"{name}: not valid UTF-8 ({exc})")
        return self._text[name]

    def path(self, name: str) -> Path:
        return self.root / name

    def head(self, name: str, n: int = 32) -> bytes:
        with open(self.root / name, "rb") as fh:
            return fh.read(n)


# ----------------------------------------------------------------------------------------------------
# Minimal HTML tree (html.parser) with source line numbers
# ----------------------------------------------------------------------------------------------------
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source",
             "track", "wbr"}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "line")

    def __init__(self, tag, attrs, parent, line):
        self.tag, self.attrs, self.children, self.parent, self.line = tag, attrs, [], parent, line

    def has_class(self, cls: str) -> bool:
        return cls in (self.attrs.get("class") or "").split()

    def iter(self):
        for c in self.children:
            if isinstance(c, Node):
                yield c
                yield from c.iter()

    def find_all(self, pred):
        return [n for n in self.iter() if pred(n)]

    def text(self) -> str:
        parts = []
        for c in self.children:
            parts.append(c if isinstance(c, str) else c.text())
        return "".join(parts)

    def clean_text(self) -> str:
        return " ".join(self.text().split())


class _TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None, 0)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs), self.cur, self.getpos()[0])
        self.cur.children.append(node)
        if tag not in VOID_TAGS:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, dict(attrs), self.cur, self.getpos()[0]))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        if self.cur.tag not in ("script", "style"):
            self.cur.children.append(data)


def parse_html(text: str) -> Node:
    b = _TreeBuilder()
    b.feed(text)
    b.close()
    return b.root


# ----------------------------------------------------------------------------------------------------
# Tiny JavaScript literal reader (objects, arrays, strings, numbers) with line numbers
# ----------------------------------------------------------------------------------------------------
class JsStr(str):
    line: int


class JsObj(dict):
    line: int


class JsArr(list):
    line: int


class Negated:
    """`!"text"` inside an array literal: JavaScript evaluates it to false (the FUN-E07 bug)."""

    def __init__(self, value: "JsStr", line: int):
        self.value, self.line = value, line


_JS_ESC = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}


class JsReader:
    def __init__(self, text: str, pos: int, page: str):
        self.t, self.i, self.page = text, pos, page

    def line_at(self, i: int) -> int:
        return self.t.count("\n", 0, i) + 1

    def where(self, i=None) -> str:
        return f"{self.page}:{self.line_at(self.i if i is None else i)}"

    def skip(self):
        t = self.t
        while self.i < len(t):
            c = t[self.i]
            if c.isspace():
                self.i += 1
            elif t.startswith("//", self.i):
                j = t.find("\n", self.i)
                self.i = len(t) if j < 0 else j
            elif t.startswith("/*", self.i):
                j = t.find("*/", self.i + 2)
                if j < 0:
                    fail(f"{self.where()}: unterminated comment")
                self.i = j + 2
            else:
                break

    def value(self):
        self.skip()
        if self.i >= len(self.t):
            fail(f"{self.where()}: unexpected end of script")
        c = self.t[self.i]
        if c == "{":
            return self.obj()
        if c == "[":
            return self.arr()
        if c in "\"'`":
            return self.string()
        if c == "!":
            start = self.i
            self.i += 1
            inner = self.value()
            if not isinstance(inner, JsStr):
                fail(f"{self.where(start)}: unsupported '!' expression")
            return Negated(inner, self.line_at(start))
        m = re.compile(r"-?\d+(?:\.\d+)?").match(self.t, self.i)
        if m:
            self.i = m.end()
            return float(m.group()) if "." in m.group() else int(m.group())
        m = re.compile(r"[A-Za-z_$][\w$]*").match(self.t, self.i)
        if m and m.group() in ("true", "false", "null"):
            self.i = m.end()
            return {"true": True, "false": False, "null": None}[m.group()]
        fail(f"{self.where()}: unexpected {c!r} in a JavaScript literal")

    def string(self) -> JsStr:
        q = self.t[self.i]
        start = self.i
        self.i += 1
        out = []
        while True:
            if self.i >= len(self.t):
                fail(f"{self.where(start)}: unterminated string")
            c = self.t[self.i]
            if c == q:
                self.i += 1
                break
            if c == "\n" and q != "`":
                fail(f"{self.where(start)}: newline inside a string")
            if c == "\\":
                nxt = self.t[self.i + 1]
                if nxt == "u":
                    out.append(chr(int(self.t[self.i + 2:self.i + 6], 16)))
                    self.i += 6
                    continue
                if nxt == "x":
                    out.append(chr(int(self.t[self.i + 2:self.i + 4], 16)))
                    self.i += 4
                    continue
                out.append(_JS_ESC.get(nxt, nxt))
                self.i += 2
                continue
            if q == "`" and c == "$" and self.t.startswith("${", self.i):
                fail(f"{self.where(start)}: template interpolation is not supported")
            out.append(c)
            self.i += 1
        s = JsStr("".join(out))
        s.line = self.line_at(start)
        return s

    def key(self) -> str:
        self.skip()
        c = self.t[self.i]
        if c in "\"'":
            return str(self.string())
        m = re.compile(r"[A-Za-z_$][\w$]*").match(self.t, self.i)
        if not m:
            fail(f"{self.where()}: expected an object key")
        self.i = m.end()
        return m.group()

    def obj(self) -> JsObj:
        o = JsObj()
        o.line = self.line_at(self.i)
        self.i += 1
        while True:
            self.skip()
            if self.t[self.i] == "}":
                self.i += 1
                return o
            k = self.key()
            self.skip()
            if self.t[self.i] != ":":
                fail(f"{self.where()}: expected ':' after key {k!r}")
            self.i += 1
            if k in o:
                fail(f"{self.where()}: duplicate key {k!r}")
            o[k] = self.value()
            self.skip()
            c = self.t[self.i]
            if c == ",":
                self.i += 1
            elif c != "}":
                fail(f"{self.where()}: expected ',' or '}}' in an object")

    def arr(self) -> JsArr:
        a = JsArr()
        a.line = self.line_at(self.i)
        self.i += 1
        while True:
            self.skip()
            if self.t[self.i] == "]":
                self.i += 1
                return a
            a.append(self.value())
            self.skip()
            c = self.t[self.i]
            if c == ",":
                self.i += 1
            elif c != "]":
                fail(f"{self.where()}: expected ',' or ']' in an array")


def read_js_literal(bl: Baseline, page: str, var: str):
    text = bl.text(page)
    m = re.search(r"\b(?:const|let|var)\s+" + re.escape(var) + r"\s*=\s*", text)
    if not m:
        fail(f"{page}: JavaScript variable '{var}' not found")
    return JsReader(text, m.end(), page).value()


# ----------------------------------------------------------------------------------------------------
# Text helpers
# ----------------------------------------------------------------------------------------------------
def collapse(s: str) -> str:
    return " ".join(s.split())


def capitalise_words(s: str) -> str:
    return " ".join(w[:1].upper() + w[1:] for w in collapse(s).split(" "))


def title_case(s: str) -> str:
    words = collapse(s).split(" ")
    out = []
    for i, w in enumerate(words):
        if i > 0 and w.lower() in TITLE_SMALL_WORDS:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def split_leading_emoji(s: str):
    s = collapse(s)
    head, sep, rest = s.partition(" ")
    if sep and head and not any(ch.isalnum() for ch in head):
        return head, rest
    return None, s


# ----------------------------------------------------------------------------------------------------
# Media planning
# ----------------------------------------------------------------------------------------------------
def sniff(head: bytes) -> str:
    if head[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    if head[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if head[4:8] == b"ftyp":
        brand = head[8:12]
        return "avif" if brand in (b"avif", b"avis") else "mp4"
    return "unknown"


EXPECTED_KIND = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp", "gif": "gif", "avif": "avif",
                 "mp4": "mp4", "m4a": "mp4"}


def split_ext(name: str):
    stem, dot, ext = name.rpartition(".")
    if dot and re.fullmatch(r"[A-Za-z0-9]{2,5}", ext) and stem:
        return stem, ext.lower()
    return name, None


def normalise_stem(stem: str) -> str:
    s = stem.lower()
    s = re.sub(r"[ _]+", "-", s)
    s = re.sub(r"[^a-z0-9.-]", "", s)
    s = re.sub(r"-{2,}", "-", s)
    s = s.strip("-.")
    if not s:
        fail(f"cannot normalise file name stem {stem!r}")
    return s


class MediaPlan:
    def __init__(self, bl: Baseline):
        self.bl = bl
        self.by_folder: dict[str, dict[str, str]] = {}     # folder -> {source name: new name}
        self.order: list[tuple[str, str]] = []              # (folder, source name) in first-use order
        self.ext_added: list[tuple[str, str, str]] = []     # (folder, source, sniffed kind)
        self.type_mismatch: list[tuple[str, str, str]] = []

    def add(self, folder: str, source: str) -> str:
        names = self.by_folder.setdefault(folder, {})
        if source in names:
            return f"{folder}/{names[source]}"
        stem, ext = split_ext(source)
        kind = sniff(self.bl.head(source))
        if ext is None:
            if kind != "mp4":
                fail(f"{source}: no extension and not recognisable as MP4 (sniffed {kind})")
            ext = "mp4"
            self.ext_added.append((folder, source, kind))
        elif EXPECTED_KIND.get(ext) and EXPECTED_KIND[ext] != kind:
            self.type_mismatch.append((folder, source, kind))
        base = normalise_stem(stem)
        new = f"{base}.{ext}"
        taken = set(names.values())
        n = 2
        while new in taken:
            new = f"{base}-{n}.{ext}"
            n += 1
        names[source] = new
        self.order.append((folder, source))
        return f"{folder}/{new}"


# ----------------------------------------------------------------------------------------------------
# Extraction
# ----------------------------------------------------------------------------------------------------
class Log:
    def __init__(self):
        self.fixes: list[dict] = []          # course, where, what, before, after, basis
        self.capitalised: list[dict] = []    # course, where, before, after
        self.missing: list[dict] = []        # course, where, file, effect
        self.dedup: list[dict] = []          # course, reserve, where, main, rule
        self.notes: list[str] = []
        self.warnings: list[str] = []


def resolve_media(bl: Baseline, log: Log, course: str, raw: str | None, where: str, role: str):
    """Return the exact baseline file name for a reference, or None (logged as missing)."""
    if raw is None or raw.strip() == "":
        return None
    ref = raw.strip()
    if re.match(r"^[A-Za-z]:[\\/]", ref) or "\\" in ref or "/" in ref:
        base = re.split(r"[\\/]", ref)[-1]
        if base in bl.name_set:
            log.fixes.append(dict(course=course, where=where, what=f"{role}: absolute/foreign path",
                                  before=ref, after=base,
                                  basis="the file exists in the baseline folder under its own name"))
            return base
        log.missing.append(dict(course=course, where=where, file=ref, effect=f"{role} set to null"))
        return None
    if ref in bl.name_set:
        return ref
    cands = bl.lower_map.get(ref.lower(), [])
    if len(cands) == 1:
        log.fixes.append(dict(course=course, where=where, what=f"{role}: file-name case differs",
                              before=ref, after=cands[0], basis="only case-insensitive match in the baseline"))
        return cands[0]
    log.missing.append(dict(course=course, where=where, file=ref, effect=f"{role} set to null"))
    return None


def display_word(log: Log, course: str, raw: str, where: str) -> str:
    key = (course, collapse(raw).lower())
    if key in WORD_FIXES:
        fixed, basis = WORD_FIXES[key]
        log.fixes.append(dict(course=course, where=where, what="spelling of displayed word",
                              before=raw, after=fixed, basis=basis))
        return fixed
    word = capitalise_words(raw)
    if key in UNRESOLVED_WORDS:
        log.warnings.append(f"`{where}` {course}: word '{raw}' kept as '{word}' - Information Required: "
                            f"{UNRESOLVED_WORDS[key]}")
    if word != raw:
        log.capitalised.append(dict(course=course, where=where, before=raw, after=word))
    return word


def card_fields(card: Node):
    h2 = [n for n in card.iter() if n.tag == "h2"]
    ps = [n for n in card.iter() if n.tag == "p"]
    imgs = [n for n in card.iter() if n.tag == "img"]
    audios = [n for n in card.iter() if n.tag == "audio"]
    videos = [n for n in card.iter() if n.tag == "video"]
    video_src, video_line = None, None
    if videos:
        v = videos[0]
        if v.attrs.get("src"):
            video_src, video_line = v.attrs["src"], v.line
        else:
            srcs = [n for n in v.iter() if n.tag == "source" and n.attrs.get("src")]
            if srcs:
                video_src, video_line = srcs[0].attrs["src"], srcs[0].line
    return dict(
        h2=(h2[0].clean_text(), h2[0].line) if h2 else None,
        p0=(ps[0].clean_text(), ps[0].line) if len(ps) > 0 else None,
        p1=(ps[1].clean_text(), ps[1].line) if len(ps) > 1 else None,
        alt=(collapse(imgs[0].attrs.get("alt") or ""), imgs[0].line) if imgs and imgs[0].attrs.get("alt") else None,
        img=(imgs[0].attrs.get("src"), imgs[0].line) if imgs else None,
        audio=(audios[0].attrs.get("src"), audios[0].line) if audios else None,
        video=(video_src, video_line) if video_src else None,
    )


def new_item(**kw):
    item = dict(sortOrder=None, label=None, word=None, sourceWord=None, emoji=None, description=None,
                image=None, audio=None, video=None, lyrics=None, alt=None, status="READY")
    item.update(kw)
    return item


def alt_for(item: dict, kind: str):
    if kind == "MEDIA":
        return f"Video of {item['word']}"
    if item["image"]:
        return f"Picture of {item['word']}"
    if item["video"]:
        return f"Video of {item['word']}"
    return None


def extract_topic_cards(bl, log, plan, spec):
    page, slug = spec["page"], spec["slug"]
    root = parse_html(bl.text(page))
    cards = root.find_all(lambda n: n.tag == "div" and n.has_class("card"))
    if not cards:
        fail(f"{page}: no .card elements found")
    items = []
    for card in cards:
        f = card_fields(card)
        src = f[spec["word"]]
        if not src:
            fail(f"{page}:{card.line}: card has no '{spec['word']}' text for the word")
        raw_word, wline = src
        where = f"{page}:{wline}"
        word = display_word(log, slug, raw_word, where)
        if spec["label"] == "word":
            label = word
        else:
            if not f[spec["label"]]:
                fail(f"{page}:{card.line}: card has no '{spec['label']}' label")
            label = f[spec["label"]][0]
        emoji = None
        if spec["emoji"]:
            if not f[spec["emoji"]]:
                fail(f"{page}:{card.line}: card has no emoji <p>")
            emoji = f[spec["emoji"]][0]
        it = new_item(label=label, word=word, sourceWord=raw_word, emoji=emoji)
        missing = False
        for role, key in (("image", "img"), ("audio", "audio"), ("video", "video")):
            if f[key]:
                ref, line = f[key]
                name = resolve_media(bl, log, slug, ref, f"{page}:{line}", role)
                if name:
                    it[role] = plan.add(slug, name)
                else:
                    missing = True
        if missing:
            it["status"] = "MEDIA_MISSING"
        it["alt"] = alt_for(it, "TOPIC")
        items.append(it)
    return items, None, None


_SHOWINFO = re.compile(
    r"""showInfo\(\s*(['"])((?:\\.|(?!\1).)*)\1\s*,\s*(['"])((?:\\.|(?!\3).)*)\3\s*(?:,\s*(['"])((?:\\.|(?!\5).)*)\5\s*)?\)""")


def _js_unescape(s: str) -> str:
    return re.sub(r"\\(.)", lambda m: _JS_ESC.get(m.group(1), m.group(1)), s)


def _num(v: str):
    f = float(v)
    return int(f) if f.is_integer() else f


def extract_body_parts(bl, log, plan, spec):
    page, slug = spec["page"], spec["slug"]
    root = parse_html(bl.text(page))
    spots = root.find_all(lambda n: n.has_class("hotspot") and "onclick" in n.attrs)
    if not spots:
        fail(f"{page}: no SVG hotspots found")
    by_name: dict[str, dict] = {}
    items, hotspots = [], []
    for s in spots:
        m = _SHOWINFO.search(s.attrs["onclick"])
        if not m:
            fail(f"{page}:{s.line}: hotspot onclick is not showInfo('<name>', '<description>')")
        raw_name, desc = _js_unescape(m.group(2)), collapse(_js_unescape(m.group(4)))
        audio_raw = _js_unescape(m.group(6)) if m.group(6) else None
        where = f"{page}:{s.line}"
        if raw_name not in by_name:
            word = capitalise_words(raw_name)
            if word != raw_name:
                log.capitalised.append(dict(course=slug, where=where, before=raw_name, after=word))
            it = new_item(label=word, word=word, sourceWord=raw_name, description=desc)
            if audio_raw:
                name = resolve_media(bl, log, slug, audio_raw, where, "audio")
                it["audio"] = plan.add(slug, name) if name else None
            items.append(it)
            by_name[raw_name] = dict(item=it, desc=desc, where=where)
        elif by_name[raw_name]["desc"] != desc:
            fail(f"{where}: hotspot '{raw_name}' repeats with a different description than "
                 f"{by_name[raw_name]['where']}")
        geo = {k: _num(s.attrs[k]) for k in ("x", "y", "cx", "cy", "r", "rx", "ry", "width", "height")
               if k in s.attrs}
        hotspots.append(dict(word=by_name[raw_name]["item"]["word"], shape=s.tag, geometry=geo))
    if not any(it["audio"] for it in items):
        log.notes.append(f"body-parts: {len(items)} items from {len(spots)} hotspots ({page}:"
                         f"{spots[0].line}-{spots[-1].line}); showInfo() passes no audio file and no body-part "
                         f"audio exists in the baseline, so every item has audio null and status READY "
                         f"(INF-10, FUN-E06).")
    img = root.find_all(lambda n: n.tag == "img" and n.attrs.get("id") == "bodyImage")
    svg = root.find_all(lambda n: n.tag == "svg")
    if not img or not svg:
        fail(f"{page}: body diagram image (#bodyImage) or its <svg> overlay not found")
    diagram_name = resolve_media(bl, log, slug, img[0].attrs.get("src"), f"{page}:{img[0].line}", "diagram")
    if not diagram_name:
        fail(f"{page}:{img[0].line}: body diagram image missing")
    diagram = dict(image=plan.add(slug, diagram_name), alt=collapse(img[0].attrs.get("alt") or "") or None,
                   viewBox=svg[0].attrs.get("viewbox"),
                   preserveAspectRatio=svg[0].attrs.get("preserveaspectratio"), hotspots=hotspots)
    return items, diagram, diagram["image"]


def parse_quiz(bl: Baseline, page: str):
    data = read_js_literal(bl, page, "quizData")
    if not isinstance(data, JsArr):
        fail(f"{page}: quizData is not an array")
    out = []
    for q in data:
        if not isinstance(q, JsObj):
            fail(f"{page}: quizData entry is not an object")
        where = f"{page}:{q.line}"
        prompt = q.get("question", q.get("q"))
        if not isinstance(prompt, str) or not prompt.strip():
            fail(f"{where}: question text missing")
        opts = q.get("options")
        if not isinstance(opts, list) or len(opts) < 2:
            fail(f"{where}: options missing")
        if any(isinstance(o, (bool, Negated)) or o is None or isinstance(o, (list, dict)) for o in opts):
            fail(f"{where}: an option is not text or a number")
        options = [collapse(str(o)) for o in opts]
        ans = q.get("answer")
        if ans is None or isinstance(ans, (bool, list, dict, Negated)):
            fail(f"{where}: answer missing")
        answer = collapse(str(ans))
        hits = [i for i, o in enumerate(options) if o == answer]
        if len(hits) != 1:
            fail(f"{where}: answer {answer!r} is not exactly one of the options {options}")
        numeric = any(isinstance(o, (int, float)) for o in opts) or isinstance(ans, (int, float))
        out.append(dict(q=dict(prompt=collapse(prompt), options=options, answerIndex=hits[0]),
                        where=where, answer=answer, numeric=numeric))
    return out


def _tokens(prompt: str, subject: set) -> set:
    out = set()
    for t in re.findall(r"[A-Za-z0-9']+", prompt):
        if len(t) == 1 and t.isupper():
            out.add(t)
            continue
        w = t.lower().strip("'")
        if w.endswith("'s"):
            w = w[:-2]
        if not w or w in STOPWORDS or w in subject:
            continue
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.add(w)
    return out


def _norm(s: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())


def dedupe_reserve(log: Log, slug: str, subject: set, main: list, reserve: list) -> list:
    kept = []
    pool = [(m["q"]["prompt"], m) for m in main]
    for r in reserve:
        rp, ra = r["q"]["prompt"], r["answer"].lower()
        rt = _tokens(rp, subject)
        match = None
        for mp, m in pool:
            same_answer = m["answer"].lower() == ra
            if _norm(mp) == _norm(rp):
                match = (m, "same question text")
                break
            if same_answer and sorted(o.lower() for o in m["q"]["options"]) == sorted(
                    o.lower() for o in r["q"]["options"]):
                match = (m, "same options and answer")
                break
            mt = _tokens(mp, subject)
            if same_answer and rt and mt:
                overlap = len(rt & mt) / min(len(rt), len(mt))
                if overlap >= 0.6:
                    match = (m, f"same answer, {overlap:.0%} key-word overlap")
                    break
        if match:
            log.dedup.append(dict(course=slug, reserve=rp, where=r["where"], main=match[0]["q"]["prompt"],
                                  main_where=match[0]["where"], rule=match[1]))
        else:
            kept.append(r)
            pool.append((rp, r))
    return kept


def extract_media_course(bl, log, plan, spec):
    page, slug = spec["page"], spec["slug"]
    root = parse_html(bl.text(page))
    cards = root.find_all(lambda n: n.tag == "div" and n.has_class("card") and spec["card_key"] in n.attrs)
    data = read_js_literal(bl, page, spec["js"])
    if not isinstance(data, JsObj):
        fail(f"{page}: '{spec['js']}' is not an object")
    if len(cards) != len(data):
        fail(f"{page}: {len(cards)} cards but {len(data)} entries in '{spec['js']}'")
    items, lesson_titles = [], []
    for card in cards:
        key = card.attrs[spec["card_key"]]
        if key not in data:
            fail(f"{page}:{card.line}: card key {key!r} has no entry in '{spec['js']}'")
        entry = data[key]
        f = card_fields(card)
        raw_title = entry.get("title")
        if not isinstance(raw_title, JsStr):
            fail(f"{page}:{entry.line}: title missing")
        emoji, bare = split_leading_emoji(raw_title)
        cleaned = bare
        for rx, rep in TITLE_TYPOS:
            cleaned = rx.sub(rep, cleaned)
        cleaned = title_case(cleaned)
        where = f"{page}:{raw_title.line}"
        if cleaned != bare:
            log.fixes.append(dict(course=slug, where=where, what="display title (typos, spacing, capitals)",
                                  before=bare, after=cleaned, basis="sourceTitle keeps the raw title"))
        label = f["h2"][0] if slug == "rhymes" and f["h2"] else cleaned
        it = new_item(label=label, word=cleaned, sourceWord=str(raw_title), emoji=emoji)
        if f["img"]:
            name = resolve_media(bl, log, slug, f["img"][0], f"{page}:{f['img'][1]}", "image")
            it["image"] = plan.add(slug, name) if name else None
        file_ref = entry.get("file")
        if not isinstance(file_ref, JsStr):
            fail(f"{page}:{entry.line}: file missing")
        vname = resolve_media(bl, log, slug, str(file_ref), f"{page}:{file_ref.line}", "video")
        if vname:
            it["video"] = plan.add(slug, vname)
        else:
            it["status"] = "MEDIA_MISSING"
            log.missing[-1]["effect"] = "video null, item status MEDIA_MISSING (INF-09)" \
                if slug == "stories" else log.missing[-1]["effect"]
        if "lines" in entry:
            lines = entry["lines"]
            if not isinstance(lines, JsArr):
                fail(f"{page}:{entry.line}: lines is not an array")
            it["lyrics"] = "\n".join(recover_lyrics(log, slug, page, lines))
        if not it["image"]:
            it["status"] = "MEDIA_MISSING" if f["img"] else it["status"]
        it["alt"] = alt_for(it, "MEDIA")
        items.append(it)
        lesson_titles.append((cleaned, str(raw_title)))
    return items, lesson_titles


_CAPS_TYPO = re.compile(r"\b([A-Z])([A-Z])([a-z]{2,})\b")


def recover_lyrics(log: Log, slug: str, page: str, lines: JsArr) -> list:
    out: list[str] = []
    for el in lines:
        if isinstance(el, Negated):
            # `"X",!"Y"` evaluates to [..., "X", false, ...]: the '!' belongs to the end of "X".
            if not out:
                fail(f"{page}:{el.line}: '!' before the first lyric line")
            prev_before = out[-1]
            if not prev_before.endswith("!"):
                out[-1] = prev_before + "!"
            log.fixes.append(dict(course=slug, where=f"{page}:{el.line}-{el.value.line}",
                                  what="stray '!' outside a string (FUN-E07): the next line rendered as 'false'",
                                  before=f'"{prev_before}",!"{el.value}"',
                                  after=f'"{out[-1]}", "{el.value}"',
                                  basis="the second verse has the same line as \"Johnny, Johnny!\" "
                                        f"({page}:{_find_line(lines, 'Johnny, Johnny!')})"))
            out.append(str(el.value))
            continue
        if not isinstance(el, str):
            fail(f"{page}:{lines.line}: a lyric line is not text")
        out.append(str(el))
    for i, line in enumerate(out):
        fixed = _CAPS_TYPO.sub(lambda m: m.group(1) + m.group(2).lower() + m.group(3), line)
        if fixed != line:
            src_line = _find_line(lines, line.rstrip("!")) or lines.line
            log.fixes.append(dict(course=slug, where=f"{page}:{src_line}", what="capitalisation typo in lyrics",
                                  before=line, after=fixed, basis="a capital second letter ('JOhnny')"))
            out[i] = fixed
    return out


def _find_line(lines, text):
    for el in lines:
        s = el.value if isinstance(el, Negated) else el
        if isinstance(s, JsStr) and str(s) == text:
            return s.line
    return None


def group_sizes(n: int) -> list:
    if n <= 0:
        return []
    k = math.ceil(n / MAX_LESSON_ITEMS)
    base, extra = divmod(n, k)
    return [base + 1 if i < extra else base for i in range(k)]


def lesson_title(slug: str, chunk: list) -> str:
    a, b = chunk[0], chunk[-1]
    if slug in ("alphabets", "numbers"):
        return f"{a['label']} {EN_DASH} {b['label']}" if a is not b else a["label"]
    return f"{a['word']} to {b['word']}" if a is not b else a["word"]


def learning_page_info(bl: Baseline):
    """Course order and cover images from the Learning hub (second_page.html)."""
    text = bl.text(LEARNING_PAGE)
    root = parse_html(text)
    css = {}
    for m in re.finditer(r"\.([A-Za-z0-9_-]+)\s*\{[^}]*?background-image:\s*url\(\s*['\"]?([^'\")]+)['\"]?\s*\)",
                         text):
        css[m.group(1)] = (m.group(2).strip(), text.count("\n", 0, m.start(2)) + 1)
    order, covers = [], {}
    for card in root.find_all(lambda n: n.tag == "div" and n.has_class("card")):
        btn = [n for n in card.iter() if n.tag == "button" and "onclick" in n.attrs]
        if not btn:
            continue
        m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", btn[0].attrs["onclick"])
        if not m:
            continue
        target = m.group(1)
        order.append(target)
        for cls in (card.attrs.get("class") or "").split():
            if cls != "card" and cls in css:
                covers[target] = css[cls]
    return order, covers


def quiz_hub_icons(bl: Baseline):
    root = parse_html(bl.text(QUIZ_HUB_PAGE))
    icons = {}
    for card in root.find_all(lambda n: n.has_class("quiz-card") and "data-subject" in n.attrs):
        spans = [n for n in card.iter() if n.tag == "span" and n.has_class("card-icon")]
        if spans:
            icons[card.attrs["data-subject"]] = (spans[0].clean_text(), f"{QUIZ_HUB_PAGE}:{spans[0].line}")
    return icons


def background_videos(bl: Baseline):
    found: dict[str, list[str]] = {}
    for name in bl.names:
        if not name.lower().endswith(".html"):
            continue
        root = parse_html(bl.text(name))
        for v in root.find_all(lambda n: n.tag == "video" and n.attrs.get("id") == "bgVideo"):
            srcs = [v.attrs["src"]] if v.attrs.get("src") else []
            srcs += [n.attrs["src"] for n in v.iter() if n.tag == "source" and n.attrs.get("src")]
            for s in srcs:
                found.setdefault(s, []).append(f"{name}:{v.line}")
    return found


def build(bl: Baseline, log: Log, plan: MediaPlan):
    order, covers = learning_page_info(bl)
    icons = quiz_hub_icons(bl)
    courses = []
    for spec in TOPIC_COURSES + MEDIA_COURSES:
        slug, page = spec["slug"], spec["page"]
        kind = "TOPIC" if spec in TOPIC_COURSES else "MEDIA"
        if page not in order:
            fail(f"{LEARNING_PAGE}: no card links to {page}")
        sort_order = order.index(page) + 1
        diagram, cover = None, None
        titles = None
        if kind == "TOPIC" and spec["word"] == "hotspot":
            items, diagram, cover = extract_body_parts(bl, log, plan, spec)
            if page in covers:
                log.notes.append(f"body-parts: cover is the diagram {diagram['image']} (as instructed); the "
                                 f"Learning-page card image '{covers[page][0]}' ({LEARNING_PAGE}:"
                                 f"{covers[page][1]}) is not used and not copied.")
        elif kind == "TOPIC":
            items, _, _ = extract_topic_cards(bl, log, plan, spec)
        else:
            items, titles = extract_media_course(bl, log, plan, spec)
        if cover is None and page in covers:
            cname = resolve_media(bl, log, slug, covers[page][0], f"{LEARNING_PAGE}:{covers[page][1]}", "cover")
            cover = plan.add(slug, cname) if cname else None
        icon = None
        if kind == "TOPIC" and spec["hub"] in icons:
            icon = icons[spec["hub"]][0]
        # lessons
        lessons = []
        if kind == "TOPIC":
            pos = 0
            for li, size in enumerate(group_sizes(len(items)), start=1):
                chunk = items[pos:pos + size]
                pos += size
                for ii, it in enumerate(chunk, start=1):
                    it["sortOrder"] = ii
                lessons.append(dict(title=lesson_title(slug, chunk), sourceTitle=None, sortOrder=li, items=chunk))
        else:
            for li, (it, (clean, raw)) in enumerate(zip(items, titles), start=1):
                it["sortOrder"] = 1
                lessons.append(dict(title=clean, sourceTitle=raw, sortOrder=li, items=[it]))
        # quiz
        quiz, reserve, quiz_page, reserve_page, stats = None, [], None, None, {}
        if kind == "TOPIC":
            quiz_page = spec["quiz"]
            main = parse_quiz(bl, quiz_page)
            for q in main:
                if q["numeric"]:
                    log.fixes.append(dict(course=slug, where=q["where"], what="numeric options stored as text",
                                          before="numbers", after=f"{q['q']['options']}",
                                          basis="options are shown as text; answerIndex points into them"))
            quiz = dict(title=f"{spec['title']} Quiz", passMarkPercent=PASS_MARK, questions=[q["q"] for q in main])
            if len(main) != 10:
                log.warnings.append(f"{slug}: {quiz_page} has {len(main)} questions, not 10")
            stats["quizTotal"] = len(main)
            if spec["reserve"]:
                reserve_page = spec["reserve"]
                res = parse_quiz(bl, reserve_page)
                for q in res:
                    if q["numeric"]:
                        log.fixes.append(dict(course=slug, where=q["where"], what="numeric options stored as text",
                                              before="numbers", after=f"{q['q']['options']}",
                                              basis="options are shown as text; answerIndex points into them"))
                kept = dedupe_reserve(log, slug, spec["subject"], main, res)
                reserve = [q["q"] for q in kept]
                stats["reserveTotal"] = len(res)
            else:
                stats["reserveTotal"] = 0
        course = dict(slug=slug, title=spec["title"], kind=kind, icon=icon,
                      description=spec["describe"]([it for ls in lessons for it in ls["items"]]),
                      coverImage=cover, sortOrder=sort_order, lessons=lessons, quiz=quiz,
                      reserveQuestions=reserve, diagram=diagram,
                      source=dict(lessonPage=page, quizPage=quiz_page, reservePage=reserve_page))
        courses.append((course, stats))
        if kind == "MEDIA":
            log.notes.append(f"{slug}: icon null - no subject emoji for it on {LEARNING_PAGE} or {QUIZ_HUB_PAGE}.")
    courses.sort(key=lambda cs: cs[0]["sortOrder"])
    logo = plan.add("brand", LOGO) if LOGO in bl.name_set else fail(f"{LOGO} missing from the baseline")
    return courses, logo, icons


# ----------------------------------------------------------------------------------------------------
# Self-checks on the built content
# ----------------------------------------------------------------------------------------------------
PATH_FIELDS_ITEM = ("image", "audio", "video")


def content_paths(course: dict) -> list:
    paths = []
    if course["coverImage"]:
        paths.append(course["coverImage"])
    if course["diagram"]:
        paths.append(course["diagram"]["image"])
    for ls in course["lessons"]:
        for it in ls["items"]:
            paths += [it[f] for f in PATH_FIELDS_ITEM if it[f]]
    return paths


def check_path(p: str) -> str | None:
    if p.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", p) or "\\" in p:
        return "absolute or backslash path"
    if any(seg in ("..", ".", "") for seg in p.split("/")):
        return "'..', '.' or empty segment"
    if not re.fullmatch(r"[a-z0-9-]+/[a-z0-9.-]+", p):
        return "not <folder>/<normalised-name>"
    return None


# ----------------------------------------------------------------------------------------------------
# Writing (atomic; only the tool's own outputs)
# ----------------------------------------------------------------------------------------------------
def write_if_changed(path: Path, data: bytes) -> str:
    if path.exists() and path.read_bytes() == data:
        return "unchanged"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)
    return "written"


def disk_free(path: Path) -> int:
    p = path
    while not p.exists():
        p = p.parent
    return shutil.disk_usage(p).free


def fmt_mib(n: int) -> str:
    return f"{n / MIB:,.2f}"


def fmt_gib(n: int) -> str:
    return f"{n / GIB:,.2f} GiB"


# ----------------------------------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------------------------------
def md_cell(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " / ")


def render_report(ctx) -> str:
    L = []
    a = L.append
    a("# Extraction Report — CleverCubs baseline content to course JSON and media library")
    a("")
    a(f"**Generated by `{TOOL}` — do not edit by hand.** Re-run the tool to refresh it. · "
      f"**Mode:** {'dry run (nothing written)' if ctx['dry_run'] else 'write'} · "
      f"**Baseline:** `{ctx['baseline_rel']}` (read-only) · **MB:** MiB (1,048,576 bytes)")
    a("")
    a("---")
    a("")
    a("## 1. Per-course counts")
    a("")
    a("| # | Course | Kind | Lessons | Items | Ready | Media missing | Quiz questions | Reserve kept / in page "
      "| Media files | MB |")
    a("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    tot = dict(lessons=0, items=0, files=0, bytes=0)
    for c, st in ctx["courses"]:
        items = [it for ls in c["lessons"] for it in ls["items"]]
        ready = sum(1 for it in items if it["status"] == "READY")
        mf = ctx["folder_stats"].get(c["slug"], (0, 0))
        q = len(c["quiz"]["questions"]) if c["quiz"] else "—"
        r = f"{len(c['reserveQuestions'])} / {st.get('reserveTotal', 0)}" if c["kind"] == "TOPIC" else "—"
        a(f"| {c['sortOrder']} | `{c['slug']}` | {c['kind']} | {len(c['lessons'])} | {len(items)} | {ready} | "
          f"{len(items) - ready} | {q} | {r} | {mf[0]} | {fmt_mib(mf[1])} |")
        tot["lessons"] += len(c["lessons"])
        tot["items"] += len(items)
        tot["files"] += mf[0]
        tot["bytes"] += mf[1]
    bf = ctx["folder_stats"].get("brand", (0, 0))
    a(f"| — | `brand` (logo) | — | — | — | — | — | — | — | {bf[0]} | {fmt_mib(bf[1])} |")
    a(f"| | **Total** | | **{tot['lessons']}** | **{tot['items']}** | | | | | **{tot['files'] + bf[0]}** | "
      f"**{fmt_mib(tot['bytes'] + bf[1])}** |")
    a("")
    a("Lesson sizes follow `D60`: `n` items make `ceil(n/5)` lessons, larger lessons first. Course order is the "
      f"card order on `{LEARNING_PAGE}`. Covers are that page's card images; icons are the `{QUIZ_HUB_PAGE}` "
      "card icons.")
    a("")
    a("| Course | Lesson sizes | Icon | Cover |")
    a("|---|---|---|---|")
    for c, _ in ctx["courses"]:
        sizes = ", ".join(str(len(ls["items"])) for ls in c["lessons"])
        a(f"| `{c['slug']}` | {sizes} | {c['icon'] or 'null'} | `{c['coverImage']}` |")
    a("")
    a("## 2. Fixes applied")
    a("")
    a("Each is a deliberate change from the baseline text; the raw value is kept in the JSON (`sourceWord`, "
      "`sourceTitle`) wherever a displayed word or title changed.")
    a("")
    a("| # | Course | Baseline location | What | Before | After | Basis |")
    a("|---:|---|---|---|---|---|---|")
    for i, f in enumerate(ctx["log"].fixes, start=1):
        a(f"| {i} | `{f['course']}` | `{f['where']}` | {md_cell(f['what'])} | `{md_cell(f['before'])}` | "
          f"`{md_cell(f['after'])}` | {md_cell(f['basis'])} |")
    a("")
    caps = ctx["log"].capitalised
    a(f"**Capitalisation only** ({len(caps)} words; first letter of each word upper-cased for display, raw text "
      "kept in `sourceWord`):")
    a("")
    a("| Course | Baseline location | Before | After |")
    a("|---|---|---|---|")
    for f in caps:
        a(f"| `{f['course']}` | `{f['where']}` | `{md_cell(f['before'])}` | `{md_cell(f['after'])}` |")
    a("")
    a("## 3. Missing files (referenced by the baseline, absent from it)")
    a("")
    if ctx["log"].missing:
        a("| Course | Referenced at | File | Effect |")
        a("|---|---|---|---|")
        for m in ctx["log"].missing:
            a(f"| `{m['course']}` | `{m['where']}` | `{md_cell(m['file'])}` | {md_cell(m['effect'])} |")
    else:
        a("None.")
    a("")
    a("## 4. Excluded files (present in the baseline, not copied)")
    a("")
    a("**Autoplaying background videos** (`#bgVideo`), excluded by design (`FUN-E26`):")
    a("")
    a("| File | MB | Used as background by |")
    a("|---|---:|---|")
    for name, refs in ctx["bg"]:
        a(f"| `{name}` | {fmt_mib(ctx['sizes'].get(name, 0))} | {', '.join(f'`{r}`' for r in refs)} |")
    a("")
    a("**Excluded by name:**")
    a("")
    for name, why in EXCLUDED_BY_NAME.items():
        a(f"- `{name}` ({fmt_mib(ctx['sizes'].get(name, 0))} MB): {why}.")
    a("")
    a("**Not referenced by any extracted content** (media files only; pages and PHP are not listed):")
    a("")
    a("| File | MB | Mentioned in a baseline page? |")
    a("|---|---:|---|")
    for name, pages in ctx["orphans"]:
        a(f"| `{name}` | {fmt_mib(ctx['sizes'].get(name, 0))} | "
          f"{', '.join(f'`{p}`' for p in pages) if pages else 'no (orphan)'} |")
    a("")
    a(f"Other baseline files not copied: {ctx['non_media_count']} pages/scripts (`.html`, `.php`).")
    a("")
    a("## 5. Reserve questions dropped as duplicates of the main quiz")
    a("")
    a("A hub-quiz (`_qq`) question is dropped when it has the same text as a main question, the same options and "
      "answer, or the same answer with at least 60% of its key words shared.")
    a("")
    a("| Course | Reserve question | Location | Duplicate of | Location | Rule |")
    a("|---|---|---|---|---|---|")
    for d in ctx["log"].dedup:
        a(f"| `{d['course']}` | {md_cell(d['reserve'])} | `{d['where']}` | {md_cell(d['main'])} | "
          f"`{d['main_where']}` | {d['rule']} |")
    a("")
    a("## 6. Notes and open items")
    a("")
    for n in ctx["log"].notes:
        a(f"- {n}")
    for w in ctx["log"].warnings:
        a(f"- ⚠️ {w}")
    for folder, src, kind in ctx["ext_added"]:
        a(f"- `{src}` has no extension; its header is `ftyp` ({kind}), so it is stored as `.mp4` in `{folder}/`.")
    for folder, src, kind in ctx["type_mismatch"]:
        a(f"- ⚠️ `{src}` (in `{folder}/`): the extension does not match the file header ({kind}). Kept as is.")
    a("- `alt` is null for items with no picture or video of their own (numbers, whose visual is emoji text, and "
      "body parts, which are regions of the course diagram).")
    a("- `diagram` (body-parts only, null elsewhere) keeps the SVG hotspot geometry so the diagram can be rebuilt.")
    a("")
    a("## 7. Self-checks")
    a("")
    a("| Check | Result |")
    a("|---|---|")
    for name, ok, detail in ctx["checks"]:
        a(f"| {name} | {'✅' if ok else '⛔'} {md_cell(detail)} |")
    a("")
    a("## 8. Media library and disk space")
    a("")
    mt = ctx["media_totals"]
    a("| Measure | Value |")
    a("|---|---:|")
    a(f"| Files in the library (planned) | {mt['files']} |")
    a(f"| Size of the library | {fmt_mib(mt['bytes'])} MB |")
    a(f"| Copied this run | {mt['copied']} files, {fmt_mib(mt['copied_bytes'])} MB |")
    a(f"| Already present, sha256 verified | {mt['unchanged']} files |")
    a(f"| Free on the media drive before | {fmt_gib(ctx['free_before'])} |")
    a(f"| Free on the media drive after | {fmt_gib(ctx['free_after'])} |")
    a(f"| Minimum allowed after copying | {fmt_gib(MIN_FREE_AFTER)} |")
    a("")
    a("## 9. Outputs")
    a("")
    a("| File | Bytes | sha256 |")
    a("|---|---:|---|")
    for rel, size, digest in ctx["outputs"]:
        a(f"| `{rel}` | {size:,} | `{digest}` |")
    a("")
    return "\n".join(L)


# ----------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------
def find_repo_root(start: Path) -> Path:
    for d in [start, *start.parents]:
        if (d / "CLAUDE.md").is_file() and (d / ".claude").is_dir():
            return d
    fail(f"repository root (a folder holding both CLAUDE.md and .claude/) not found above {start}")


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def run(argv=None) -> int:
    script_dir = Path(__file__).resolve().parent
    root = find_repo_root(script_dir)
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--baseline", default=str(root / "New Task" / "Current Project" / "Kids_learn_project"))
    ap.add_argument("--out-content", default=str(root / "New Task" / "Updated Project" / "app" / "src" / "main"
                                                  / "resources" / "content"))
    ap.add_argument("--out-media", default=str(root / "New Task" / "Updated Project" / "media"))
    ap.add_argument("--dry-run", action="store_true", help="parse and plan only; write nothing")
    args = ap.parse_args(argv)
    baseline = Path(args.baseline).resolve()
    out_content = Path(args.out_content).resolve()
    out_media = Path(args.out_media).resolve()
    report_path = script_dir / "extraction-report.md"
    for p in (out_content, out_media, report_path):
        if is_within(p, baseline):
            fail(f"output {p} is inside the read-only baseline {baseline}")

    free_before = disk_free(out_media)
    bl = Baseline(baseline)
    log = Log()
    plan = MediaPlan(bl)
    courses, logo_rel, _icons = build(bl, log, plan)

    # ---- media plan: sizes, hashes, background videos, orphans
    bg = background_videos(bl)
    sizes = {n: bl.path(n).stat().st_size for n in bl.names}
    copy_rows = []   # (folder, source, new_name)
    for folder, src in plan.order:
        copy_rows.append((folder, src, plan.by_folder[folder][src]))
    used = {src for _, src, _ in copy_rows}
    for s in bg:
        if s in used:
            log.warnings.append(f"background video '{s}' is also referenced by content; it was copied")
    missing_bg = [s for s in bg if s not in bl.name_set]
    for s in missing_bg:
        log.warnings.append(f"background video '{s}' referenced by {bg[s]} is not in the baseline")
    page_texts = {n: bl.text(n) for n in bl.names if n.lower().endswith((".html", ".php"))}
    orphans, non_media = [], 0
    for n in bl.names:
        if n in used or n in bg or n in EXCLUDED_BY_NAME:
            continue
        stem, ext = split_ext(n)
        if ext in ("html", "php"):
            non_media += 1
            continue
        if ext is None or ext in MEDIA_EXT:
            orphans.append((n, [p for p, t in page_texts.items() if n in t]))
        else:
            non_media += 1
            log.warnings.append(f"'{n}' is neither a page nor a known media type; not copied")

    # ---- self-checks
    checks = []
    all_paths = []
    bad = []
    for c, _ in courses:
        for p in content_paths(c):
            all_paths.append(p)
            why = check_path(p)
            if why:
                bad.append(f"{c['slug']}: {p} ({why})")
    checks.append(("Media paths are relative `<folder>/<name>` with no `..` or drive", not bad,
                   f"{len(all_paths)} paths" if not bad else "; ".join(bad)))
    planned = {f"{f}/{n}" for f, _, n in copy_rows}
    not_planned = sorted({p for p in all_paths if p not in planned})
    checks.append(("Every JSON media path is in the copy plan", not not_planned,
                   "all planned" if not not_planned else ", ".join(not_planned)))
    topic_quiz = [(c["slug"], len(c["quiz"]["questions"])) for c, _ in courses if c["kind"] == "TOPIC"]
    bad_q = [f"{s}={n}" for s, n in topic_quiz if n != 10]
    checks.append(("Every TOPIC quiz has 10 questions", not bad_q,
                   f"{len(topic_quiz)} quizzes" if not bad_q else ", ".join(bad_q)))
    bad_ai = [c["slug"] for c, _ in courses if c["quiz"]
              for q in c["quiz"]["questions"] + c["reserveQuestions"]
              if not (0 <= q["answerIndex"] < len(q["options"]))]
    checks.append(("Every answerIndex points into its options", not bad_ai, "ok" if not bad_ai else str(bad_ai)))
    bg_names = sorted(bg)
    checks.append(("Background videos found (`#bgVideo`)", True, f"{len(bg_names)}: " + ", ".join(bg_names)))

    # ---- space check before any write
    to_copy_bytes = 0
    src_hash: dict[str, str] = {}
    for folder, src, new in copy_rows:
        src_hash[src] = src_hash.get(src) or sha256_file(bl.path(src))
        dst = out_media / folder / new
        if not (dst.exists() and dst.stat().st_size == sizes[src] and sha256_file(dst) == src_hash[src]):
            to_copy_bytes += sizes[src]
    remaining = free_before - to_copy_bytes
    checks.append(("Free space after copying stays at or above 1.5 GiB", remaining >= MIN_FREE_AFTER,
                   f"{fmt_gib(free_before)} free, {fmt_mib(to_copy_bytes)} MB to copy, "
                   f"{fmt_gib(remaining)} would remain"))
    if remaining < MIN_FREE_AFTER:
        fail(f"not enough disk space: {fmt_gib(free_before)} free, {fmt_mib(to_copy_bytes)} MB to copy, "
             f"only {fmt_gib(remaining)} would remain (minimum {fmt_gib(MIN_FREE_AFTER)}). Nothing was copied.")
    if bad or not_planned or bad_ai:
        fail("self-checks failed: " + "; ".join(bad + not_planned + [str(x) for x in bad_ai]))

    # ---- copy media (verified)
    copied = unchanged = copied_bytes = 0
    csv_rows = []
    folder_stats: dict[str, tuple[int, int]] = {}
    for folder, src, new in copy_rows:
        dst = out_media / folder / new
        digest = src_hash[src]
        n_files, n_bytes = folder_stats.get(folder, (0, 0))
        folder_stats[folder] = (n_files + 1, n_bytes + sizes[src])
        csv_rows.append((folder, f"{folder}/{new}", src, sizes[src], digest))
        if args.dry_run:
            if dst.exists() and dst.stat().st_size == sizes[src] and sha256_file(dst) == digest:
                unchanged += 1
            else:
                copied += 1
                copied_bytes += sizes[src]
            continue
        if dst.exists() and dst.stat().st_size == sizes[src] and sha256_file(dst) == digest:
            unchanged += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.with_name(dst.name + ".part")
        shutil.copyfile(bl.path(src), tmp)
        got = sha256_file(tmp)
        if got != digest:
            tmp.unlink()
            fail(f"sha256 mismatch copying {src} -> {dst}: {got} != {digest}")
        os.replace(tmp, dst)
        if sha256_file(dst) != digest:
            fail(f"sha256 mismatch after placing {dst}")
        copied += 1
        copied_bytes += sizes[src]

    # extra files in our output folders (never deleted; reported)
    if out_media.exists():
        for f in sorted(out_media.rglob("*")):
            if f.is_file():
                rel = f.relative_to(out_media).as_posix()
                if rel != "MEDIA-MAP.csv" and rel not in planned:
                    log.warnings.append(f"media/{rel} is not part of this run's plan (left untouched)")
    expected_json = {f"{c['slug']}.json" for c, _ in courses}
    if out_content.exists():
        for f in sorted(out_content.glob("*.json")):
            if f.name not in expected_json:
                log.warnings.append(f"content/{f.name} is not produced by this tool (left untouched)")

    # ---- serialise
    outputs = []
    json_blobs = {}
    for c, _ in courses:
        blob = (json.dumps(c, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        json_blobs[c["slug"]] = blob
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["course", "new_path", "original_name", "bytes", "sha256"])
    for row in csv_rows:
        w.writerow(row)
    csv_blob = buf.getvalue().encode("utf-8")

    upd = root / "New Task" / "Updated Project"

    def rel_to_upd(p: Path) -> str:
        try:
            return p.relative_to(upd).as_posix()
        except ValueError:
            return p.as_posix()

    for slug, blob in json_blobs.items():
        outputs.append((rel_to_upd(out_content / f"{slug}.json"), len(blob), hashlib.sha256(blob).hexdigest()))
    outputs.append((rel_to_upd(out_media / "MEDIA-MAP.csv"), len(csv_blob), hashlib.sha256(csv_blob).hexdigest()))

    write_status = {}
    if not args.dry_run:
        for slug, blob in json_blobs.items():
            write_status[f"{slug}.json"] = write_if_changed(out_content / f"{slug}.json", blob)
        write_status["MEDIA-MAP.csv"] = write_if_changed(out_media / "MEDIA-MAP.csv", csv_blob)
        # verify every JSON media path now exists in the library
        missing_after = [p for p in all_paths if not (out_media / p).is_file()]
        checks.append(("Every JSON media path exists in the media folder", not missing_after,
                       f"{len(set(all_paths))} distinct paths present" if not missing_after
                       else ", ".join(missing_after)))
        if missing_after:
            fail("media paths missing after copy: " + ", ".join(missing_after))

    free_after = disk_free(out_media)
    ctx = dict(dry_run=args.dry_run, baseline_rel=rel_to_upd(baseline) if is_within(baseline, upd) else
               (baseline.relative_to(root).as_posix() if is_within(baseline, root) else baseline.as_posix()),
               courses=courses, folder_stats=folder_stats, log=log,
               bg=[(n, bg[n]) for n in sorted(bg)], sizes=sizes, orphans=orphans, non_media_count=non_media,
               ext_added=plan.ext_added, type_mismatch=plan.type_mismatch, checks=checks,
               media_totals=dict(files=len(copy_rows), bytes=sum(sizes[s] for _, s, _ in copy_rows),
                                 copied=copied, copied_bytes=copied_bytes, unchanged=unchanged),
               free_before=free_before, free_after=free_after, outputs=outputs)
    report = render_report(ctx)
    if not args.dry_run:
        write_status["extraction-report.md"] = write_if_changed(report_path, report.encode("utf-8"))

    # ---- console summary
    print(f"{'DRY RUN - nothing written' if args.dry_run else 'Written'}")
    print(f"baseline : {baseline}")
    print(f"content  : {out_content}")
    print(f"media    : {out_media}")
    print(f"report   : {report_path}")
    for c, st in courses:
        items = sum(len(ls['items']) for ls in c['lessons'])
        q = len(c['quiz']['questions']) if c['quiz'] else 0
        print(f"  {c['sortOrder']:>2} {c['slug']:<11} lessons={len(c['lessons']):>2} items={items:>2} quiz={q:>2} "
              f"reserve={len(c['reserveQuestions']):>2} media={folder_stats.get(c['slug'], (0, 0))[0]:>3} "
              f"{fmt_mib(folder_stats.get(c['slug'], (0, 0))[1]):>8} MB"
              + (f"  [{write_status.get(c['slug'] + '.json')}]" if write_status else ""))
    print(f"media files={len(copy_rows)} size={fmt_mib(ctx['media_totals']['bytes'])} MB "
          f"{'to copy' if args.dry_run else 'copied'}={copied} ({fmt_mib(copied_bytes)} MB) verified-present={unchanged}")
    print(f"fixes={len(log.fixes)} capitalised={len(log.capitalised)} missing={len(log.missing)} "
          f"reserve-duplicates-dropped={len(log.dedup)} warnings={len(log.warnings)}")
    print(f"free space: before {fmt_gib(free_before)}, after {fmt_gib(free_after)}")
    for name, ok, detail in checks:
        print(f"  [{'ok' if ok else 'FAIL'}] {name}: {detail}")
    if write_status:
        print("outputs: " + ", ".join(f"{k}={v}" for k, v in write_status.items() if not k.endswith(".json"))
              + f", json written={sum(1 for k, v in write_status.items() if k.endswith('.json') and v == 'written')}"
              + f" unchanged={sum(1 for k, v in write_status.items() if k.endswith('.json') and v == 'unchanged')}")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    try:
        return run()
    except ExtractionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
