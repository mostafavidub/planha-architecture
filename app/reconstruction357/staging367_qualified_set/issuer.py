"""Closed reviewed-artifact conceptual set issuer. No engine callback or delivery."""
import json,hashlib,types,ast,copy,os
from pathlib import Path
from fractions import Fraction as F
P=Path(__file__).resolve().parent;ROOT=P.parent
REGISTRY_SHA='7fa43802507e03349aeb88af7dfb02fba10cc366707ebc9d10826235e53b083d'
RULES=('SPACE_ACCOUNTING','GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','CIRCULATION_NECESSITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','OPENINGS_REAL','KITCHEN_PROXIMITY')
Q12_STATUS='PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW'
DEPS={'SOURCE_ROOM_USE','PUBLIC_SUPPORT','ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON'}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def need(ok,code):
 if not ok:raise ValueError(code)
def capture():
 data=(P/'registry.json').read_bytes();need(hashlib.sha256(data).hexdigest()==REGISTRY_SHA,'REGISTRY_CHANGED');reg=json.loads(data);captured={}
 for n,h in reg['sources'].items():
  d=(ROOT/n).read_bytes();need(hashlib.sha256(d).hexdigest()==h,'SOURCE_CHANGED:'+n);captured[n]=d;canonical=os.path.relpath((ROOT/n).resolve(),ROOT.resolve());need(canonical not in captured or captured[canonical]==d,'CONFLICTING_SOURCE_ALIAS');captured[canonical]=d
 return reg,captured

