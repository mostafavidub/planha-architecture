# e1-1 installable invalid-input check

This stage extends the already audited e1-1 source without rewriting it. The current guard authenticates both the historical v390 freeze and the immediate e1-1 parent freeze, requires the complete parent keyset with identical pins, and validates every current file.

`launch_invalid_only392.py` is the only current entrypoint for this operation. It requires Linux, Python Playwright, Chromium, and psutil; requires a new non-existing evidence directory; authenticates the supplied freeze SHA; launches the unchanged real `server390.py`; runs only the fixed invalid-input browser runner; verifies that `one_shot_used` remains false and that no `runs` directory appears; then requests safe shutdown and verifies process/listener closure.

The copied `launch390.py` is historical full-generation machinery and MUST NOT be used for e1-1. It remains byte-identical only for provenance. This operation does not authorize valid POSTs, constructors, solvers, reviewers, semantic evaluation, deployment, or later roadmap steps.

The Linux entrypoint depends on psutil and the managed Chromium/Playwright environment. The previously described Mac environment lacks psutil and is not an authorized execution target for this check; do not install dependencies or alter security settings there.
