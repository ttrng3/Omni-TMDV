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

And on data/history.json, if present:
  - the series only ever grows, and past rows are never rewritten (compared
    against the copy in git HEAD)
  - periods are unique and in chronological order
  - every metric the manifest declares exists in every row, with a trust tag

The history guard matters more than it looks. This dashboard already lost its
trend once: before the 2026-09-22 split each period lived inside a 300 KB HTML
file that the next run deleted, and only two periods survived in git. Rows
before 22/09 were reconstructed from run records on Drive. There is no third
copy to reconstruct from.

Usage:
    python3 tools/validate-panels.py [data-dir]     # default: data

Exits 0 when every panel is clean, 1 on the first panel that is not.
"""
import json
import pathlib
import re
import subprocess
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}
FORBIDDEN = {"html", "head", "body"}
# The letters run A-L across ops and ctrl as ONE sequence; exec carries its own
# numbered series. Extending it means editing this map AND every prose reference
# to a letter that moved — which REFERENCED below now checks.
EXPECTED = {"exec": ["01"],
            "ops": list("ABCDEFGH"),
            "ctrl": list("IJKL")}
# Prose points at sections by letter ("(mục E)"). When a section moves, those
# references go stale silently and send a reader to the wrong table. On
# 2026-09-22 a renumber left three "(mục C)" pointing at the funnel instead of
# the disputed-openings block, and nothing noticed until the next renumber.
REFERENCE = re.compile(r"mục ([A-Z])\b")


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


def check_history(path):
    """Append-only, ordered, fully-tagged. Compared against git HEAD when we can."""
    errors = []
    d = json.loads(path.read_text(encoding="utf-8"))
    series = d.get("series") or []
    if not series:
        return ["history has no series rows"]

    keys = [m["key"] for m in d.get("metrics", [])]
    seen = set()
    prev_iso = ""
    for i, row in enumerate(series):
        where = f"row {i} ({row.get('asof', '?')})"
        iso = row.get("iso", "")
        if not iso:
            errors.append(f"{where}: no iso date")
        elif iso < prev_iso:
            errors.append(f"{where}: iso {iso} is older than the row before it ({prev_iso})")
        prev_iso = max(prev_iso, iso)
        if iso in seen:
            errors.append(f"{where}: duplicate period {iso} — append a run, do not re-file one")
        seen.add(iso)
        if not row.get("src"):
            errors.append(f"{where}: no src — every row states where its numbers came from")
        for k in keys:
            cell = row.get(k)
            if cell is None:
                errors.append(f"{where}: missing metric '{k}'")
            elif "v" not in cell or not cell.get("t"):
                errors.append(f"{where}: metric '{k}' has no value/trust tag")

    # Append-only, checked against what is committed rather than trusted.
    head = subprocess.run(["git", "show", f"HEAD:{path.as_posix()}"],
                          capture_output=True, text=True)
    if head.returncode == 0:
        try:
            old = json.loads(head.stdout).get("series") or []
        except ValueError:
            old = []
        if len(series) < len(old):
            errors.append(f"history shrank: {len(old)} rows in HEAD, {len(series)} now — "
                          "rows are appended, never removed")
        else:
            for i, (a, b) in enumerate(zip(old, series)):
                if a != b:
                    errors.append(f"row {i} ({a.get('asof', '?')}) was rewritten — "
                                  "a past period is a record, not a draft")
    return errors


def check_references(panels):
    """Every 'mục X' in prose must name a section that exists somewhere."""
    letters, refs = set(), []
    for tab, html in panels:
        letters.update(re.findall(r'<span class="k">(\w+)</span>', html))
        for m in REFERENCE.finditer(html):
            start = max(0, m.start() - 40)
            refs.append((tab, m.group(1), html[start:m.end() + 10]))
    return [f"{tab}: 'mục {ltr}' points at no section (letters in use: "
            f"{''.join(sorted(letters))}) — near ...{ctx[-60:].strip()}"
            for tab, ltr, ctx in refs if ltr not in letters]


def main(root="data"):
    panels = sorted((pathlib.Path(root) / "panels").glob("*.json"))
    if not panels:
        sys.exit(f"no panels under {root}/panels")
    failed = False

    hist = pathlib.Path(root) / "history.json"
    if hist.exists():
        errors = check_history(hist)
        if errors:
            failed = True
            print(f"FAIL {hist}")
            for e in errors:
                print(f"  - {e}")
        else:
            n = len(json.loads(hist.read_text(encoding="utf-8"))["series"])
            print(f"ok   {hist}  ({n} periods, append-only)")
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

    loaded = [(json.loads(p.read_text(encoding="utf-8")).get("id", p.stem),
               json.loads(p.read_text(encoding="utf-8")).get("html", "")) for p in panels]
    ref_errors = check_references(loaded)
    if ref_errors:
        failed = True
        print("FAIL cross-references")
        for e in ref_errors:
            print(f"  - {e}")
    else:
        print("ok   cross-references (every 'mục X' resolves)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
