# Intent: TMDV's README says "one address, one preview", so the routine stops skipping its mirror step

**Status:** accepted 2026-09-28 (revised after reading the 27/09 run log and re-accepted by Ty; the first version rested on a wrong fact and is in git history at 053845b)
**Source:** chat, 2026-09-28 (Ty: "rewrite TMDV's README to 'one address, one preview', like Omni-Audit. The 26/09 rule replaces 23/09."), plus the TMDV routine's run log of 2026-09-27

**Problem.** `README.md` "One surface, on purpose" (lines 310–321) still carries the 23/09 rule: "there is no claude.ai artifact copy … Do not recreate one." Ty's 26/09 ruling (the artifact mirror contract) replaced it: every Pages pipeline has exactly one Cowork preview, the preview must exist, and its URL is never written anywhere.

The stale section isn't only misleading. **It is what stops the preview being refreshed.** The routine's prompt has a mirror step (STEP 9), and it says "if anything disagrees with the README, THAT FILE WINS". On 2026-09-27 the routine reached STEP 9 and skipped it on purpose. Its report, translated: "Artifact: not done. README.md … says Ty decided on 23/09 Pages is the only surface … 'Do not recreate one.' If the 23/09 decision was reversed, README must be fixed before step 9 is turned back on." So the preview (titled *TMDV Điều hành*) has stayed at 22/09 while the page moved on (the collector marks it "behind").

The same log shows a **second, separate cause**: the session had no Artifact tool. The tool search for "artifact" found nothing, although the routine config lists it. Fixing the README removes the reason the routine skipped; it doesn't guarantee the tool loads.

(The first version of this intent said "nothing refreshes the preview". That was wrong: the step exists and was deliberately skipped because of this README.)

**Outcome.**
- The section is renamed "One address, one preview" and states the 26/09 rule in Omni-Audit's terms. The Pages URL is the only link. The preview exists, is refreshed as the routine's last step, must never be deleted, and its URL is never written in this repo, a Drive doc or a run report.
- It says explicitly that the 23/09 "no artifact" rule is replaced, so the next run doesn't read the two as a conflict.
- The `build-fragment.py` line says what it's for: deriving the preview's fragment, used by STEP 9 when the renderer changes.
- Checked on the next run (Sun 4 Oct): the routine's report no longer says the mirror was skipped because of the README.

**Who and what is affected.** `README.md`, one section; through it, the TMDV routine's STEP 9 behaviour. No code, no Pages change (`README.md` isn't served).

**Constraints.** No preview URL or id in the repo (public). No personal data by value. The PR goes to Ty to ship.

**Decision (Ty, 2026-09-28).** Yes: the missing Artifact tool is its own intent, `work/260928-tmdv-artifact-tool/`. It replaces the "add a mirror step" intent, since the step exists.

**Open questions.** None.
