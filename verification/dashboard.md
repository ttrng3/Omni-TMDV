# Verification: the dashboard

## Promise

Every file https://ttrng3.github.io/Omni-TMDV/ serves (the page, `robots.txt`, `index.json`, `history.json`, the three panels) is byte-identical to `main`. `main`'s panels pass `tools/validate-panels.py` (balanced HTML, section letters in order, every "mục X" resolves, history only grows). The manifest's tabs, panels and history agree; `exec` holds exactly three KPI cards; `robots.txt` disallows crawlers. The page renders all three tabs with the same section letters as the panel files, the trend, and no console error. No private file, personal link, email address or account handle is served. The Cowork preview carries either `main`'s data or the last weekly run's.

## Clean state

```bash
cd ~/Projects/Omni-TMDV && git checkout main && git pull --ff-only
```
Run after a weekly run (the TMDV routine's cron, `0 11 * * 0` UTC = 18:00 Sunday Hanoi, per pipeline-wiring's `collect_status.py` on 01/10) or after any merge. Wait for the merge's Pages run to go green first (`gh run list -w "Pages (allowlist)" -L1`).

## Steps

1. **Repo and live site.** `python3 tools/verify_live.py --forbid <words>` → exit 0 and `"pass": true`. The words come from the runner's own notes: the other entity's name, and every person's account handle that has appeared on this page before (four did, until 01/10, #14). Names of people are never written into this repo. Without `--forbid` the entity verdict fails on purpose.
2. **Live page in Chrome.** Open https://ttrng3.github.io/Omni-TMDV/. Run the script under Invariants. Expected: one tab button per manifest tab; each panel's section letters in the page equal those in its panel file; `exec` shows three KPI cards; the trend table is present when `history.json` has two or more periods; the header loaded (no "Không nạp được dữ liệu"); no link to a storage host.
3. **Console.** Reload, then read errors for `TypeError|ReferenceError|Uncaught|SyntaxError`. Expected: none.
4. **Preview.** Get the preview link from the TMDV routine's prompt (`RemoteTrigger get`). Never write it here. Find the last weekly run: `c=$(git log --format='%h %s' -- data/index.json | grep -v ' (#[0-9]*)$' | head -1 | cut -d' ' -f1)`, the last commit to `index.json` that is not a squash-merged PR (their titles end `(#N)`); routine runs commit directly. `Artifact list` the preview's files and `Artifact read` `data/index.json` and `data/panels/exec.json`. Expected: `index.html` (the page fragment the routine's mirror step publishes) plus the data files `main` or `$c` holds, nothing else; each file read has the sha256 of either `main`'s copy (`shasum -a 256 <path>`) or `$c`'s (`git show $c:<path> | shasum -a 256`). Matching `$c` and not `main` means PRs changed data since the run: behind by design until the next run.

## Invariants

Step 1 prints these verdicts, all of which must be true: `validator_passes`, `manifest_consistent`, `served_equals_main`, `private_not_served`, `robots_disallow_all`, `exec_three_kpis` (README "What belongs on each tab"), `heartbeat_fresh` (≤ 9 days, pipeline-wiring's watchdog for this pipeline), `data_fresh` (≤ 24 days, `freshness.py`'s `MAX_DATA_AGE_DAYS` default), `no_personal_traces`, `no_forbidden_words`.

Step 2, in the page:
```js
window.confirm=()=>true; window.alert=()=>{};
await new Promise(r=>setTimeout(r,3000));
const idx=await fetch('data/index.json?v='+Date.now()).then(r=>r.json());
const keysOf=html=>[...new DOMParser().parseFromString(html,'text/html').querySelectorAll('span.k')].map(s=>s.textContent.trim());
const panelsMatch=[];
for(const id of Object.keys(idx.panels)){
  const p=await fetch(`data/panels/${idx.panels[id]}.json?v=`+Date.now()).then(r=>r.json());
  panelsMatch.push(JSON.stringify([...document.querySelectorAll(`#${id} span.k`)].map(s=>s.textContent.trim()))===JSON.stringify(keysOf(p.html)));
}
const h=await fetch(`data/${idx.history}?v=`+Date.now()).then(r=>r.json());
JSON.stringify({tabs_match:document.querySelectorAll('#tabs .tab').length===idx.tabs.length,
  sections_match:panelsMatch.every(Boolean), exec_three_kpis:document.querySelectorAll('#exec .kpi').length===3,
  trend_rendered:(h.series||[]).length<2||!!document.querySelector('#trend .trend'),
  header_loaded:!document.getElementById('meta').innerText.includes('Không nạp được'),
  no_source_links:!document.querySelector('a[href*="sharepoint"],a[href*="1drv"],a[href*="/personal/"]')})
```
All of them must be true.

## Adversary

- **A stranger on the public page** (public on purpose, README "Confidentiality"). `private_not_served`: README, CLAUDE.md, REVIEW.md, the heartbeat, the four `tools/` scripts, this protocol, one `work/` file found at run time, `.github/scripts/freshness.py` and `.pages-allow` all exist on `main` and answer 404 live. `robots_disallow_all` keeps search engines out. `no_personal_traces` (storage links, email addresses, and bare handles written as "name@") and `no_forbidden_words` keep people off every served file, live and on `main`: until 01/10 the page named the run account and three DB Group mailboxes (#14). Matches are reported by count and file, never by value.
- **A refresh that breaks the HTML** (a stray `</div>`, 22/09) or moves a section without its "mục X" references. `validator_passes`, and in the browser `sections_match`.
- **A refresh that grows `exec`** past its contract (22/09). `exec_three_kpis`, in the file and in the page.
- **A run that loses or rewrites the trend.** The validator's append-only history check, and `trend_rendered`.
- **A routine that stopped running.** `heartbeat_fresh`. **A routine that runs but publishes nothing:** `data_fresh`.
- **A preview a generation behind** (it once held CSS fixes the repo lacked, 23/09). Step 4.

## Sanctioned substitutes

- The forbidden word list is passed on the command line, so it can change without a PR and the repo never names a person. This proves served files and tracked data don't contain those words; it cannot catch a name nobody has listed.
- The preview cannot be fetched by a script, so step 4 is done by the runner with `Artifact list` and `Artifact read`.

## Evidence

- The JSON from step 1 and the JSON from step 2.
- Screenshots (`save_to_disk: true`): each of the three tabs.
- For step 4: the preview's file list and the hashes read.

## Not covered

- Whether the figures are right against the Drive trackers. Revenue here is budget rate × NLA, a ceiling (README); the cash-gap card shows "?" until accounting supplies collected figures.
- A person's name typed as plain words in a panel (not an address or a listed handle). Read the timeline by eye if in doubt.
- "còn N ngày" values: computed from the run date by the routine, not re-derived here.
- Git history still holds the names removed on 01/10 (#14).

## Traps

- Pages answers `cache-control: max-age=600` (10 minutes; response header seen with `curl -sI` on the sister dashboards, 01/10). A `served_equals_main` failure straight after a merge is the cache: wait for the Pages run, then re-run. Each request retries once on a network error or a 5xx.
- The page loads its panels in parallel after the first paint; step 2 waits 3 s before reading them.
- `index.html` falls back to the published data only when the relative `data/` fetch fails (a `file://` open). Over a local http serve it reads the branch's data; opened as a file it silently shows live data.
- `no_forbidden_words` can fail inside a timeline line the routine wrote. Do not edit around it silently: fix the line in a PR and check the README rule held.
- Weekly-run commit titles vary and some PR merges predate squash titles, so step 4 takes the last `index.json` commit that is not a `(#N)` PR merge.
