"""Import-only origin/dependency audit. No configure, model or semantic run."""
import sys,json,ast,importlib.util
from pathlib import Path
W=Path.cwd();ROOT=W/'reconstruction357';FORM=ROOT/'staging385_form';SEM=ROOT/'staging385_current_semantics'
sys.path[:0]=[str(FORM),str(SEM),str(ROOT/'semantic_rules357'),str(ROOT/'staging368_semantic_bridge')]
import contract385,integration385,joint_semantics385,joint_composition385
from adapters385 import audit_loaded
origins=audit_loaded()
roots=[FORM/'contract385.py',FORM/'joint_semantics385.py',FORM/'joint_composition385.py',SEM/'integration385.py',SEM/'extended385.py',SEM/'qualification385.py']
queue=roots[:];seen=set();edges=[];external=set();missing=[];search=[Path(x)for x in sys.path if x]
while queue:
 p=queue.pop()
 if p in seen:continue
 seen.add(p)
 for n in ast.walk(ast.parse(p.read_text())):
  names=[a.name for a in n.names]if isinstance(n,ast.Import)else[n.module]if isinstance(n,ast.ImportFrom)and n.module else[]
  for name in names:
   top=name.split('.')[0];local=next((q/(top+'.py')for q in search if(q/(top+'.py')).is_file()and(q/(top+'.py')).resolve().is_relative_to(W)),None)
   if local:
    local=local.resolve();edges.append({'source':str(p.relative_to(W)),'line':n.lineno,'module':name,'path':str(local.relative_to(W))});queue.append(local)
   else:
    try:spec=importlib.util.find_spec(top)
    except Exception:spec=None
    if spec is None:missing.append({'source':str(p.relative_to(W)),'line':n.lineno,'module':name})
    else:external.add(top)
print(json.dumps({'no_model_or_semantic_execution':True,'module_origins':origins,'local_modules':len(seen),'edges':edges,'external_roots':sorted(external),'unresolved_static_imports':missing},indent=2))
# Context-dependent source constructors are imported in isolated phase paths;
# unresolved static names are disclosed, not automatically treated as execution failures.
