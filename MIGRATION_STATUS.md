# Migration status: partial, not runnable-verified

## Authorization and necessity
Owner authorized only Blueprint/PRD-derived material needed to execute or continue development, excluding credentials, databases and personal data. No complete source document is being published.
- Engine Python/JS/HTML/CSS: implementation, version-linked imports, regression tests and reproducible development sources; historical versions are not automatically current approved behavior.
- rule_contract118.json: rule_contract118.py load_contract reads exact bytes, verifies SHA256 b286c31d09fd58b962e0af1a81ee0e5c79c43c17271c40580ff6ee5b7ce3a1ac and the 89-rule registry. Removing its embedded obligations breaks evaluator loading and loses named requirements.
- world_record_schema129/131/132/133/136/147.json: world_inventory125.py selects these by model family and verifies each hash before checking local/world records; 147 is also required by constructor129 and construction_replay129.
- world_record_schema125.json: retained for project_input_audit118.py pinned source integrity. Not asserted to be the currently selected schema.
- Geometric reference models/routes/instances: retained for associated model validation and regression development under prior explicit reference-data approval.
- test_privacy115_baseline_result.json: excluded from this transfer; no Python consumer was found in the engine tree. Historical results are not needed merely to publish more files.

## Verified transfer scope
479 selected engine/reference files plus 42 adapter/staged files, 3 root policy/readme/ignore files and this report: 525 files.
Local source was read without modification. Writes took place only through GitHub connector.
Strong credential markers and local /Users/ paths were checked for the selected engine files; this is not a guarantee that every possible sensitive pattern was detected. Databases, credentials, virtual environments and known personal-machine deployment helpers were excluded.

## Open dependencies, not an execution claim
- frontend staging400 and its guard400 freeze-chain are not yet imported.
- Adapter root discovery expects manifests/WORKTREE_STATE.json; root aliases are not yet reconstructed.
- Historical guard closure: 12,991 references, 8,178 distinct source paths, approximately 542 MB. This inventory is not a claim those files are all necessary to the minimal future runtime, and they have not all been migrated.
- Some tests require local evidence fixtures not in this repository.
- No original 588 package was recovered.
- Python/JS test successes documented in README are historical Mac results, not tests of this GitHub commit.
- Historical engine contracts retain 5..45 in places for source integrity. The current adapter validates 5..25, but direct legacy entrypoints have NOT been certified for this new range. Do not expose these legacy entrypoints.
- No deployment, service restart or DB change was performed.