def validate_member(kind,record,fresh,q,manifest):
 """Structural defense only; authority requires fixed captured bytes upstream."""
 m=record['candidate']['model'];mh=digest(m);rd=digest(record);fd=digest(fresh)
 need(fresh['model_digest']==mh and fresh['raw_report']['model_hash']==mh,'FRESH_MODEL')
 raw=record['candidate']['request'];need(type(raw)is dict and set(raw)=={'W','L','n','requested_count'} and type(raw['requested_count'])is int and raw['requested_count']==2,'REQUEST_COUNT')
 need(digest(raw)==record['candidate']['request_digest'] and digest(raw)==digest(fresh['provenance']['raw']),'REQUEST_PROVENANCE')
 need(list(map(F,m['inputs']))==[F(raw[k])for k in ('W','L','n')],'INPUT_MODEL')
 if kind=='balanced365':
  need(q['schema']=='BALANCED365_QUALIFICATION_EXPANDED367' and q['model_digest']==mh and q['record_digest']==rd and q['fresh_result_digest']==fd,'BALANCED_QUAL_BINDING')
  need(manifest['record_digest']==rd and manifest['fresh_digest']==fd,'BALANCED_MANIFEST_INPUT')
  roles=q['roles'];q12=q['internal_q12'];units=q12['evidence'];deps=q12['sealed_dependency_digests']
 else:
  need(kind=='joint367' and q['schema']=='SEMANTIC_JOINT367_CURRENT_SOURCE_V4_FINAL_AUDITED_ARTIFACT' and q['source_profile']=='SOURCE_JOINT367' and q['registered_artifact_verified']is True,'JOINT_PROFILE')
  need(q['model_hash']==mh and q['raw_report_hash']==digest(fresh['raw_report']) and q['source_manifest_digest']==digest(manifest),'JOINT_QUAL_BINDING')
  roles=q['source_closures']['final_role'];q12=roles['internal_per_unit_review'];units=q12['units'];deps=q12['dependency_evidence_digests']
  need(q12['model_hash']==mh and q12['record_digest']==rd and q12['fresh_result_digest']==fd,'JOINT_Q12_BINDING')
  need(q12['verdict']==Q12_STATUS and q12['missing']==[],'JOINT_Q12_VERDICT')
  expected={'same_model_source_capacity_use_access','all_unit_required_role_gaps_closed','own_source_common_balance_closed','same_model_finite_service_criterion_closed','no_dependency_on_selected_set'}
  need(set(q12['explicit_complete_predicate'])==expected and all(v is True for v in q12['explicit_complete_predicate'].values()),'Q12_EXPLICIT_PREDICATES')
 need(roles['model_hash']==mh and roles['record_digest']==rd and roles['review_digest']==fd,'ROLES_BINDING')
 qs=q['quality'];need(type(qs)is list and len(qs)==12 and all(type(x)is dict for x in qs),'QUALITY_SHAPE');ids=[x['rule_id']for x in qs]
 need(len(set(ids))==12 and set(ids)==set(RULES)|{'DISTINCTNESS_AND_FAIRNESS'},'QUALITY_IDS')
 for row in qs:
  if row['rule_id']in RULES:need(row['verdict']=='PASS' and row.get('missing')==[] and row.get('model_hash')==mh and bool(row.get('scope')) and bool(row.get('source_closure')),'PARENT_UNPROVEN')
 uid=[u['id']for u in m['units']];need(len(uid)==2 and len(set(uid))==2,'MODEL_UNIT_IDS')
 need(type(units)is list and len(units)==2 and all(type(u)is dict for u in units) and {u['unit']for u in units}==set(uid),'Q12_UNITS')
 nodes=roles['nodes'];node=nodes['Q12_PER_UNIT'];need(node['status']==Q12_STATUS and node['blocking_dependencies']==[],'Q12_NODE_PENDING')
 need(set(deps)==DEPS and set(node['depends_on'])==DEPS and node['sealed_dependency_digests']==deps,'Q12_DEPENDENCIES')
 need(all(deps[k]==digest(nodes[k])for k in DEPS),'Q12_SEALED_DAG')
 if kind=='balanced365':need(digest(node)==digest(q12),'BALANCED_Q12_NODE')
 else:need(digest(node['evidence'])==digest(units),'JOINT_Q12_UNIT_SOURCE')
 balance=node['balanced_common_access'];bh=digest(balance)
 need(balance['model_hash']==mh and balance['record_digest']==rd and balance['fresh_result_digest']==fd,'BALANCE_BINDING')
 for u in units:
  need(u['whole_unit_verdict']==Q12_STATUS and u['exact_pending']==[] and u['balanced_access_digest']==bh,'Q12_UNIT_PENDING')
  need(u['resolved_dependency_digests']=={k:deps[k]for k in ('COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON')} and bool(u['source_room_roles']) and bool(u['capacity_use_access_source_rows']),'Q12_UNIT_SOURCES')
 return {'member':kind,'model_digest':mh,'record_digest':rd,'fresh_digest':fd,'qualification_digest':digest(q),'q12_digest':digest(q12),'program_digest':digest(m['program']),'profile_digest':digest(m['profile']),'request_digest':digest(raw),'unit_ids':uid,'scope':'PINNED_CURRENT_SOURCE_CONCEPTUAL_REVIEW','parent_scopes':{x['rule_id']:x['scope']for x in qs if x['rule_id']in RULES}}

