#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "EPR Command Dashboard v3 WHO blue.dc.html"
BUNDLE = ROOT / "index.html"
DATA = ROOT / "data.json"
SEED_RE = re.compile(r"const SEED = \{.*?\n\};\n", re.S)

TEMPLATE_OPEN = '<script type="__bundler/template">'
FONTS_LINK_RE = re.compile(r'<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet" />')
THUMBNAIL_RE = re.compile(r'<template id="__bundler_thumbnail">.*?</template>', re.S)
CAMEL_ATTR_RE = re.compile(r'(\s)([a-z]+[A-Z][A-Za-z0-9]*)(\s*=)')
FONT_FACE_RE = re.compile(r"/\* [\w-]+ \*/\s*@font-face \{.*?\}", re.S)


def read_template_line(lines):
    for i, line in enumerate(lines):
        if line.strip() == TEMPLATE_OPEN:
            return i + 1
    sys.exit("build.py: template block not found in index.html")


def encode_camel(match):
    kebab = re.sub(r"[A-Z]", lambda c: "-" + c.group(0).lower(), match.group(2))
    return match.group(1) + "sc-camel-" + kebab + match.group(3)


def sync_seed():
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        sys.exit(f"build.py: data.json is not valid JSON — {err}")
    seed = "const SEED = " + json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/") + ";\n"
    src = SOURCE.read_text(encoding="utf-8")
    updated, n = SEED_RE.subn(lambda _: seed, src, count=1)
    if not n:
        sys.exit("build.py: SEED block not found in the source")
    if updated != src:
        SOURCE.write_text(updated, encoding="utf-8")
        print("data.json copied into the source")


def main():
    sync_seed()
    lines = BUNDLE.read_text(encoding="utf-8").split("\n")
    tpl_idx = read_template_line(lines)
    current = json.loads(lines[tpl_idx])

    runtime = re.search(r'<script src="([0-9a-f-]{36})"></script>', current)
    if not runtime:
        sys.exit("build.py: runtime reference not found in the current bundle")
    faces = [f for f in FONT_FACE_RE.findall(current) if "'IBM Plex Sans'" in f]
    if not faces:
        sys.exit("build.py: embedded IBM Plex Sans @font-face rules not found")

    src = SOURCE.read_text(encoding="utf-8")
    src = src.replace('<script src="./support.js"></script>', f'<script src="{runtime.group(1)}"></script>', 1)
    src, n_fonts = FONTS_LINK_RE.subn(lambda _: "<style>" + "\n".join(faces) + "\n</style>", src, count=1)
    if not n_fonts:
        sys.exit("build.py: Google Fonts <link> not found in the source")
    src = THUMBNAIL_RE.sub("", src, count=1)

    start, end = src.index("<x-dc>"), src.index("</x-dc>")
    src = src[:start] + CAMEL_ATTR_RE.sub(encode_camel, src[start:end]) + src[end:]

    lines[tpl_idx] = json.dumps(src, ensure_ascii=False).replace("</", "<\\u002F")
    for i in range(tpl_idx):
        if lines[i].strip() == "<html>":
            lines[i] = lines[i].replace("<html>", '<html lang="en">')
        lines[i] = lines[i].replace("<title>Bundled Page</title>", "<title>EPR Workbench</title>")
    BUNDLE.write_text("\n".join(lines), encoding="utf-8")
    print(f"index.html rebuilt from {SOURCE.name} ({len(src):,} chars, {len(faces)} font faces)")


if __name__ == "__main__":
    main()
