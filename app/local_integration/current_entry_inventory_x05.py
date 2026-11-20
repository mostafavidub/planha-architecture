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
def scan_historical(root=ROOT):
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


# P03-B reuses X05 reconciliation; immutable V1 bytes and X03 failures remain evidence.
SPEC_V2='specs/current_entry_inventory_x05_v2.json'
PREVIOUS_BLOB='5b61b827ddaca0368eebe9eb707a5ac0d26d705f'
CURRENT_REF='b6918faf97735cc4faca2caf5e3040506560a377'
SELF_V2={"app/local_integration/current_entry_inventory_x05.py","tests/r4/test_current_entry_inventory_x05.py","specs/current_entry_inventory_x05_v2.json",".github/workflows/r4-source-inventory-x05.yml"}
# Reviewed explicit per-path provenance. This is not inferred from the current filesystem.
PROVENANCE_V2=json.loads(r'''[{"path":".github/workflows/v25-criteria-catalog.yml","old_blob":"c20c692f4d4ff32f0ff6df080f2e28607e6861a0","blob":"3f3d7a1a188dd20f1c39bd9d0046f856232205bb","source_change_commit":"83b77df2a366ce503219a2c2d7970eaba9b906f7","task":"P20","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/public_wln_server.py","old_blob":"3063058f102a96d67deedee270a119a5fa6b898c","blob":"6db3de70e19b79ca1817bac550549a540a0ea552","source_change_commit":"bbf8210aa09d5faae6d7f03a7aaa800910a3afef","task":"P01","role":"CURRENT_HTTP_HANDLER","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/current_entry_launch_x03.py","old_blob":"de44992fd9f2021445decebc7b2ef9cd5fed80c6","blob":"c6a7901a3e8412806121b020de3008a4dcd4459b","source_change_commit":"652fcfbed5320ff7ae3744431a8c90fea2296cf6","task":"P01","role":"CURRENT_LAUNCHER","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/http_withholding_x04.py","old_blob":"d2237f58367ccec40699e581632883bb5d95815d","blob":"5207b00d3e30ac1a194a6605d50c26fd554f5c0d","source_change_commit":"bbf8210aa09d5faae6d7f03a7aaa800910a3afef","task":"P01","role":"HTTP_WITHHOLDING_BOUNDARY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/historical-engine-batch50.yml","old_blob":null,"blob":"1ddd2add678b9e80da02fc327fffccc2ce893f52","source_change_commit":"b21592e02e26fd9d92577ea81855b5b6b7e93e7c","task":"USER_TEST50","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/p01-stop-observation.yml","old_blob":null,"blob":"5f3fac736e04a7c184caab096a3a7ef62cad2611","source_change_commit":"906fc0bf33bdd0111c101256de9e05a0c0ded939","task":"P01","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/p03-input-contract.yml","old_blob":null,"blob":"56621ee39204061d6a5cae8712b9f8ef490fa63c","source_change_commit":"6ad44e3331c573ae9aa81894650a2833a923f1d2","task":"P03","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/p15-single-model.yml","old_blob":null,"blob":"f5d60b5d03a182e36e13a53b34ab1bcd61cb406a","source_change_commit":"93bdf0e7e29d4165701b8abd93b75f27749a4e70","task":"P15","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/p17-single-api.yml","old_blob":null,"blob":"51b5513d2a6f24630852a26d291e516cd1548323","source_change_commit":"e6703adf92d154fc23b40d65fd1989fd0f498bd7","task":"P17","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/p32a-status.yml","old_blob":null,"blob":"5e636160335b8fef53e2b707f5504b1e568ae379","source_change_commit":"b7445bde59f1a480c07a5d4f0806ef5600a954d3","task":"P01","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/public-api-batch50.yml","old_blob":null,"blob":"43cd3a1e6fea33f0514805bfd3dfd7d3e6d3635a","source_change_commit":"856376a97e22cb1c64a5ed548ce0cbcd15ade138","task":"USER_TEST50","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/r4-cause-regression108.yml","old_blob":null,"blob":"1044773a40f0d3c3fdc3591c7b5e875347141c8b","source_change_commit":"a3c070237e8a00ae662489c88ac37f9b5dbfdfe5","task":"R4-1.08","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/r4-http-evidence-x07.yml","old_blob":null,"blob":"5fb2e67d4edd0de323e6dd16c59d281391ef2a89","source_change_commit":"7a4b11e9f0fc6b8c2b86eaac02613130df13f7e8","task":"R4-X.07","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":".github/workflows/r4-planned-witness108.yml","old_blob":null,"blob":"042bb8e7cc4343f3a30fccb24269182f6079096a","source_change_commit":"1f77c504e4fe1645ede21ce50115e4e36ae38cbd","task":"R4-1.08","role":"WORKFLOW_DECLARATION_ONLY","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/cause_parent_witness108.py","old_blob":null,"blob":"0693ef9c20c0c8a367e59331bcb5e6064e3c37a2","source_change_commit":"a3c070237e8a00ae662489c88ac37f9b5dbfdfe5","task":"R4-1.08","role":"HISTORICAL_TARGETED_REPAIR_STUDY_NOT_PUBLIC_DISPATCH","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/cause_regression108.py","old_blob":null,"blob":"ca6853222856d0620dcc49c718751ca9c78ed1ce","source_change_commit":"105658c1d9ac757765265608c961a750be8af2d5","task":"R4-1.08","role":"HISTORICAL_TARGETED_REPAIR_STUDY_NOT_PUBLIC_DISPATCH","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/cause_regression_support108.py","old_blob":null,"blob":"343758e578800ee3aa26c61629e9e80a79705af1","source_change_commit":"6fe759023bfa8c51eb98fc9b17ec514532f8d825","task":"R4-1.08","role":"HISTORICAL_TARGETED_REPAIR_STUDY_NOT_PUBLIC_DISPATCH","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/compound_panel_candidate108.py","old_blob":null,"blob":"2116843f25ea430f5b41dd38cf728715c3c56944","source_change_commit":"1f77c504e4fe1645ede21ce50115e4e36ae38cbd","task":"R4-1.08","role":"HISTORICAL_TARGETED_REPAIR_STUDY_NOT_PUBLIC_DISPATCH","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/http_evidence_x07.py","old_blob":null,"blob":"58529992c730abc74bbdd9be236e65a015c8792e","source_change_commit":"652fcfbed5320ff7ae3744431a8c90fea2296cf6","task":"P01","role":"SAME_REQUEST_EVIDENCE_CONSUMER","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/planned_witness_chain108.py","old_blob":null,"blob":"dfc788713fd5830f7c5257a2c3a645b60c11718c","source_change_commit":"b6682851cb15b65cc8c8210496b5e841d5b5fd34","task":"R4-1.08","role":"HISTORICAL_TARGETED_REPAIR_STUDY_NOT_PUBLIC_DISPATCH","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/planned_witness_contract108.py","old_blob":null,"blob":"d48b3355d148bb78dc8038acaf56e7e3d666b254","source_change_commit":"b6682851cb15b65cc8c8210496b5e841d5b5fd34","task":"R4-1.08","role":"HISTORICAL_TARGETED_REPAIR_STUDY_NOT_PUBLIC_DISPATCH","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/planned_witness_support108.py","old_blob":null,"blob":"845038df0f2b66ff9fcd2ee423f69757220ea190","source_change_commit":"1f77c504e4fe1645ede21ce50115e4e36ae38cbd","task":"R4-1.08","role":"HISTORICAL_TARGETED_REPAIR_STUDY_NOT_PUBLIC_DISPATCH","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/public_program_dispatch_p17.py","old_blob":null,"blob":"65a9b9cb4a77925e442837429a5fa1e176860d2d","source_change_commit":"9032ebaea0e4c685b9306cbdfe7815f459bcd9c9","task":"P17","role":"SCOPED_SINGLE_UNIT_RUNTIME_OR_ASSESSOR","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_access_p15.py","old_blob":null,"blob":"72a497a872ca446bf0d172f4e5971d44d3638d4c","source_change_commit":"93bdf0e7e29d4165701b8abd93b75f27749a4e70","task":"P15","role":"SCOPED_SINGLE_UNIT_SOURCE","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_assembler_p15.py","old_blob":null,"blob":"778189cccaba7e9e4e7fcd29b2a1f6f7c280386b","source_change_commit":"6cd00f456a40d23c23999dc111cf344ad08f025c","task":"P15","role":"SCOPED_SINGLE_UNIT_SOURCE","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_current_programme_evaluator_p17.py","old_blob":null,"blob":"7ac2f8efcddab91bba747b7e232393ef6bda45a3","source_change_commit":"1c93dfad22c4c16abcce72fd97a384e6b529c097","task":"P17","role":"SCOPED_SINGLE_UNIT_RUNTIME_OR_ASSESSOR","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_decision_p17.py","old_blob":null,"blob":"717362f62c8eaef45ae065d0770d5517c44b7bbe","source_change_commit":"c154f3d715fc42f3ce60a73dadad58b52657da98","task":"P17","role":"SCOPED_SINGLE_UNIT_RUNTIME_OR_ASSESSOR","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_evaluation_p17.py","old_blob":null,"blob":"23956db2458c1d0c416c5c39a24ec3b521766845","source_change_commit":"bbf8210aa09d5faae6d7f03a7aaa800910a3afef","task":"P01","role":"SCOPED_SINGLE_UNIT_RUNTIME_OR_ASSESSOR","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_model_p15.py","old_blob":null,"blob":"434b7633cdccd8d006baa8a22bbef2e006062730","source_change_commit":"93bdf0e7e29d4165701b8abd93b75f27749a4e70","task":"P15","role":"SCOPED_SINGLE_UNIT_SOURCE","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_physical_p17.py","old_blob":null,"blob":"16a16f20af2603ea67a2cb631954342462fe73a0","source_change_commit":"1c93dfad22c4c16abcce72fd97a384e6b529c097","task":"P17","role":"SCOPED_SINGLE_UNIT_RUNTIME_OR_ASSESSOR","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_runtime_p17.py","old_blob":null,"blob":"ca33f86aa6ca0d23aa59fa366698c268f9c7c936","source_change_commit":"2f058ffafdb8763d6ced85c80d0051cd4de6c873","task":"P01","role":"SCOPED_SINGLE_UNIT_RUNTIME_OR_ASSESSOR","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_source_guest_route_evaluator_p17.py","old_blob":null,"blob":"e32189f2de3cea1545fba2c391468565dc4a0353","source_change_commit":"1c93dfad22c4c16abcce72fd97a384e6b529c097","task":"P17","role":"SCOPED_SINGLE_UNIT_RUNTIME_OR_ASSESSOR","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_source_living_evaluator_p17.py","old_blob":null,"blob":"cee0eb2d5262b99b553f38ef11c3a77a03e1cb10","source_change_commit":"1c93dfad22c4c16abcce72fd97a384e6b529c097","task":"P17","role":"SCOPED_SINGLE_UNIT_RUNTIME_OR_ASSESSOR","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/single_source_wall_function_evaluator_p17.py","old_blob":null,"blob":"8beab5c8b68d50458fd8edb10de3608ec5c1b2ca","source_change_commit":"1c93dfad22c4c16abcce72fd97a384e6b529c097","task":"P17","role":"SCOPED_SINGLE_UNIT_RUNTIME_OR_ASSESSOR","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false},{"path":"app/local_integration/stop_observation_p01.py","old_blob":null,"blob":"e5421221179a78ad8e313a5e86ba8e000bc26b79","source_change_commit":"652fcfbed5320ff7ae3744431a8c90fea2296cf6","task":"P01","role":"SAFE_STOP_OBSERVATION","review_scope":"Exact path bytes at last-change commit read back; task provenance is not new execution permission.","new_dispatch":false}]''')
def reconcile_current(m,previous,old):
 require(m.get('schema')=='CURRENT_SOURCE_INVENTORY_X05_V2' and type(m.get('version')) is int and m['version']==2 and m.get('reviewed_ref')==CURRENT_REF,'WRONG_CURRENT_SNAPSHOT_VERSION')
 require(m.get('previous_manifest_path')==SPEC and m.get('previous_manifest_blob')==PREVIOUS_BLOB and m.get('previous_reviewed_ref')==REVIEWED,'PREVIOUS_MANIFEST_BINDING')
 require(m.get('historical_x03_manifest_path')==OLD and m.get('historical_x03_manifest_blob')==OLD_BLOB,'OLD_MANIFEST_BINDING')
 require(m.get('new_dispatch') is False and m.get('self_hash_closure') is False and m.get('literal_legacy_isolation') is False,'NO_NEW_AUTHORITY')
 require(type(m.get('self_paths_unhashed')) is list and len(m['self_paths_unhashed'])==4 and set(m['self_paths_unhashed'])==SELF_V2,'SELF_SCOPE_CHANGED')
 previous_files,previous_tops=reconcile(previous,old)
 require(json.dumps(m.get('provenance'),sort_keys=True)==json.dumps(PROVENANCE_V2,sort_keys=True),'CURRENT_PROVENANCE_MISMATCH')
 added={r['path'] for r in PROVENANCE_V2 if r['old_blob'] is None}
 changed={r['path'] for r in PROVENANCE_V2 if r['old_blob'] is not None}
 d=m.get('delta',{})
 require(type(d.get('added')) is list and len(d['added'])==31 and set(d['added'])==added and type(d.get('changed')) is list and len(d['changed'])==4 and set(d['changed'])==changed and d.get('missing')==[],'CURRENT_DIFF_SET')
 files={p:dict(r) for p,r in previous_files.items()}
 for row in PROVENANCE_V2:
  path=row['path']
  require(row['new_dispatch'] is False,'NO_NEW_AUTHORITY')
  if row['old_blob'] is None:
   require(path not in files and path not in previous_tops,'CURRENT_ADDITION_DUPLICATE')
   cls='REVIEWED_WORKFLOW_DECLARATION_NO_NEW_DISPATCH' if path.startswith('.github/workflows/') else 'REVIEWED_STUDY_SOURCE_NO_NEW_DISPATCH'
   files[path]={'blob':row['blob'],'classification':cls}
  else:
   require(path in files and files[path]['blob']==row['old_blob'],'CURRENT_SOURCE_CHAIN')
   files[path]['blob']=row['blob']
 tops=previous_tops|added
 require(files==m.get('files') and len(files)==274,'CURRENT_RECONCILIATION_FAILED')
 require(type(m.get('top_level_paths')) is list and len(m['top_level_paths'])==311 and set(m['top_level_paths'])==tops,'CURRENT_TOP_LEVEL_SCOPE')
 require(type(m.get('presence_only_paths')) is list and len(m['presence_only_paths'])==51 and set(m['presence_only_paths'])==tops-set(files),'PRESENCE_ONLY_SCOPE')
 return files,tops
