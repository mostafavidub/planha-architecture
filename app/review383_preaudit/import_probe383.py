"""Fresh-process import-only probe: no build/replay/checker execution."""
import ast,json,sys,importlib,hashlib
from pathlib import Path
W=Path.cwd();H=W/'reconstruction357/staging383_rank2';sys.path.insert(0,str(H))
import source383
import family378
FAMILY=H.parent/'staging378_finite_portals'
roots=[H/'source383.py',FAMILY/'constructor378.py',FAMILY/'core378.py',FAMILY/'family378.py',H.parent/'staging365_balanced_portals/assemble365.py',H.parent/'staging365_balanced_portals/selector365.py',H.parent/'staging365_balanced_portals/operation_domain365.py']
mode=sys.argv[1]if len(sys.argv)>1 else'constructor'
if mode=='reviewer':
 import evaluate383
 evaluate383.module_origin_audit()
 import checker114
 roots=[H/'evaluate383.py',H/'source383.py',H/'runtime/checker114.py',H/'runtime/named_checks118.py',H/'runtime/source_registry365.py',H/'runtime/source_identity365.py']
names=set();rows=[]
for p in roots:
 for n in ast.walk(ast.parse(p.read_text())):
  if isinstance(n,ast.Import):names.update(a.name for a in n.names)
  elif isinstance(n,ast.ImportFrom)and n.module:names.add(n.module)
for name in sorted(names):
 mod=importlib.import_module(name);path=getattr(mod,'__file__',None)
 rows.append({'module':name,'path':path,'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()if path and Path(path).is_file()else None})
# Closure discovery includes delayed imports recursively, without executing them.
# Resolve local modules by the exact source-import search order; external modules
# receive an explicit separate availability inventory, not source equivalence.
search=[Path(p)for p in sys.path if p];queue=list(roots);seen=set();edges=[];missing=[];external=set()
while queue:
 p=queue.pop()
 if p in seen:continue
 seen.add(p)
 for node in ast.walk(ast.parse(p.read_text())):
  imported=[a.name for a in node.names]if isinstance(node,ast.Import)else[node.module]if isinstance(node,ast.ImportFrom)and node.module else[]
  for name in imported:
   top=name.split('.')[0];local=next((d/(top+'.py')for d in search if (d/(top+'.py')).is_file()and (d/(top+'.py')).resolve().is_relative_to(W)),None)
   if local:
    local=local.resolve();edges.append({'from':str(p.relative_to(W)),'line':node.lineno,'module':name,'resolved':str(local.relative_to(W))});queue.append(local)
   else:
    try:spec=importlib.util.find_spec(top)
    except Exception:spec=None
    if spec is None:missing.append({'from':str(p.relative_to(W)),'line':node.lineno,'module':name})
    else:external.add(top)
print(json.dumps({'mode':mode,'import_only':True,'model_build_executed':False,'fresh_review_executed':False,'direct_imports':rows,'static_local_modules':len(seen),'static_edges':edges,'external_import_roots':sorted(external),'missing':missing},indent=2))
if missing:raise SystemExit(1)
