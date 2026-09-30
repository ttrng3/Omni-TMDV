# Intent — Pages workflow template v2 (accepted)

Status: accepted by Ty on 30/09 (he approved the template spec and shipped claude-config PR 9).

Bring this repo's Pages workflow to the shared template so coverage checks the
whole tracked tree, symlinks are refused, and write permissions live only on the
deploy job. TMDV is rollout 1 of 9 and goes alone, to prove the per-job
permissions on a real deploy before the other 8 move.
