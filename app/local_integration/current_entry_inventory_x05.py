"""Read-only reviewed source snapshot; no imports of inventoried code or dispatch.
Manifest and four explicit self paths are a reviewed trust root, not self-hash closure.
Unknown selected surfaces require review, never automatic registration.
"""
import ast, hashlib, json, re
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
PROVENANCE={"app/local_integration/report_lifecycle112.py":{"task":"R4-4.08","commit":"c930f72f5b354892df0adf86b60b9820250df324"},"app/local_integration/request_trace109.py":{"task":"R4-4.08","commit":"c930f72f5b354892df0adf86b60b9820250df324"},"app/local_integration/public_wln_server.py":{"task":"R4-X.04","commit":"194b765edd44aa2eb0b48482a0177d61ef9de262"},"app/local_integration/current_entry_launch_x03.py":{"task":"R4-X.04","commit":"194b765edd44aa2eb0b48482a0177d61ef9de262"},".github/workflows/r4-current-matrix211.yml":{"task":"R4-2.11","commit":"4ae9b597e33b4f2b65c5a5aa5a8215a0ff272b86"},".github/workflows/r4-disclosure311.yml":{"task":"R4-3.11","commit":"8061ece6f2d57314aad55bfa4b97f15a6d65e05d"},".github/workflows/r4-public-navigation310.yml":{"task":"R4-3.10","commit":"7af2c91aa789ab364208979f875a383b6d8bf38d"},".github/workflows/r4-semantic-descriptor301.yml":{"task":"R4-3.01","commit":"d7ef1537702e50f918d187ab40b7ddfdf6d2064e"},".github/workflows/r4-structural-pair302.yml":{"task":"R4-3.02","commit":"8f4dc80417512a167acd16feef13ace38d51561d"},"app/local_integration/current_matrix211.py":{"task":"R4-2.11","commit":"24adb4f8e1dec32107155d9e88e2c0742c62ffc5"},"app/local_integration/structural_pair302.py":{"task":"R4-3.02","commit":"fcf6f6ea0bb7625536c35ee5351daab18d49491e"},".github/workflows/r4-http-withholding-x04.yml":{"task":"R4-X.04","commit":"017c47c806da39174daa03ce71a8fbc576b5d316"},"app/local_integration/http_withholding_x04.py":{"task":"R4-X.04","commit":"194b765edd44aa2eb0b48482a0177d61ef9de262"}}
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
  require(r['task'] in {'R4-2.11','R4-3.11','R4-3.10','R4-3.01','R4-3.02','R4-X.04'} and type(r['source_change_commit']) is str and re.fullmatch('[0-9a-f]{40}',r['source_change_commit']) is not None,'ADDITION_PROVENANCE')
  require({'task':r['task'],'commit':r['source_change_commit']}==PROVENANCE[row['path']],'ADDITION_PROVENANCE_MISMATCH')
  files[row['path']]['classification']=expected
 require(files==m['files'] and len(files)==243,'SNAPSHOT_RECONCILIATION_FAILED')
 require(tops==set(m['top_level_paths']) and len(tops)==len(m['top_level_paths']),'TOP_LEVEL_SCOPE_CHANGED')
 require(set(changes)==set(m['changed_source_tasks']),'CHANGED_PROVENANCE_REQUIRED')
 require(m['changed_source_tasks']=={p:PROVENANCE[p] for p in changes},'CHANGED_PROVENANCE_MISMATCH')
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