def verify_whole_dag(kind,qualification,captured):
 base='role_registry_model365.py'if kind=='balanced365'else'role_registry_joint367.py'
 final='role_registry_balanced365_expanded367_v3.py'if kind=='balanced365'else'role_registry_final_joint367_v4.py'
 prefix='semantic_rules357/'
 tree=ast.parse(captured[prefix+base]);assign=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='DAG'for t in n.targets));dag=ast.literal_eval(assign.value)
 ns={'copy':copy,'BASE_DAG':dag,'ORIGINAL_DAG':dag}
 tree=ast.parse(captured[prefix+final]);selected=[]
 for n in tree.body:
  if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='DAG'for t in n.targets):selected.append(n)
  elif isinstance(n,ast.AugAssign)and isinstance(n.target,ast.Subscript)and isinstance(n.target.value,ast.Name)and n.target.value.id=='DAG':selected.append(n)
  elif isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and isinstance(n.value.func.value,ast.Subscript)and isinstance(n.value.func.value.value,ast.Name)and n.value.func.value.value.id=='DAG':selected.append(n)
 need(len(selected)==3,'FINAL_DAG_SOURCE_SHAPE')
 exec(compile(ast.Module(body=selected,type_ignores=[]),final,'exec'),ns)
 # Compile the exact pinned digest and seal functions, without importing an engine.
 common=ast.parse(captured[prefix+'common.py']);df=next(n for n in common.body if isinstance(n,ast.FunctionDef)and n.name=='digest');env={'copy':copy,'hashlib':hashlib,'json':json}
 exec(compile(ast.Module(body=[df],type_ignores=[]),'captured_common_digest','exec'),env)
 seal=ast.parse(captured[prefix+'role_dependency_seal367.py']);functions=[n for n in seal.body if isinstance(n,ast.FunctionDef)];exec(compile(ast.Module(body=functions,type_ignores=[]),'captured_dependency_seal','exec'),env)
 roles=qualification['roles']if kind=='balanced365'else qualification['source_closures']['final_role']
 env['verify'](roles['nodes'],ns['DAG']);need(roles['topological_order']==env['order'](ns['DAG']),'TOPOLOGICAL_ORDER')
 return True

def _build():
 reg,cap=capture();members=[];objects={}
 for kind,cfg in reg['members'].items():
  r,f,q,man=[json.loads(cap[cfg[k]])for k in ('record','fresh','qualification','manifest')]
  if kind=='balanced365':need(q['invocation_manifest_sha256']==reg['sources'][cfg['manifest']],'INVOCATION_MANIFEST')
  verify_whole_dag(kind,q,cap)
  members.append(validate_member(kind,r,f,q,man));objects[kind]=(r,f,q)
 need(len(members)==2 and len({x['model_digest']for x in members})==2,'TWO_DISTINCT_MEMBERS')
 for k in ('program_digest','profile_digest','request_digest'):need(members[0][k]==members[1][k],'SHARED_'+k)
 # Recompute the existing exact fixed-pair source algorithm, not stored boolean.
 path=ROOT/reg['pair_code'];module=types.ModuleType('_qualified_pair367');module.__file__=str(path);exec(compile(cap[reg['pair_code']],str(path),'exec'),module.__dict__);pair=module.evaluate()
 need(type(pair['pair_count'])is int and pair['pair_count']==1 and pair['source_organization_distinct']is True,'EXACT_DISTINCT_PAIR')
 expected={x['model_digest']:x for x in members}
 need(len(pair['members'])==2 and {x['model_digest']for x in pair['members']}==set(expected),'PAIR_MEMBERS')
 for x in pair['members']:
  e=expected[x['model_digest']];need(x['record_digest']==e['record_digest'] and x['fresh_result_digest']==e['fresh_digest'],'PAIR_MEMBER_BINDING')
 capture()
 body={'schema':'FIXED_TWO_MEMBER_CONCEPTUAL_SELECTED_SET367','members':members,'pair_digest':digest(pair),'pair_identity':pair['pair_identity'],'registry_sha256':REGISTRY_SHA,'requested_count':2,'qualified_selected_count':2,'request_fulfilled_for_fixed_concept_profile':True,'membership_authority':'FIXED_PINNED_REVIEWED_CONCEPT_SET_ONLY','accepted':False,'delivery_allowed':False,'live_authority':False,'global_domain_complete':False,'scope':'ONLY_FIXED_REQUEST_26x28_N2_COUNT2_AND_REGISTERED_SOURCE_PROGRAM_PROFILE; NOT_GENERAL_MVP_OR_TECHNICAL_APPROVAL'}
 body['immutable_set_digest']=digest(body);return body

def evaluate_registered_set():
 try:return _build()
 except (ValueError,KeyError,TypeError,IndexError,OSError,OverflowError)as e:return {'status':'UNKNOWN','missing':[str(e)],'qualified_selected_count':0,'membership_authority':False,'request_fulfilled_for_fixed_concept_profile':False,'accepted':False,'delivery_allowed':False,'live_authority':False,'global_domain_complete':False}
