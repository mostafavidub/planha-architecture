"""Only filesystem/hash/manifest checks; no application imports or model run."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parents[2];S=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=W/'review376_preaudit/source_freeze.json';f=json.loads(freeze.read_text())['files']
for n,h in f.items():assert sha(W/n)==h,n
inv=json.loads((S/'runtime_inventory376.json').read_text())['files'];rt=W/'reconstruction357/staging369_current_source_validation/runtime'
actual={str(p.relative_to(W))for p in rt.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.suffix not in('.pyc','.pyo')};assert actual==set(inv)
for n,h in inv.items():assert sha(W/n)==h,n
assets=json.loads((S/'runtime_assets376.json').read_text())
for row in assets['legitimate_original_byte_provenance']:assert sha(W/row['newly_pinned_runtime_path'])==sha(W/row['original_frozen_source'])==row['sha256']
old=W/'reconstruction357/staging375_same_run_form';new=W/'reconstruction357/staging376_same_run_form'
for p in old.iterdir():
 if p.is_file():assert(new/p.name.replace('375','376')).read_text().replace('376','375')==p.read_text(),p.name
print(json.dumps({'all_frozen_references_verified':len(f),'all_runtime_files_including_every_suffix':len(inv),'added_assets_verified':len(assets['new_assets']),'harness_version_only_transform':True,'execution_performed':False}))
