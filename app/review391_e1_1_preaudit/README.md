# e1-1 Linux preaudit

This source tree is a separate, invalid-input-only evaluation of the working frontend patch. Historical v390 source, freeze, and actual evidence are immutable inputs and are not rewritten.

The new staging directory is an exact copy of `staging390_form` except for the authorized `index.html` and a minimally extended `guard390.py`. The guard first authenticates the historical v390 freeze by its fixed SHA-256, requires the new manifest to contain the complete historical keyset with identical pins, then validates every current pinned file. The new manifest additionally pins every file in the new staging directory, including the new guard and patched frontend, plus the retained patch provenance files.

Only invalid requests may be sent to the real loopback server. Valid input, accepted responses, 409/500 responses, network ambiguity, and guard failures are exercised only by an explicitly nongenerative synthetic harness. No constructor, solver, reviewer, or semantic phase is authorized by this operation.
