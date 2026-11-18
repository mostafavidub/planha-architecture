"""Build only a source/evidence freeze, never execute any model or reviewer."""
import json,hashlib,difflib
from pathlib import Path
W=Path.cwd();O=W/'review385_preaudit';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=W/'review386_preaudit/source_freeze.json';files=json.loads(prior.read_text())['files'];assert all((W/n).is_file()and sha(W/n)==v for n,v in files.items())
(O/'prior386_unchanged.json').write_text(json.dumps({'verified':True,'pins':len(files),'sha256':sha(prior)},indent=2));files[str(prior.relative_to(W))]=sha(prior)
for folder in ('reconstruction357/staging379_form','reconstruction357/staging385_form','reconstruction357/staging385_current_semantics'):
 for p in(W/folder).rglob('*'):
  if p.is_file()and '__pycache__'not in p.parts and p.suffix not in('.pyc','.pyo'):files[str(p.relative_to(W))]=sha(p)
# Immutable384 proof authority, not merely a result boolean.
for name in ('result.json','supervision.json','state.json','preregistration.json','source_unchanged.json','independent_audit.json'):
 p=W/'review384_actual_v1'/name;files[str(p.relative_to(W))]=sha(p)
files['review384_preaudit/source_freeze.json']=sha(W/'review384_preaudit/source_freeze.json')
for p in(W/'review386_actual_v1').rglob('*'):
 if p.is_file()and p.suffix not in('.zip','.png','.jpg','.jpeg'):files[str(p.relative_to(W))]=sha(p)
for name in('prepare385.py','import_probe385.py'):files['review385_preaudit/'+name]=sha(O/name)
# The complete joint proof-transport registry readset must be covered, including aliases.
ref=json.loads((W/'reconstruction357/staging368_semantic_bridge/reference_registry.json').read_text())
for name,h in ref['sources'].items():
 p=(W/'reconstruction357'/name).resolve();assert p.is_relative_to(W)and sha(p)==h;files[str(p.relative_to(W))]=h
(O/'source_freeze.json').write_text(json.dumps({'schema':'TWO_CURRENT_BUILDERS385_FULL_SOURCE_EVIDENCE_FREEZE','files':files},sort_keys=True,indent=2))
lines=[]
for p in sorted((W/'reconstruction357/staging385_form').glob('*')):
 if p.suffix not in('.py','.html'):continue
 q=W/'reconstruction357/staging379_form'/p.name.replace('385','379');old=q.read_text()if q.is_file()else''
 lines+=list(difflib.unified_diff(old.splitlines(True),p.read_text().splitlines(True),fromfile=str(q.relative_to(W)),tofile=str(p.relative_to(W))))
(O/'form_exact_diff.patch').write_text(''.join(lines))
print(json.dumps({'freeze_sha256':sha(O/'source_freeze.json'),'pins':len(files),'actual_run_started':False},indent=2))
