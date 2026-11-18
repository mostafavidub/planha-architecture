"""Static local import closure plus explicit artifact/data roots. Outer must pin.
Includes source actually imported by Q04 even when intrinsic eligibility does not.
"""
from pathlib import Path
import ast,json,hashlib
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
SEARCH=[HERE,ROOT/'semantic_rules357',ROOT/'planha_general150_runtime_work']
def closure(start):
 todo=[ROOT/p for p in start];seen=set();edges={}
 while todo:
  p=todo.pop().resolve()
  if p in seen:continue
  seen.add(p)
  if p.suffix!='.py':continue
  mods=set()
  for n in ast.walk(ast.parse(p.read_text())):
   if isinstance(n,ast.Import):mods.update(a.name.split('.')[0]for a in n.names)
   elif isinstance(n,ast.ImportFrom)and n.module:mods.add(n.module.split('.')[0])
  children=[]
  for mod in mods:
   candidates=[d/(mod+'.py')for d in [p.parent]+SEARCH];unique=[]
   for c in candidates:
    if c.exists()and c.resolve()not in unique:unique.append(c.resolve())
   children+=unique
  edges[str(p.relative_to(ROOT))]=[str(c.relative_to(ROOT))for c in sorted(set(children))];todo+=children
 return seen,edges
if __name__=='__main__':
 roots=['finite_comparison358/q04_closure359.py','finite_comparison358/service_closure359.py','finite_comparison358/branch_registry359.py']
 files,edges=closure(roots)
 # Pin dynamic-loader files and named JSON method registries; their embedded
 # source hashes remain independently checked by existing bound readset gates.
 for pattern in ['eligibility_intrinsic359_pins.json','group_readsets359_pins.json','group_readsets358_pins.json','method_registry_source359.json','method_registry_source358.json']:
  p=ROOT/'semantic_rules357'/pattern;files.add(p.resolve());j=json.loads(p.read_text())
  for name in j.get('files',{}):
   f=p.parent/name
   if f.exists():
    more,ed=closure([str(f.relative_to(ROOT))]);files|=more;edges.update(ed)
 for name in ['bound_comparison_actual358.json','core_branch_bound358.json','branch_registry_actual359_v2.json']:files.add((HERE/name).resolve())
 files.add((ROOT/'staging358_core_branch/actual_full_band358.json').resolve());files.add((ROOT/'staging274_evaluator_transport_fix/quality_contract.json').resolve())
 m={'schema':'Q04_SERVICE359_TRANSITIVE_IMPORT_AND_DYNAMIC_PIN_CLOSURE','roots':roots,'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(files)},'import_edges':edges,'instruction':'Outer fixed runner must pin this manifest and verify every file before execution. JSON manifest is not standalone authority. Intrinsic eligibility pin edit authorization does not waive Q04 actual wall_purpose dependency.','live_authority':False}
 (HERE/'transitive_manifest359.json').write_text(json.dumps(m,indent=2));print(len(files),'files','wall_purpose pinned:', 'semantic_rules357/wall_purpose.py'in m['files'])
