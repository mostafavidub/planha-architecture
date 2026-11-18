"""Extract literal source-kernel data readsets without executing the bridge."""
import ast,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def kernel_readset():
 p=ROOT/'staging351_collision_lineage/fresh_bridge.py';tree=ast.parse(p.read_text());tables={}
 for n in tree.body:
  if isinstance(n,ast.Assign):
   for t in n.targets:
    if isinstance(t,ast.Name)and t.id in ('GROUP285_SOURCE_PINS','NETWORK288_PINS'):tables[t.id]=ast.literal_eval(n.value)
  if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call):
   call=n.value
   if isinstance(call.func,ast.Attribute)and isinstance(call.func.value,ast.Name)and call.func.value.id=='GROUP285_SOURCE_PINS'and call.func.attr=='update':tables['GROUP285_SOURCE_PINS'].update(ast.literal_eval(call.args[0]))
 if set(tables)!= {'GROUP285_SOURCE_PINS','NETWORK288_PINS'}:raise ValueError('KERNEL_LITERAL_INVENTORY')
 files={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()}
 for table,items in tables.items():
  for name,h in items.items():
   f=(ROOT/'planha_general150_runtime_work'/name)if table=='GROUP285_SOURCE_PINS'else ROOT/name
   if hashlib.sha256(f.read_bytes()).hexdigest()!=h:raise ValueError('DYNAMIC_READSET_DRIFT:'+name)
   files[str(f.relative_to(ROOT))]=h
 return files
