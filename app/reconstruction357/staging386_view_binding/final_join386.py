"""Pure measured current-role dependency join. No pinned current-record loader."""
import copy,json,hashlib
from pathlib import Path
from fractions import Fraction as F
D=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
DAG={
 'SOURCE_GATE':[], 'PARTITION':['SOURCE_GATE'], 'SOURCE_ROOM_USE':['SOURCE_GATE'],
 'PUBLIC_SUPPORT':['SOURCE_ROOM_USE','SOURCE_GATE'], 'ENTRY_CIRCULATION':['SOURCE_GATE'],
 'PRIVATE_CIRCULATION':['SOURCE_GATE'], 'SERVICE_CIRCULATION':['SOURCE_ROOM_USE'],
 'COMMON_ROLE':['SOURCE_GATE'], 'WALL_PURPOSE':['SOURCE_ROOM_USE','PRIVATE_CIRCULATION'],
 'Q04_COMPARISON':['ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE'],
 'Q11_WHOLE_ROLE':['PARTITION','SOURCE_ROOM_USE','PUBLIC_SUPPORT','ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE','WALL_PURPOSE','Q04_COMPARISON'],
 'Q05_PRIVACY':['SOURCE_GATE','WALL_PURPOSE','Q11_WHOLE_ROLE'],
 'Q12_PER_UNIT':['SOURCE_ROOM_USE','PUBLIC_SUPPORT','ENTRY_CIRCULATION','PRIVATE_CIRCULATION','SERVICE_CIRCULATION','COMMON_ROLE','WALL_PURPOSE'],
 'Q14_SELECTION_SET':['SOURCE_GATE']}
def order():
 out=[]
 while len(out)<len(DAG):
  ready=sorted(k for k in DAG if k not in out and all(x in out for x in DAG[k]))
  if not ready:raise ValueError('DAG_CYCLE')
  out+=ready
 return out
def validate_semantic_views(record,fresh,semantic_views):
 env,res,binding=semantic_views;c=record['candidate'];trace=record['trace']
 expected={'record_digest':D(record),'fresh_digest':D(fresh),'model_digest':D(c['model'])}
 if any(binding.get(k)!=v for k,v in expected.items()):raise ValueError('SEMANTIC_PRODUCER_BINDING')
 ef={'candidate_id':D(c),'raw':c['request'],'packet':c['packet'],'input_record_digest':D(record),'outer_trace_digest':D(trace),'original_result_digest':D(fresh),'new_fresh_execution':False}
 rf={'candidate_digest':D(env),'raw_fresh_report':fresh['raw_report'],'original_result_digest':D(fresh),'input_record_digest':D(record),'outer_trace_digest':D(trace),'new_fresh_execution':False}
 if any(env.get(k)!=v for k,v in ef.items())or any(res.get(k)!=v for k,v in rf.items()):raise ValueError('SEMANTIC_VIEW_EXACT_ARTIFACT_BINDING')
 if D(env['packet']['world_model'])!=D(c['model'])or fresh['model_digest']!=D(c['model']):raise ValueError('SEMANTIC_VIEW_MODEL_BINDING')
 if not isinstance(env.get('schema'),str)or not env['schema']or not isinstance(res.get('schema'),str)or not res['schema']:raise ValueError('SEMANTIC_VIEW_SCHEMA_REQUIRED')
 # Producer-specific schemas and run metadata are preserved, never normalized.
 # The caller gates the view producer; exact original bytes feed the wall digest.
 return D(res)
def validate_wall_inventory(record,fresh,w,semantic_views):
 m=record['candidate']['model'];ids=[x['wall_id']for x in w['rows']]
 if len(ids)!=len(set(ids))or set(ids)!=set(m['walls']):raise ValueError('EXACT_CURRENT_WALL_INVENTORY')
 if w['source_origin_record_digest']!=D(record)or w['base_fresh_digest']!=validate_semantic_views(record,fresh,semantic_views):raise ValueError('WALL_ORIGIN_FRESH_BINDING')
 return ids
