#!/usr/bin/env python3
"""Check that each panel's HTML fragment is well-formed before it is published.

The weekly job writes `data/panels/<tab>.json` as a blob of hand-authored HTML.
Nothing validated it, and an unbalanced tag does not fail loudly — the browser
silently reparents whatever came after it. On 2026-09-22 one extra `</div>` in
the third decision card closed `.xd` early, so cards 4 and 5 fell out of the
grid and rendered full-width. The page looked fine enough that it shipped and
sat live for two refreshes.

Checks, per panel:
  - every tag opens and closes in order (void elements excluded)
  - the panel declares the section letters the renderer expects, in order
  - the panel is a fragment: no <html>, <head>, <body> or doctype

Usage:
    python3 tools/validate-panels.py [data-dir]     # default: data

Exits 0 when every panel is clean, 1 on the first panel that is not.
"""
import json
import pathlib
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}
FORBIDDEN = {"html", "head", "body"}
# The letters run A-K across ops and ctrl; exec carries its own numbered series.
EXPECTED = {"exec": ["01"],
            "ops": list("ABCDEFG"),
            "ctrl": list("HIJK")}


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.keys = [], [], []
        self._in_key = False

    def handle_starttag(self, tag, attrs):
        if tag in FORBIDDEN:
            self.errors.append(f"line {self.getpos()[0]}: <{tag}> — panels are fragments")
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()[0]))
        if tag == "span" and dict(attrs).get("class") == "k":
            self._in_key = True

    def handle_data(self, data):
        if self._in_key:
            self.keys.append(data.strip())
            self._in_key = False

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: stray </{tag}>")
            return
        open_tag, open_line = self.stack[-1]
        if open_tag != tag:
            self.errors.append(
                f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> opened on line {open_line}")
            return
        self.stack.pop()

    def handle_decl(self, decl):
        self.errors.append(f"line {self.getpos()[0]}: <!{decl}> — panels are fragments")


def check(tab, html):
    p = Balance()
    p.feed(html)
    p.close()
    errors = list(p.errors)
    errors += [f"<{t}> opened on line {n} is never closed" for t, n in p.stack]
    want = EXPECTED.get(tab)
    if want is not None and p.keys != want:
        errors.append(f"section letters are {p.keys or '[]'}, expected {want} — "
                      "renumbering breaks the cross-tab A-K sequence")
    return errors


def main(root="data"):
    panels = sorted((pathlib.Path(root) / "panels").glob("*.json"))
    if not panels:
        sys.exit(f"no panels under {root}/panels")
    failed = False
    for path in panels:
        d = json.loads(path.read_text(encoding="utf-8"))
        errors = check(d.get("id", path.stem), d.get("html", ""))
        if errors:
            failed = True
            print(f"FAIL {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"ok   {path}  ({len(d.get('html','')):,} chars)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
