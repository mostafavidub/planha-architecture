"""Same-run390 balanced role computation; no automatic parent admission."""
import json,sys,time,copy
from pathlib import Path
from gate390 import ROOT,HERE,D,validate
SEM=ROOT/'semantic_rules357'
sys.path[:0]=[str(HERE),str(SEM),str(ROOT/'staging378_finite_portals'),str(ROOT/'finite_comparison358')]
def run(record,fresh):
 start=time.monotonic();before=D([record,fresh]);binding=validate(record,fresh)
 from semantic390 import run as essential
 e={'essential':essential(record,fresh)};errors={}
 import common
 common.REGISTRY_NAME='method_registry_source365.json'
 from adapters390 import audit_loaded
 audit_loaded()
 def capture(key,fn):
  try:e[key]=fn()
  except Exception as error:errors[key]=type(error).__name__+':'+str(error)
 from reassess_spatial390 import evaluate as spatial
 from circulation_role390 import evaluate as circulation
 from common_role_closure390 import evaluate as common_role
 from entry_separation390 import evaluate as reservation
 from balanced_access390 import evaluate as balance
 from service390 import evaluate as service
 from cohort390 import evaluate as cohort
 from role_registry_model390 import room_inventory,DAG,ordered_dag
 from support_reservation365 import reconcile
 capture('source_room_roles',lambda:room_inventory(record['candidate']['model'],common.rows(record['candidate']['model'],fresh['raw_report'])))
 capture('spatial',lambda:spatial(record,fresh))
 capture('circulation',lambda:circulation(record,fresh))
 capture('common_role',lambda:common_role(record,fresh))
 capture('operational_reservation',lambda:reservation(record,fresh))
 capture('exact_balance',lambda:balance(record,fresh))
 capture('service',lambda:service(record,fresh))
 capture('public_reconciliation',lambda:reconcile(e['spatial']['support'],e['operational_reservation']))
 capture('cohort',lambda:cohort(record,fresh,e['essential']['evidence']['intrinsic_eligibility']))
 n={k:{'status':'UNKNOWN','missing':['REQUIRED_CURRENT_EVIDENCE_NOT_COMPLETE']}for k in DAG}
 n['SOURCE_GATE']={'status':'PASS_REGISTERED_CURRENT390_SUPERVISED_MEMBER','binding':binding}
 if 'source_room_roles'in e:n['SOURCE_ROOM_USE']={'status':'PASS_SCOPED_WHOLE_SOURCE_ROOM_ROLES','evidence':e['source_room_roles']};n['PARTITION']={'status':'PASS_EXACT_GEOMETRIC_PARTITION_NOT_ROLE_ACCEPTANCE','scope':'room_inventory requires exact named-floor inventory and same current partition row'}
 rec=e.get('public_reconciliation',{})
 if rec:n['PUBLIC_SUPPORT']={'status':'UNKNOWN_UNRESOLVED_FUNCTIONAL_EXTENT'if rec['unresolved_positive_extent']else'PASS_SCOPED_FUNCTIONAL_EXTENT_WITH_SEPARATE_NONUSABLE_OPERATIONAL_RESERVATION','evidence':rec}
 ci=e.get('circulation',{})
 if ci:
  n['ENTRY_CIRCULATION']={'status':'PASS_SCOPED_REQUIRED_TARGET_COMPONENTS'if all(c['verdict']=='PASS_EXACT_REQUIRED_PATH_USE_COMPONENT'for u in ci['units']for c in u['entry_circulation_components'])else'UNKNOWN','evidence':{u['unit']:u['entry_circulation_components']for u in ci['units']}}
  n['PRIVATE_CIRCULATION']={'status':'PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE'if all(u['intrinsic_private_role_status']=='PASS_SCOPED_SOURCE_WHOLE_CONNECTOR_ROLE'for u in ci['units'])else'UNKNOWN_SOURCE_PRIVATE_COMPONENT_ROLE','evidence':ci}
 svc=e.get('service',{})
 if svc:n['SERVICE_CIRCULATION']={'status':'PASS_SCOPED_SOURCE117_BATH_WC_CIRCULATION_RECONCILIATION'if svc['verdict']=='PASS_SCOPED_FINITE_SERVICE_COMPACTNESS'else'UNKNOWN_EXCLUSIVE_SERVICE_ROLE_ACCOUNTING','evidence':svc}
 core=e.get('common_role',{})
 if core:n['COMMON_ROLE']={'status':core['verdict'],'evidence':core}
 walls=e.get('spatial',{}).get('wall_purpose',{})
 n['WALL_PURPOSE']={'status':'UNKNOWN_Q04_DEPENDENT_WALL_NECESSITY','evidence':walls,'actual_pending_wall_ids':[x['wall_id']for x in walls.get('rows',[])if not x['verdict'].startswith('PASS_')],'no_hardcoded_wall_count':True}
 n['Q04_COMPARISON']={'status':'UNKNOWN_FINITE_COHORT_JOIN_PENDING','evidence':e.get('cohort'),'missing':['CURRENT_FULL_COHORT_AND_BOUND_RANK2_INTRINSIC_PROOF_REQUIRED']}
 n['Q12_PER_UNIT']={'status':'UNKNOWN_REQUIRED_ROLE_DEPENDENCIES','current_exact_balance':e.get('exact_balance'),'reservation_reconciled':rec,'scope':'No equality or dependency predicate waived; current exact metric mismatches remain UNKNOWN.'}
 n['Q14_SELECTION_SET']={'status':'UNKNOWN_SELECTION_SET_NOT_SUPPLIED','requested_count':2,'actual_branch_count':1}
 for k in ordered_dag():n[k]['depends_on']=DAG[k];n[k]['blocking_dependencies']=[x for x in DAG[k]if not n[x]['status'].startswith('PASS_')]
 parents={k:{'verdict':'UNKNOWN','reason':'CURRENT_DEPENDENCIES_UNCLOSED','model_digest':binding['model_digest']}for k in('SPACE_ACCOUNTING','CIRCULATION_NECESSITY','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','DISTINCTNESS_AND_FAIRNESS')}
 parents['SERVICE_COMPACTNESS']={'verdict':'UNKNOWN_PENDING_INDEPENDENT_AUDIT'if svc.get('verdict')=='PASS_SCOPED_FINITE_SERVICE_COMPACTNESS'else'UNKNOWN_CURRENT_SERVICE_PROOF_INCOMPLETE','evidence_digest':D(svc),'model_digest':binding['model_digest']}
 origins=audit_loaded();validate(record,fresh)
 if before!=D([record,fresh]):raise ValueError('INPUT_MUTATION')
 return {'schema':'SAME_RUN390_ESSENTIAL_AND_ROLE_COMPUTATION','binding':binding,'evidence':e,'errors':errors,'nodes':n,'parent_candidates':parents,'source_module_origins':origins,'evidence_bindings':{k:{**binding,'evidence_digest':D(v)}for k,v in e.items()},'new_fresh_checker_executed':False,'full_candidate_constructed':False,'source_prefix_geometry_reexecuted':True,'post_form_stored_artifact_reassessment':False,'same_browser_run_semantic_execution':True,'full_q04_closed':False,'accepted':False,'delivery_allowed':False,'request_fulfilled':False,'seconds':time.monotonic()-start}
