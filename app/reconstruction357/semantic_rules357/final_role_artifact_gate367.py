"""Closed reuse of an audited own-model role evaluation, never fresh authority.
No caller path, digest, approval flag, or substitute proof is accepted.
Binding is intentionally unavailable until the actual and its audit exist.
"""
import ast,copy,hashlib,json,types
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
BINDING_SHA='e23c87d27cb32349f07e633e16b278b879b860206929df0c2fee760c5c5abc75'
MODEL='b1256726013116ef5f1cbcd784380a80861fa485c372909d52bf8bce0d398759'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def file_sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def _predicates(p):
 return type(p)is dict and bool(p) and all(type(v)is bool and v for v in p.values())
def _load_seal_and_dag():
 # Only declarations from fixed, pre-verified source; no project imports.
 ns={'copy':copy,'digest':digest}
 tree=ast.parse((HERE/'role_dependency_seal367.py').read_text())
 nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('order','seal','verify')]
 if {n.name for n in nodes}!={'order','seal','verify'}:raise ValueError('SEAL_DECLARATION_INVENTORY')
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'<PINNED_DEPENDENCY_SEAL367>','exec'),ns)
 tree=ast.parse((HERE/'role_registry_joint367.py').read_text())
 assignments=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name)and t.id=='DAG'for t in n.targets)]
 if len(assignments)!=1:raise ValueError('DAG_SOURCE_INVENTORY')
 dag=ast.literal_eval(assignments[0].value)
 dag['WALL_PURPOSE']+=['Q04_COMPARISON'];dag['Q12_PER_UNIT']+=['Q04_COMPARISON']
 return ns,dag

def _validate(out,record,review,seal,dag):
 mh=digest(record['candidate']['model']);rh=digest(record);fh=digest(review)
 if mh!=MODEL or out['model_hash']!=mh or out['record_digest']!=rh or out['review_digest']!=fh:raise ValueError('CURRENT_ROLE_TRIPLE_BINDING')
 if out['schema']!='ROLE_REGISTRY_FINAL_JOINT367_V4_SAME_INVOCATION_SEALED_CURRENT_SOURCE_ROLES':raise ValueError('ROLE_SCHEMA')
 n=out['nodes'];seal['verify'](n,dag)
 if out['topological_order']!=seal['order'](dag):raise ValueError('TOPOLOGICAL_ORDER')
 for key in dag:
  if key!='Q14_SELECTION_SET' and (not n[key]['status'].startswith('PASS_')or n[key]['blocking_dependencies']):raise ValueError('ROLE_DEPENDENCY_NOT_CLOSED:'+key)
 service=out['service_compactness_evidence']
 if service['verdict']!='PASS_SCOPED_FINITE_SERVICE_COMPACTNESS'or service['remaining']:raise ValueError('SERVICE_INCOMPLETE')
 for name,field in [('cost','cost_receipt_digest'),('necessity','necessity_receipt_digest'),('functional_partition','functional_partition_digest')]:
  receipt=service['invocation_receipts'][name]
  if digest(receipt)!=service[field]:raise ValueError('SAME_INVOCATION_DIGEST:'+name)
  for key,val in [('model_digest',mh),('record_digest',rh),('fresh_result_digest',fh)]:
   if receipt[key]!=val or service[key]!=val:raise ValueError('SAME_INVOCATION_CURRENT_BINDING:'+name)
 q04=service['invocation_receipts']['necessity']
 if q04['remaining'] or q04['verdict']!='PASS_SCOPED_FINITE_Q04_SOURCE_JOINT367'or q04['domain']['domain_closed']is not True:raise ValueError('CURRENT_DOMAIN_INCOMPLETE')
 if digest(n['Q04_COMPARISON']['evidence'])!=digest(q04):raise ValueError('DERIVED_Q04_NOT_SAME_INVOCATION')
 partition=service['invocation_receipts']['functional_partition']
 if partition['remaining']or partition['verdict']!='PASS_SCOPED_CURRENT_SOURCE_ROLE_PARTITION':raise ValueError('CURRENT_PARTITION_INCOMPLETE')
 parents=('SPACE_ACCOUNTING','CIRCULATION_NECESSITY','PRIVACY_WITHOUT_FAKE_BAFFLE','COMMON_CORE_COMPACTNESS','SERVICE_COMPACTNESS')
 for rid in parents:
  proof=out['parent_evidence'][rid]
  if proof['verdict']!='PASS_SCOPED_INTERNAL_CURRENT_SOURCE'or proof['missing']or not _predicates(proof['explicit_complete_predicate']):raise ValueError('PARENT_NOT_COMPLETE:'+rid)
  for key,val in [('model_hash',mh),('record_digest',rh),('fresh_result_digest',fh)]:
   if proof[key]!=val:raise ValueError('PARENT_BINDING:'+rid)
  if rid=='SERVICE_COMPACTNESS':
   if proof['closure_evidence_digest']!=digest(service):raise ValueError('SERVICE_PARENT_RECEIPT')
  else:
   if proof['closure_evidence_digest']!=digest(n[proof['closure_node']]):raise ValueError('PARENT_NODE_BINDING')
   if set(proof['required_dependency_nodes'])!=set(proof['dependency_evidence_digests']):raise ValueError('PARENT_DEPENDENCY_INVENTORY')
   for dep,sha in proof['dependency_evidence_digests'].items():
    if sha!=digest(n[dep])or not n[dep]['status'].startswith('PASS_'):raise ValueError('PARENT_DEPENDENCY_BINDING')
 unitids={u['id']for u in record['candidate']['model']['units']};per=out['internal_per_unit_review']
 if per['missing']or not per['verdict'].startswith('PASS_')or not _predicates(per['explicit_complete_predicate']):raise ValueError('PER_UNIT_NOT_COMPLETE')
 for key,val in [('model_hash',mh),('record_digest',rh),('fresh_result_digest',fh)]:
  if per[key]!=val:raise ValueError('PER_UNIT_BINDING')
 if len(per['units'])!=len(unitids)or {u['unit']for u in per['units']}!=unitids:raise ValueError('PER_UNIT_INVENTORY')
 if digest(per['units'])!=digest(n['Q12_PER_UNIT']['evidence']):raise ValueError('PER_UNIT_NODE_BINDING')
 if set(per['dependency_evidence_digests'])!=set(dag['Q12_PER_UNIT']):raise ValueError('PER_UNIT_DEPENDENCY_INVENTORY')
 for dep,sha in per['dependency_evidence_digests'].items():
  if sha!=digest(n[dep]):raise ValueError('PER_UNIT_DEPENDENCY_BINDING')
 for u in per['units']:
  if u['exact_pending']or not u['whole_unit_verdict'].startswith('PASS_'):raise ValueError('PER_UNIT_UNRESOLVED')
 if out['parent_evidence']['DISTINCTNESS_AND_FAIRNESS']['verdict']!='UNKNOWN'or out['parent_evidence']['DISTINCTNESS_AND_FAIRNESS']['missing']!=['ACTUAL_REQUESTED_SELECTION_SET_NOT_SUPPLIED']:raise ValueError('SELECTION_PREMATURE')
 return True

