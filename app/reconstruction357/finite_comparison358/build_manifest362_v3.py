"""Freeze v3 plus exact dynamic readsets and approved COMMON source package."""
from build_transitive_manifest359 import ROOT,HERE,closure,json,hashlib,Path
from dynamic_readset362 import kernel_readset
base=json.loads((HERE/'q04_manifest362_v2b.json').read_text());files=set()
for name,h in base['files'].items():
 p=ROOT/name
 if hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise ValueError('PREVIOUS_V2B_DEPENDENCY_CHANGED:'+name)
 files.add(p)
more,edges=closure(['finite_comparison358/q04_closure362_v3.py']);files|=more
freeze=ROOT/'semantic_rules357/common_role_closure362_v3_freeze.json';f=json.loads(freeze.read_text());files.add(freeze)
for name,h in f['files'].items():
 p=freeze.parent/name
 if hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise ValueError('COMMON_FREEZE_CHANGED:'+name)
 files.add(p)
more,extra=closure([str(p.relative_to(ROOT))for p in files if p.suffix=='.py']);files|=more;edges.update(extra)
for name,h in kernel_readset().items():files.add(ROOT/name)
m={'schema':'Q04_362_V3_FIXED_TRANSITIVE_AND_DYNAMIC_MANIFEST','files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)},'import_edges':edges,'common_freeze_sha256':hashlib.sha256(freeze.read_bytes()).hexdigest(),'scope':'Current source362 bound finite engineering reassessment; no live authority or global optimum. The outer final registry must pin q04_runner362_v3 itself, whose embedded SHA pins this manifest.'}
p=HERE/'q04_manifest362_v3.json';p.write_text(json.dumps(m,indent=2));print(hashlib.sha256(p.read_bytes()).hexdigest(),len(files))
