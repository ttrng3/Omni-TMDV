#!/usr/bin/env python3
"""Machine half of verification/dashboard.md: is the live page what main says, and is main sound?

Run from an up-to-date checkout of main:
  git pull --ff-only && python3 tools/verify_live.py --forbid WORD [WORD ...]

--forbid takes words that must not appear in anything served (another entity's name, a person's
account handle that leaked before). The runner supplies them so the list can change without a PR.
Without them the entity check fails rather than passing unchecked.

Panel structure, cross-references and the append-only history are checked by
tools/validate-panels.py, which this script runs and reports as one verdict.

Prints one JSON object of verdicts and exits 0 only when every verdict is true.
Matches of personal traces are reported by count and file, never by value.
"""
import argparse, datetime as dt, glob, hashlib, json, pathlib, re, subprocess, sys, time, unicodedata, urllib.request, urllib.error
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = "https://ttrng3.github.io/Omni-TMDV/"
# Tracked but never served (.pages-allow); each must exist on main and answer 404 live.
PRIVATE = ["README.md", "CLAUDE.md", "REVIEW.md", "data/.last-check", "tools/validate-panels.py",
           "tools/build-fragment.py", "tools/reconcile.py", "tools/verify_live.py", "verification/dashboard.md",
           ".github/scripts/freshness.py", ".pages-allow"]
# Storage links, full email addresses, and bare handles ("name@" with no domain, as escalation senders were written).
TRACES = re.compile(r"/personal/|sharepoint\.com|1drv\.ms|[\w.+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}|\b[a-z][a-z0-9._-]{2,}@(?![\w-])", re.I)
HEARTBEAT_MAX = 9  # the watchdog pipeline-wiring's collect_status.py sets for this pipeline
DATA_MAX = 24      # MAX_DATA_AGE_DAYS default in .github/scripts/freshness.py (its run clock, RUN_MAX, is 10)
EXEC_KPIS = 3      # README "What belongs on each tab": exec keeps three KPI cards


def get(path, tries=2):
    """One retry on a network error or a 5xx: a blip must not read as a mismatch."""
    url = f"{LIVE}{path}?v={int(time.time())}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "verify-live"}), timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return get(path, tries - 1) if e.code >= 500 and tries > 1 else (e.code, b"")
    except Exception as e:
        return get(path, tries - 1) if tries > 1 else (str(e), b"")