def evaluate(record,review):
 if BINDING_SHA.startswith('PENDING'):raise ValueError('ACTUAL_AUDITED_ARTIFACT_NOT_BOUND')
 binding=HERE/'final_role_artifact367_binding.json'
 if file_sha(binding)!=BINDING_SHA:raise ValueError('ROLE_BINDING_SOURCE_CHANGED')
 b=json.loads(binding.read_text());before=digest([record,review])
 if digest(record)!=b['record_digest']or digest(review)!=b['fresh_digest']:raise ValueError('UNREGISTERED_ROLE_INPUT')
 def check():
  if file_sha(binding)!=BINDING_SHA:raise ValueError('ROLE_BINDING_MUTATED')
  for name,sha in b['files'].items():
   if file_sha(ROOT/name)!=sha:raise ValueError('ROLE_ARTIFACT_OR_SOURCE_CHANGED:'+name)
 check()
 out=json.loads((ROOT/'final_role367_v4_supervised/actual.json').read_text())
 test=json.loads((ROOT/'final_role367_v4_supervised/tests.json').read_text())
 supervision=json.loads((ROOT/'final_role367_v4_supervised/supervision.json').read_text())
 provenance=json.loads((ROOT/'final_role367_v4_supervised/actual_provenance.json').read_text())
 if test!={'tests_run':19,'failures':0,'errors':0,'successful':True}:raise ValueError('ACTUAL_TEST_RUN_NOT_CLOSED')
 if supervision['reason']!='COMPLETED'or not all(supervision[k]is True for k in ('worker_reaped','cleanup_verified','source_unchanged','actual_exists'))or supervision['unresolved']!=[]:raise ValueError('ACTUAL_EXECUTION_NOT_CLOSED')
 if provenance['kind']!='TEST_POSITIVE_REAL_REASSESSMENT'or provenance['synthetic']is not False or provenance['new_fresh']is not False:raise ValueError('ACTUAL_PROVENANCE')
 seal,dag=_load_seal_and_dag();_validate(out,record,review,seal,dag);check()
 if before!=digest([record,review]):raise ValueError('CALLER_INPUT_MUTATION')
 out['reuse_scope']='AUDITED_FIXED_OWN_MODEL_ARTIFACT_REASSESSMENT_NO_NEW_FRESH_OR_GEOMETRY_EXECUTION'
 out['new_geometry_execution']=False;out['artifact_binding_sha256']=BINDING_SHA
 return out
