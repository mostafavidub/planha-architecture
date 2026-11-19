"""Read-only reviewed source snapshot; no imports of inventoried code or dispatch.
Manifest and four explicit self paths are a reviewed trust root, not self-hash closure.
Unknown selected surfaces require review, never automatic registration.
"""
import ast, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SPEC='specs/current_entry_inventory_x05.json'
OLD='specs/current_entry_inventory_x03.json'
OLD_BLOB='4d3a5b85bbcfa742ad9219e8190e00f81dfdb070'
BASE='9775a6a544c352137f45d24e258874a754de59ae'
REVIEWED='017c47c806da39174daa03ce71a8fbc576b5d316'
SELF={'app/local_integration/current_entry_inventory_x05.py',
 'tests/r4/test_current_entry_inventory_x05.py',SPEC,
 '.github/workflows/r4-source-inventory-x05.yml'}
def require(ok,code):
 if not ok:raise ValueError(code)
def blob(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()
def read(root,path):
 p=root/path
 try:return str(p.readlink()).encode() if p.is_symlink() else p.read_bytes()
 except OSError:raise ValueError('MISSING_REVIEWED_PATH') from None
def decode(data):
 def unique(pairs):
  out={}
  for k,v in pairs:
   require(k not in out,'DUPLICATE_MANIFEST_KEY');out[k]=v
  return out
 return json.loads(data,object_pairs_hook=unique)
def surfaces(root):
 return {p.relative_to(root).as_posix() for p in (root/'app/local_integration').glob('*.py')}|{p.relative_to(root).as_posix() for p in (root/'.github/workflows').glob('*') if p.is_file() or p.is_symlink()}
def reconcile(m,old):
 require(m['schema']=='CURRENT_SOURCE_INVENTORY_X05_V1' and m['base_ref']==BASE and m['reviewed_ref']==REVIEWED,'WRONG_SNAPSHOT_VERSION')
 require(m['old_manifest_path']==OLD and m['old_manifest_blob']==OLD_BLOB,'OLD_MANIFEST_BINDING')
 require(m['new_dispatch'] is False and m['self_hash_closure'] is False,'NO_NEW_AUTHORITY')
 require(set(m['self_paths_unhashed'])==SELF and len(m['self_paths_unhashed'])==4,'SELF_SCOPE_CHANGED')
 files={p:dict(r) for p,r in old['files'].items()}
 tops=set(old['top_level_paths'])
 additions=[]
 changes=[]
 for phase,counts in [('old_to_base',(2,7)),('base_to_current',(2,2))]:
  d=m[phase]
  require(len(d['changed'])==counts[0] and len(d['added'])==counts[1] and d['missing']==[],'DIFF_CARDINALITY')
  for row in d['changed']:
   p=row['path'];before=row['old'] if phase=='old_to_base' else row['base']
   after=row['base'] if phase=='old_to_base' else row['current']
   require(p in files and files[p]['blob']==before and p not in changes,'DIFF_SOURCE_CHAIN')
   files[p]['blob']=after;changes.append(p)
  for row in d['added']:
   p=row['path']
   require(p not in files and p not in tops,'DIFF_ADDITION_DUPLICATE')
   additions.append(row);tops.add(p)
   files[p]={'blob':row['blob']}
 reviewed=m['reviewed_additions']
 require(len(reviewed)==9 and len({r['path'] for r in reviewed})==9,'REVIEWED_ADDITIONS_REQUIRED')
 rm={r['path']:r for r in reviewed}
 require(set(rm)=={r['path'] for r in additions},'REVIEWED_SET_MISMATCH')
 for row in additions:
  r=rm[row['path']]
  expected='REVIEWED_WORKFLOW_DECLARATION_NO_NEW_DISPATCH' if row['path'].endswith('.yml') else 'REVIEWED_STUDY_SOURCE_NO_NEW_DISPATCH'
  require(r['blob']==row['blob'] and r['new_dispatch'] is False and r['classification']==expected,'ADDITION_CLASSIFICATION')
  require(r['task'] in {'R4-2.11','R4-3.11','R4-3.10','R4-3.01','R4-3.02','R4-X.04'} and len(r['source_change_commit'])==40,'ADDITION_PROVENANCE')
  files[row['path']]['classification']=expected
 require(files==m['files'] and len(files)==243,'SNAPSHOT_RECONCILIATION_FAILED')
 require(tops==set(m['top_level_paths']) and len(tops)==len(m['top_level_paths']),'TOP_LEVEL_SCOPE_CHANGED')
 require(set(changes)==set(m['changed_source_tasks']),'CHANGED_PROVENANCE_REQUIRED')
 return files,tops
def scan(root=ROOT):
 root=Path(root)
 specbytes=read(root,SPEC);oldbytes=read(root,OLD)
 require(blob(oldbytes)==OLD_BLOB,'OLD_MANIFEST_CHANGED')
 m=decode(specbytes);old=decode(oldbytes);files,tops=reconcile(m,old)
 for p in SELF:require((root/p).is_file() and not (root/p).is_symlink(),'SELF_PATH_REQUIRED')
 require(surfaces(root)==tops|{p for p in SELF if p.startswith('app/local_integration/') or p.startswith('.github/workflows/')},'UNREVIEWED_SURFACE')
 rows=[]
 for path,r in sorted(files.items()):
  data=read(root,path)
  require(blob(data)==r['blob'],'STALE_SNAPSHOT_SOURCE_CHANGED')
  if path.endswith('.py') and not (root/path).is_symlink():ast.parse(data,filename=path)
  rows.append({'path':path,'blob':r['blob'],'classification':r['classification']})
 require(read(root,SPEC)==specbytes and read(root,OLD)==oldbytes,'MANIFEST_CHANGED_DURING_READ')
 require(all(blob(read(root,p))==r['blob'] for p,r in files.items()),'SOURCE_CHANGED_DURING_READ')
 require(surfaces(root)==tops|{p for p in SELF if p.startswith('app/local_integration/') or p.startswith('.github/workflows/')},'UNREVIEWED_SURFACE')
 return {'schema':'CURRENT_SOURCE_INVENTORY_X05_RESULT_V1','state':'CURRENT_SOURCE_INVENTORY_RECONCILED_VERSIONED_SCOPED',
 'file_count':len(rows),'changed_count':4,'added_count':9,'missing_count':0,
 'inventory_digest':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),
 'manifest_digest':hashlib.sha256(specbytes).hexdigest(),'new_dispatch':False,
 'self_hash_closure':False,'literal_legacy_isolation':False,
 'old_x03_failure_retained':True,'qualification_allowed':False,
 'scope':'Selected records and top-level surface presence; not all repository callers, runtime behavior, permissions, or readiness'}
if __name__=='__main__':print(json.dumps(scan(),sort_keys=True))