def join(record,fresh,roles,cohort,semantic_views):
 before=D([record,fresh,roles,cohort,semantic_views]);m=record['candidate']['model'];mh=D(m);b={'record_digest':D(record),'fresh_digest':D(fresh),'model_digest':mh}
 for evidence in (roles,cohort):
  if any(evidence['binding'].get(k)!=v for k,v in b.items()):raise ValueError('CURRENT_ROLE_COMPARISON_BINDING')
 if fresh['input_record_digest']!=D(record)or fresh['model_digest']!=mh:raise ValueError('CURRENT_FRESH_BINDING')
 validate_semantic_views(record,fresh,semantic_views)
 spatial=roles['evidence']['spatial']
 if spatial['record_digest']!=D(record)or spatial['raw_review_digest']!=D(fresh)or spatial['model_hash']!=mh:raise ValueError('SPATIAL_WRAPPER_CURRENT_BINDING')
 # Exact evidence bindings avoid joining current labels with an unrelated stored node.
 e=roles['evidence'];n=copy.deepcopy(roles['nodes']);errors={}
 for key,value in e.items():
  eb=roles['evidence_bindings'][key]
  if eb['evidence_digest']!=D(value)or any(eb.get(k)!=v for k,v in b.items()):raise ValueError('ROLE_EVIDENCE_BINDING:'+key)
 def need(ok,label):
  if not ok:raise ValueError(label)
 def attempt(key,fn):
  try:n[key]=fn()
  except (ValueError,KeyError,TypeError,IndexError)as ex:errors[key]=str(ex);n[key]={'status':'UNKNOWN_'+key,'missing':[str(ex)]}
 def q04():
  need(cohort['full_q04_closed']is True and not cohort['remaining']and cohort['verdict']=='PASS_SCOPED_DECLARED_FINITE_Q04','FINITE_Q04_UNCLOSED')
  need(all(n[x]['status'].startswith('PASS_')for x in DAG['Q04_COMPARISON']),'Q04_ROLE_PREREQUISITES')
  return {'status':'PASS_SCOPED_DECLARED_FINITE_Q04','evidence':cohort}
 attempt('Q04_COMPARISON',q04)
 def walls():
  w=e['spatial']['wall_purpose'];need(w['model_hash']==mh,'WALL_MODEL');need(not w.get('unjoined_host_ids'),'UNJOINED_HOSTS');need(n['PRIVATE_CIRCULATION']['status']=='PASS_SCOPED_INTRINSIC_PRIVATE_COMPONENT_ROLE','PRIVATE_ROLE');need(n['Q04_COMPARISON']['status'].startswith('PASS_'),'WALL_Q04')
  rows=w['rows'];ids=validate_wall_inventory(record,fresh,w,semantic_views)
  closed=[]
  for r in rows:
   if r['verdict']=='UNKNOWN_Q04_EXCLUSIVE_CIRCULATION_NECESSITY':
    need(r['kind']=='EXECUTED_SOURCE_PRIVATE_ACCESS_BOUNDARY','UNSUPPORTED_PENDING_WALL_KIND');closed.append({'wall_id':r['wall_id'],'source_row_digest':D(r),'intrinsic_private_role_digest':D(n['PRIVATE_CIRCULATION']),'finite_q04_digest':D(cohort),'verdict':'PASS_SCOPED_SOURCE_PRIVATE_ACCESS_BOUNDARY_WITH_FINITE_NECESSITY'})
   else:need(r['verdict'].startswith('PASS_'),'UNRESOLVED_WALL_ROLE')
  return {'status':'PASS_SCOPED_ALL_CURRENT_SOURCE_WALL_ROLES','evidence':{'immutable_constructive_wall_evidence':w,'closed_hall_dependency_rows':closed,'source_model_hash':mh,'inventory_count_measured':len(rows),'no_per_wall_removal_test_claimed':True}}
 attempt('WALL_PURPOSE',walls)
 def whole():
  need(all(n[k]['status'].startswith('PASS_')for k in DAG['Q11_WHOLE_ROLE']),'WHOLE_ROLE_DEPENDENCY')
  return {'status':'PASS_SCOPED_CURRENT_SOURCE_WHOLE_FUNCTIONAL_ROLE_ACCOUNTING','evidence':{'model_hash':mh,'dependency_digests':{k:D(n[k])for k in DAG['Q11_WHOLE_ROLE']}}}
 attempt('Q11_WHOLE_ROLE',whole)
 def privacy():
  need(all(n[k]['status'].startswith('PASS_')for k in DAG['Q05_PRIVACY']),'PRIVACY_ROLE_DEPENDENCIES')
  row=next(x for x in fresh['raw_report']['rule_contract_evidence']['requirements']if x['requirement_id']=='privacy_scenarios')
  need(row['model_hash']==mh and row['status']=='PASS_LIMITED','CURRENT_PRIVACY_SCENARIOS')
  witness=row['evidence']['witness'];need(witness.get('errors')==[]and witness.get('pending')==[]and witness['privacy'].get('errors')==[]and witness['privacy'].get('pending')==[],'PRIVACY_WITNESS_UNRESOLVED')
  return {'status':'PASS_SCOPED_CURRENT_SOURCE_PRIVACY_AND_FUNCTIONAL_WALL_ROLES','evidence':{'model_hash':mh,'same_model_privacy_row':row,'wall_role_digest':D(n['WALL_PURPOSE']),'whole_role_digest':D(n['Q11_WHOLE_ROLE'])}}
 attempt('Q05_PRIVACY',privacy)
 def units():
  need(all(n[k]['status'].startswith('PASS_')for k in DAG['Q12_PER_UNIT']),'PER_UNIT_ROLE_DEPENDENCIES');balance=e['exact_balance'];rec=e['public_reconciliation'];ci=e['circulation']
  need(balance['model_hash']==mh and balance['record_digest']==D(record)and balance['fresh_result_digest']==D(fresh),'BALANCE_CURRENT_BINDING')
  need(balance['verdict']=='PASS_SCOPED_EXACT_BALANCED_CURRENT_SOURCE_ACCESS'and all(x['equal_fixed_source_metrics']for x in balance['comparisons']),'EXACT_BALANCE_UNCLOSED')
  need(rec['model_hash']==mh and not rec['unresolved_positive_extent']and all(F(x['remaining_unresolved_area_m2'])==0 and x['usable_floor_capacity_increment']==0 for x in rec['rows']),'PUBLIC_RESERVATION_UNRESOLVED')
  expected={u['id']for u in m['units']};need({x['unit']for x in ci['units']}==expected and {x['unit']for x in rec['rows']}==expected,'PER_UNIT_INVENTORY')
  need(all(not x['untargeted_terminal_extensions']and x['intrinsic_private_role_status']=='PASS_SCOPED_SOURCE_WHOLE_CONNECTOR_ROLE'for x in ci['units']),'UNTARGETED_OR_UNPROVEN_PRIVATE_ROLE')
  return {'status':'PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW','evidence':[{'unit':u,'whole_unit_verdict':'PASS_SCOPED_CURRENT_SOURCE_INTERNAL_UNIT_ROLE_AND_BALANCED_ACCESS_REVIEW','exact_pending':[],'dependency_digests':{k:D(n[k])for k in DAG['Q12_PER_UNIT']},'balance_digest':D(balance),'public_reconciliation':next(x for x in rec['rows']if x['unit']==u)}for u in sorted(expected)],'balanced_common_access':balance}
 attempt('Q12_PER_UNIT',units)
 n['Q14_SELECTION_SET']={'status':'UNKNOWN_SELECTION_SET_NOT_SUPPLIED','requested_count':record['candidate']['request']['requested_count'],'actual_selected_set':None,'scope':'Two reviewed artifacts are not two qualified selected designs.'}
 for k in order():n[k]['depends_on']=DAG[k];n[k]['blocking_dependencies']=[x for x in DAG[k]if not n[x]['status'].startswith('PASS_')]
 specs={'SPACE_ACCOUNTING':('Q11_WHOLE_ROLE',DAG['Q11_WHOLE_ROLE']),'CIRCULATION_NECESSITY':('Q04_COMPARISON',DAG['Q04_COMPARISON']),'PRIVACY_WITHOUT_FAKE_BAFFLE':('Q05_PRIVACY',DAG['Q05_PRIVACY']),'COMMON_CORE_COMPACTNESS':('COMMON_ROLE',['COMMON_ROLE','Q11_WHOLE_ROLE','Q04_COMPARISON','Q12_PER_UNIT'])};parents={}
 for name,(key,deps)in specs.items():
  complete=n[key]['status'].startswith('PASS_')and not n[key]['blocking_dependencies']and all(n[x]['status'].startswith('PASS_')and not n[x]['blocking_dependencies']for x in deps)
  parents[name]={'verdict':'PASS_SCOPED_INTERNAL_CURRENT_SOURCE'if complete else'UNKNOWN','missing':[]if complete else['CURRENT_ROLE_DEPENDENCIES_UNCLOSED'],'required_dependency_nodes':deps,'dependency_evidence_digests':{x:D(n[x])for x in deps},'closure_node':key,'closure_evidence_digest':D(n[key]),'model_hash':mh,'fresh_result_digest':D(fresh),'record_digest':D(record),'explicit_complete_predicate':{'current_artifact_binding':True,'all_required_source_roles_closed':complete,'finite_comparison_closed':cohort['full_q04_closed'],'no_pending_required_dependency':complete},'scope':'Registered finite source Concept review only; not global optimum, technical approval or selected-output-set admission.','source_assumptions':['Unchanged source semantic predicates and actual measured current role evidence.']}
 parents['DISTINCTNESS_AND_FAIRNESS']={'verdict':'UNKNOWN','missing':['ACTUAL_REQUESTED_QUALIFIED_SELECTION_SET_NOT_SUPPLIED']}
 need(before==D([record,fresh,roles,cohort,semantic_views]),'INPUT_MUTATION')
 return {'schema':'CURRENT_MEASURED_ROLE_JOIN386_VIEW_BOUND','semantic_result_view_digest':D(semantic_views[1]),'binding':b,'nodes':n,'parent_evidence':parents,'errors':errors,'input_roles_digest':D(roles),'cohort_digest':D(cohort),'nonusable_operational_reservation':e['public_reconciliation'],'admission_allowed':False,'accepted':False,'delivery_allowed':False,'request_fulfilled':False}
