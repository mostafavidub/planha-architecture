"""Expanded-domain qualification on one fixed artifact; no selected-set approval."""
import copy
from common import digest
DEPENDENT=('SPACE_ACCOUNTING','CIRCULATION_NECESSITY','PRIVACY_WITHOUT_FAKE_BAFFLE','COMMON_CORE_COMPACTNESS')
def bind(record,fresh,old,roles):
 mh=digest(record['candidate']['model']);rd=digest(record);fd=digest(fresh)
 if old.get('model_hash')!=mh or old.get('raw_report_hash')!=digest(fresh['raw_report']) or old.get('registered_artifact_verified')is not True:raise ValueError('OLD_CURRENT_INPUT_BINDING')
 if roles.get('schema')!='ROLE_REGISTRY_BALANCED365_EXPANDED367_SOURCE_ROLES_V2' or roles.get('model_hash')!=mh or roles.get('record_digest')!=rd or roles.get('review_digest')!=fd:raise ValueError('EXPANDED_ROLE_BINDING')
 from role_dependency_seal367 import verify
 from role_registry_balanced365_expanded367_v3 import DAG
 nodes=roles['nodes'];verify(nodes,DAG);q=nodes['Q04_COMPARISON']['evidence']
 if q.get('schema')!='BALANCED365_EXPANDED_COHORT367' or q.get('verdict')!='PASS_SCOPED_FINITE_Q04_BALANCED365_EXPANDED367' or q.get('remaining')!=[]:raise ValueError('EXPANDED_Q04_REQUIRED')
 if (q.get('model_digest'),q.get('record_digest'),q.get('fresh_result_digest'))!=(mh,rd,fd):raise ValueError('EXPANDED_Q04_BINDING')
 if q.get('new367_intrinsic',{}).get('eligible')is not True or q.get('new367_comparison',{}).get('dominance')!='FALSE' or not q.get('draft366_property'):raise ValueError('EXPANDED_SCOPE_INCOMPLETE')
 per=nodes['Q12_PER_UNIT']
 if per.get('status')!='PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW' or per.get('blocking_dependencies'):raise ValueError('Q12_REQUIRED')
 balance=per['balanced_common_access']
 if (balance.get('model_hash'),balance.get('record_digest'),balance.get('fresh_result_digest'))!=(mh,rd,fd):raise ValueError('Q12_BALANCE_BINDING')
 if balance.get('verdict')!='PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS':raise ValueError('Q12_BALANCE_REQUIRED')
 for u in per['evidence']:
  if u.get('exact_pending')!=[] or u.get('balanced_access_digest')!=digest(balance):raise ValueError('Q12_UNIT_INCOMPLETE')
  if u.get('resolved_dependency_digests')!={k:digest(nodes[k])for k in ('COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON')}:raise ValueError('Q12_STALE_DEPENDENCIES')
 quality={r['rule_id']:copy.deepcopy(r)for r in old['quality']}
 for rid in DEPENDENT:
  p=roles['parent_evidence'][rid];node=nodes[p['closure_node']]
  if p['verdict']!='PASS_SCOPED_INTERNAL_CURRENT_SOURCE' or p['missing'] or not all(x is True for x in p['explicit_complete_predicate'].values()):raise ValueError('PARENT_INCOMPLETE')
  if (p['model_hash'],p['record_digest'],p['fresh_result_digest'])!=(mh,rd,fd) or p['closure_evidence_digest']!=digest(node) or node['blocking_dependencies']:raise ValueError('PARENT_BINDING')
  for dep,h in p['dependency_evidence_digests'].items():
   if h!=digest(nodes[dep])or not nodes[dep]['status'].startswith('PASS_'):raise ValueError('PARENT_STALE_DEPENDENCY')
  quality[rid]={'rule_id':rid,'verdict':'PASS','missing':[],'source_closure':p,'scope':'CURRENT_BALANCED365_WITH_EXPANDED367_FINITE_DOMAIN','model_hash':mh}
 others=[v for k,v in quality.items()if k!='DISTINCTNESS_AND_FAIRNESS']
 if len(others)!=11 or any(v['verdict']!='PASS' or v.get('missing')for v in others):raise ValueError('ELEVEN_PARENTS_NOT_COMPLETE')
 quality['DISTINCTNESS_AND_FAIRNESS']={'rule_id':'DISTINCTNESS_AND_FAIRNESS','verdict':'UNKNOWN','missing':['REQUESTED_SELECTED_SET_NOT_ESTABLISHED'],'internal_q12_digest':digest(per)}
 return {'schema':'BALANCED365_QUALIFICATION_EXPANDED367','record_digest':rd,'fresh_result_digest':fd,'model_digest':mh,'quality':list(quality.values()),'roles':roles,'internal_q12':per,'eleven_parent_complete':True,'selected_set_complete':False,'accepted':False,'delivery_allowed':False,'fresh_executed':False,'old_engine_evidence_digest':digest(old)}
def evaluate(record,fresh):
 from engine365_v3 import evaluate as old_engine
 from role_registry_balanced365_expanded367_v3 import evaluate as current_roles
 old=old_engine(record['candidate']['model'],fresh['raw_report'],registered_artifact={'record':record,'result':fresh})
 roles=current_roles(record,fresh)
 return bind(record,fresh,old,roles)
