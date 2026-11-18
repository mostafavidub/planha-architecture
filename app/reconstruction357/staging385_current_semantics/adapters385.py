"""Explicit current adapters with frozen origin checks, never live monkeypatch."""
import importlib,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;SEM=HERE.parent/'semantic_rules357';W=HERE.parents[1]
MAP={'group_readsets365_v2':'groups385','living_closure365':'living_closure385','guest_closure365':'guest_closure385','kitchen_closure365':'kitchen_closure385','closure_room_program365':'room385','primitive_review365':'primitive385'}
def require_origin(module,name):
 expected=(HERE if name.endswith('385')else SEM)/(name+'.py')
 actual=Path(getattr(module,'__file__','')).resolve()
 if actual!=expected.resolve()or not expected.is_file():raise ValueError('SEMANTIC_MODULE_ORIGIN:'+name)
 files=json.loads((W/'review385_preaudit/source_freeze.json').read_text())['files'];key=str(expected.relative_to(W))
 if hashlib.sha256(expected.read_bytes()).hexdigest()!=files.get(key):raise ValueError('SEMANTIC_MODULE_HASH:'+name)
 return module

def load(name):
 target=MAP.get(name,name)
 # Closed local module profile: no fallback to external modules or arbitrary paths.
 expected=(HERE if target.endswith('385')else SEM)/(target+'.py')
 if not expected.is_file():raise ValueError('UNREGISTERED_SEMANTIC_MODULE:'+target)
 return require_origin(importlib.import_module(target),target)

def audit_loaded():
 rows=[]
 for name,module in list(sys.modules.items()):
  if '.'in name:continue
  if (HERE/(name+'.py')).is_file()or(SEM/(name+'.py')).is_file():
   require_origin(module,name);rows.append(name)
 return sorted(rows)