def scan(root=ROOT):
 root=Path(root)
 specbytes=read(root,SPEC_V2);previousbytes=read(root,SPEC);oldbytes=read(root,OLD)
 require(blob(previousbytes)==PREVIOUS_BLOB,'PREVIOUS_MANIFEST_CHANGED')
 require(blob(oldbytes)==OLD_BLOB,'OLD_MANIFEST_CHANGED')
 m=decode(specbytes);previous=decode(previousbytes);old=decode(oldbytes)
 files,tops=reconcile_current(m,previous,old)
 for p in SELF_V2:require((root/p).is_file() and not (root/p).is_symlink(),'SELF_PATH_REQUIRED')
 expected=tops|{p for p in SELF_V2 if p.startswith('app/local_integration/') or p.startswith('.github/workflows/')}
 require(surfaces(root)==expected,'UNREVIEWED_SURFACE')
 rows=[]
 for path,r in sorted(files.items()):
  data=read(root,path)
  require(blob(data)==r['blob'],'STALE_SNAPSHOT_SOURCE_CHANGED')
  if path.endswith('.py') and not (root/path).is_symlink():ast.parse(data,filename=path)
  rows.append({'path':path,**r})
 require(read(root,SPEC_V2)==specbytes and read(root,SPEC)==previousbytes and read(root,OLD)==oldbytes,'MANIFEST_CHANGED_DURING_READ')
 require(all(blob(read(root,p))==r['blob'] for p,r in files.items()),'SOURCE_CHANGED_DURING_READ')
 require(surfaces(root)==expected,'UNREVIEWED_SURFACE')
 return {'schema':'CURRENT_SOURCE_INVENTORY_X05_RESULT_V2','state':'CURRENT_SOURCE_INVENTORY_RECONCILED_VERSIONED_SCOPED',
  'reviewed_ref':CURRENT_REF,'file_count':len(rows),'top_level_surface_count':len(expected),'presence_only_count':51,
  'changed_count':4,'added_count':31,'missing_count':0,
  'inventory_digest':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),
  'manifest_digest':hashlib.sha256(specbytes).hexdigest(),'new_dispatch':False,'self_hash_closure':False,
  'literal_legacy_isolation':False,'old_x03_failure_retained':True,'historical_x05_snapshot_retained':True,'qualification_allowed':False,
  'scope':'Selected file byte identity and exact top-level presence only; four self paths unhashed; no runtime/gate/dispatch permission or full repo closure'}
if __name__=='__main__':
 import sys
 print(json.dumps(scan_historical() if '--historical' in sys.argv else scan(),sort_keys=True))
