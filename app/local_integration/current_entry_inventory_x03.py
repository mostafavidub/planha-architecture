"""Read-only AST/CLI/workflow inventory. No imports, dispatch or code execution.
Static visibility only: dynamic targets remain unresolved, not approved.
"""
import ast,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'specs/current_entry_inventory_x03.json'
def blob(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
def read_source(path):
 p=ROOT/path
 return str(p.readlink()).encode()if p.is_symlink()else p.read_bytes()
def scan(manifest_path=MANIFEST):
 manifest_bytes=manifest_path.read_bytes()
 manifest=json.loads(manifest_bytes);rows=[];dynamic=[]
 for path,record in manifest['files'].items():
  data=read_source(path)
  if blob(data)!=record['blob']:raise ValueError('INVENTORY_SOURCE_CHANGED')
  row={'path':path,'blob':record['blob'],'classification':record['classification']}
  if (ROOT/path).is_symlink():
   row['historical_target']=data.decode();row['current_launcher_registered']=False
  elif path.endswith('.py'):
   tree=ast.parse(data,filename=path)
   row['functions']=sorted({n.name for n in ast.walk(tree)if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))})
   row['imports']=sorted({(n.module or '')for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)}|{a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names})
   row['calls']=sorted({ast.unparse(n.func)for n in ast.walk(tree)if isinstance(n,ast.Call)})
   row['cli_main']=any(isinstance(n,ast.If)and '__name__'in ast.unparse(n.test)and '__main__'in ast.unparse(n.test)for n in tree.body)
   hits=[x for x in row['calls']if x in ('eval','exec','__import__','getattr','runpy.run_path','importlib.import_module')]
   if hits:dynamic.append({'path':path,'targets':hits,'status':'STATIC_TARGET_NOT_PROVEN_NO_GENERIC_CURRENT_DISPATCH'})
  else:
   text=data.decode();row['referenced_current_files']=sorted(p for p in manifest['python_names']if p in text)
   row['upload_action_declared']='actions/upload-artifact' in text
  rows.append(row)
 # New top-level integration modules/workflows require a new reviewed inventory.
 observed={p.relative_to(ROOT).as_posix()for p in (ROOT/'app/local_integration').glob('*.py')}
 observed|={p.relative_to(ROOT).as_posix()for p in (ROOT/'.github/workflows').glob('*')if p.is_file() or p.is_symlink()}
 expected=set(manifest['top_level_paths'])|set(manifest['inventory_self_paths'])
 if observed!=expected:raise ValueError('UNREGISTERED_CURRENT_SURFACE_REVIEW_REQUIRED')
 if manifest_path.read_bytes()!=manifest_bytes:raise ValueError('INVENTORY_MANIFEST_CHANGED_DURING_READ')
 before=manifest['files']
 if any(blob(read_source(p))!=r['blob']for p,r in before.items()):raise ValueError('INVENTORY_CHANGED_DURING_READ')
 return {'schema':'CURRENT_ENTRY_INVENTORY_X03_V1','rows':rows,'dynamic_unresolved':dynamic,
  'scope':'Pinned selected integration Python plus all workflows at this revision; not every repository callable or runtime dynamic target',
  'registered_dispatch_is_not_python_isolation':True,'literal_legacy_import_isolation':'NOT_IMPLEMENTED',
  'source_manifest_digest':hashlib.sha256(manifest_bytes).hexdigest()}
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--current', action='store_true')
 args=parser.parse_args()
 out=scan(ROOT/'specs/current_entry_inventory_x03_current.json') if args.current else scan()
 print(json.dumps({'schema':out['schema'],'file_count':len(out['rows']),'dynamic_unresolved_count':len(out['dynamic_unresolved']),
  'inventory_digest':hashlib.sha256(json.dumps(out,sort_keys=True).encode()).hexdigest(),'literal_legacy_import_isolation':'NOT_IMPLEMENTED'}))