def age_days(stamp):
    """Days since an ISO stamp ('...Z', '+00:00', 3/6-digit fractions); None if unreadable."""
    try:
        t = dt.datetime.fromisoformat(stamp.strip().replace("Z", "+00:00"))
        t = t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
        return round((dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 86400, 1)
    except (ValueError, AttributeError):
        return None


class KpiCount(HTMLParser):
    """Counts elements whose class list holds `kpi`, as the browser's `#exec .kpi` does."""
    def __init__(self):
        super().__init__()
        self.n = 0

    def handle_starttag(self, tag, attrs):
        self.n += "kpi" in (dict(attrs).get("class") or "").split()


def norm(t):
    return unicodedata.normalize("NFC", str(t or "")).casefold()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forbid", nargs="*", default=[])
    forbid = [norm(w) for w in ap.parse_args().forbid if w.strip()]

    v, info, live = {}, {}, {}
    try:
        d = json.loads((ROOT / "data/index.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        d = {}
        info["index_error"] = str(e)
    panels = d.get("panels", {}) if isinstance(d.get("panels"), dict) else {}
    tabs = d.get("tabs", []) if isinstance(d.get("tabs"), list) else []

    # The validator owns structure: balanced tags, section letters, "mục X" references, append-only history.
    r = subprocess.run([sys.executable, str(ROOT / "tools/validate-panels.py")], cwd=ROOT, capture_output=True, text=True)
    v["validator_passes"] = r.returncode == 0
    info["validator"] = (r.stdout + r.stderr).strip().splitlines()[-6:]

    v["manifest_consistent"] = (bool(tabs) and [t.get("id") for t in tabs] == list(panels) and
                                all((ROOT / f"data/panels/{p}.json").exists() for p in panels.values()) and
                                bool(d.get("history")) and (ROOT / "data" / str(d.get("history"))).exists())

    served = ["index.html", "robots.txt", "data/index.json"] + \
             ([f"data/{d['history']}"] if d.get("history") else []) + [f"data/panels/{p}.json" for p in panels.values()]
    for p in served:
        st, body = get(p)
        live[p] = body
        info[p] = {"status": st, "live": hashlib.sha256(body).hexdigest()[:12],
                   "main": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()[:12] if (ROOT / p).exists() else None}
    v["served_equals_main"] = all(info[p]["status"] == 200 and info[p]["live"] == info[p]["main"] for p in served)
    info["served_mismatch"] = [p for p in served if info[p]["status"] != 200 or info[p]["live"] != info[p]["main"]]
    for p in served:
        del info[p]

    work = sorted(glob.glob(str(ROOT / "work/*/intent.md")))[:1]  # any one work file, found at run time
    private = PRIVATE + [str(pathlib.Path(w).relative_to(ROOT)) for w in work]
    info["private_status"] = {p: get(p)[0] for p in private}
    info["private_missing_on_main"] = [p for p in private if not (ROOT / p).exists()] + ([] if work else ["work/*/intent.md"])
    v["private_not_served"] = all(s == 404 for s in info["private_status"].values()) and not info["private_missing_on_main"]
    v["robots_disallow_all"] = re.search(r"(?mi)^\s*Disallow:\s*/\s*$", live.get("robots.txt", b"").decode("utf-8", "replace")) is not None

    try:
        exec_html = json.loads((ROOT / f"data/panels/{panels.get('exec', 'exec')}.json").read_text(encoding="utf-8")).get("html", "")
    except (OSError, ValueError):
        exec_html = ""
    kc = KpiCount()
    kc.feed(exec_html)
    info["exec_kpi_cards"] = kc.n
    v["exec_three_kpis"] = info["exec_kpi_cards"] == EXEC_KPIS

    beat = ((ROOT / "data/.last-check").read_text(encoding="utf-8").split() or [""])[0] if (ROOT / "data/.last-check").exists() else ""
    info["heartbeat_age_days"], info["data_age_days"] = age_days(beat), age_days(str(d.get("generatedUtc", "")))
    # -1 allows clock skew; a stamp further in the future (a wrong year) would otherwise pass forever.
    v["heartbeat_fresh"] = info["heartbeat_age_days"] is not None and -1 <= info["heartbeat_age_days"] <= HEARTBEAT_MAX
    v["data_fresh"] = info["data_age_days"] is not None and -1 <= info["data_age_days"] <= DATA_MAX

    # Every served path, both as Pages serves it and as main holds it (main may not be deployed yet).
    texts = {f"live:{p}": b.decode("utf-8", "replace") for p, b in live.items()}
    texts.update({f"main:{p}": (ROOT / p).read_text(encoding="utf-8") for p in served if (ROOT / p).exists()})
    # The repo is public too: every other tracked text file on main, except the two that spell out these patterns.
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    for p in tracked:
        if p in served or p in ("tools/verify_live.py", "verification/dashboard.md"):
            continue
        try:
            texts[f"main:{p}"] = (ROOT / p).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            pass
    hits = {p: len(TRACES.findall(t)) for p, t in texts.items()}
    info["traces"] = {p: n for p, n in hits.items() if n}
    v["no_personal_traces"] = not info["traces"]
    info["forbid_checked"] = len(forbid)
    # Forbidden words on what is served only: docs may name the other entity's label (REVIEW.md allows it).
    served_texts = [t for k, t in texts.items() if k.split(":", 1)[1] in served]
    v["no_forbidden_words"] = bool(forbid) and not any(w in norm(t) for w in forbid for t in served_texts)

    print(json.dumps({"pass": all(v.values()), "verdicts": v, "info": info}, ensure_ascii=False, indent=1))
    sys.exit(0 if all(v.values()) else 1)


if __name__ == "__main__":
    main()
