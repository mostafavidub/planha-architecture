"""Freeze live source only; no current semantic computation."""
import json,hashlib,os,difflib,re
from pathlib import Path
W=Path(__file__).resolve().parent.parent;O=W/'review390_preaudit';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();base=W/'review387_preaudit/source_freeze.json';files=json.loads(base.read_text())['files'];assert all(sha(W/k)==h for k,h in files.items());files[str(base.relative_to(W))]=sha(base)
for folder in ('reconstruction357/staging390_form','reconstruction357/staging390_current_semantics'):
 for p in(W/folder).rglob('*'):
  if p.is_file()and '__pycache__'not in p.parts and p.suffix not in('.pyc','.pyo'):files[str(p.relative_to(W))]=sha(p)
for n in ('frozen388.py','adapters388.py'):
 p=W/'reconstruction357/staging388_current_semantics'/n;files[str(p.relative_to(W))]=sha(p)
for p in(O/'prepare390.py',O/'package390.py'):files[str(p.relative_to(W))]=sha(p)
for n,h in list(files.items()):
 p=Path(os.path.abspath(W/n));assert p.is_relative_to(W)and p.resolve().is_relative_to(W);k=str(p.relative_to(W));assert k not in files or files[k]==h;files[k]=h
(O/'source_freeze.json').write_text(json.dumps({'schema':'LIVE390_TWO_BUILDERS_CACHED_INDEX_ONLY_DELTA','files':files},sort_keys=True,indent=2))
patch=[];hexrows=[]
for folder in ('form','current_semantics'):
 for p in sorted((W/'reconstruction357'/('staging387_'+folder)).glob('*')):
  if p.suffix not in('.py','.html'):continue
  q=W/'reconstruction357'/('staging390_'+folder)/p.name.replace('387','390')
  if not q.exists():continue
  old=p.read_text();normalized=old.replace('387','390')
  for h in set(re.findall(r'\b[0-9a-f]{64}\b',old)):normalized=normalized.replace(h.replace('387','390'),h)
  if not p.name.startswith('test'):assert set(re.findall(r'\b[0-9a-f]{64}\b',old))==set(re.findall(r'\b[0-9a-f]{64}\b',q.read_text()));hexrows.append(str(q.relative_to(W)))
  patch+=list(difflib.unified_diff(normalized.splitlines(True),q.read_text().splitlines(True),fromfile='VERSION_ONLY/'+str(p.relative_to(W)),tofile=str(q.relative_to(W))))
(O/'non_version_changes.patch').write_text(''.join(patch));(O/'hex_preservation.json').write_text(json.dumps({'verified':True,'files':hexrows},indent=2));print(json.dumps({'freeze_sha256':sha(O/'source_freeze.json'),'pins':len(files),'actual':False}))
