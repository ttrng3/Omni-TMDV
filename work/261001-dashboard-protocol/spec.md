# Spec

Status: approved by Ty 01/10 (same words as the intent).

- `verification/dashboard.md`: promise, clean state, 4 steps (script, live page in Chrome, console, preview), invariants, adversary, sanctioned substitutes, evidence, not covered, traps.
- `tools/verify_live.py` (stdlib only, not served): 12 verdicts as JSON, exit 0 only when all pass. It runs `tools/validate-panels.py` as one verdict and adds: manifest consistency, history rows kept as a prefix of the previous commit's, every tracked text file read, live equals `main` for every served file, private files exist and 404, `robots.txt` disallows all, `exec` has three KPI cards, heartbeat and data freshness, personal traces (storage links, email addresses, bare handles with an at-sign and no domain; by count and file, across served files and every tracked text file) and forbidden words supplied at run time (served files only; docs may name the other entity's label).
- No change to the page, the data, `.pages-allow` or the README.
- Promise: after #14 is live and this is merged, step 1 prints `"pass": true` and step 2 prints six trues. Before #14, only `no_personal_traces` fails, on the handles #14 removes.
