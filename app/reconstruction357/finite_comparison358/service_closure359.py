"""Source-profile service closure; new engineering definition, stored artifacts.
Not global minimum, all-parent acceptance, legal area requirement or live receipt.
"""
from service_component_policy359 import *
import types
from group_readsets359 import build as build359
from group_readsets358 import build as build358
H=ROOT/'semantic_rules357'
REQUIRED=('bath_service_operation','fixture_inventory_use','body_route_sweeps','door_operation','serving_route','bath_nonprivate_access','partition_ledger')

def domain_partition(m,u,serviceids,approach,opening):
 body=F(m['profile']['body_m']);service=[q for k in serviceids for q in source_sweeps(u['routes'][k],body)]
 nonservice=[q for k,p in u['routes'].items()if k not in serviceids for q in source_sweeps(p,body)]
 nonservice += [q for p in u['scenario_routes'].values()for q in source_sweeps(p,body)]
 entry=[rect(q)for q in u['rooms']['entry_circulation']];private=[rect(q)for q in u['rooms']['private_circulation']];bath=[rect(q)for q in u['rooms']['bath']]
 uncovered=difference(entry,service+nonservice)
 private_service=[z for a in private for b in service if(z:=intersection(a,b))]
 exclusive_observed=difference(entry,nonservice+bath)
 residual=difference(exclusive_observed,approach+[opening])
 return {'entry_domain_area_m2':str(union_area(entry)),'entry_uncovered_area_m2':str(union_area(uncovered)),'entry_uncovered_regions':[list(map(str,q))for q in uncovered],'private_service_intersection_m2':str(union_area(private_service)),'exclusive_after_source_clearance_m2':str(union_area(residual)),'exclusive_regions':[list(map(str,q))for q in residual],'complete':not uncovered and not private_service and not residual}

def bound_rows(m,raw,registry):
 cm=types.ModuleType('_service_closure_bound_common');cm.__file__=str(H/'common.py');exec(compile((H/'common.py').read_bytes(),cm.__file__,'exec'),cm.__dict__);cm.REGISTRY_NAME=registry;rows=cm.rows(m,raw)
 for k in REQUIRED:
  r=rows[k];w=r['evidence']['witness']
  if r['status']!='PASS_LIMITED'or w.get('errors')or w.get('pending'):raise ValueError('SERVICE_PREREQUISITE:'+k)
 return rows

def reconcile_scope(partition,classified):
 return partition['complete'] and F(classified['unassigned_after_source_clearance_m2'])==0

def assess(record,result,baseline_record,baseline_result):
 before=digest([record,result,baseline_record,baseline_result]);views=[build358(baseline_record,baseline_result),build359(record,result)]
 models=[baseline_record['candidate']['model'],record['candidate']['model']]
 if baseline_record['candidate']['request']!=record['candidate']['request']or models[0]['program']!=models[1]['program']or models[0]['profile']!=models[1]['profile']:raise ValueError('SAME_BRIEF_PROGRAM_PROFILE')
 evidence=[]
 for m,v,registry in zip(models,views,['method_registry_source358.json','method_registry_source359.json']):
  rows=bound_rows(m,v['result']['raw_fresh_report'],registry);measured=measure(m);cs=classify(m,measured);per=[]
  for r,c in zip(measured,cs):
   uid=r['unit'];u=next(u for u in m['units']if u['id']==uid);p=next(p for p in m['module_placements']if p['unit_id']==uid and p['room_id']=='bath');approach=[transformed_rect(q,p['transform'])for q in p['module']['unit']['rooms']['public_access']];o=next(o for o in m['openings']if o['id']==uid+'.bath')
   if set(r['service_target_ids'])!=set(p['module']['unit']['activities']):raise ValueError('SERVICE_TARGET_INVENTORY')
   checked=rows['serving_route']['evidence']['witness']['routes']
   for name in u['scenario_routes']:
    if not any(q['unit']==uid and q['route']==name and F(q['body_width'])==F(m['profile']['body_m'])for q in checked):raise ValueError('UNCHECKED_SOURCE_SCENARIO')
   for name in u['routes']:
    if name in u['activities'] and not any(q['unit']==uid and q['route']==name and F(q['body_m'])==F(m['profile']['body_m'])for q in rows['body_route_sweeps']['evidence']['witness']['routes']):raise ValueError('UNCHECKED_REQUIRED_ROUTE')
   partition=domain_partition(m,u,r['service_target_ids'],approach,rect(o['rect']));per.append({'unit':uid,'bath_union_m2':r['bath_union_m2'],'source_service_program_hash':digest({'module':p['module'],'activities':sorted(p['module']['unit']['activities'])}),'ownership':u['ownership'],'partition':partition,'outside_entry_service_reconciled':reconcile_scope(partition,c),'outside_entry_unassigned_m2':c['unassigned_after_source_clearance_m2'],'source_approach_and_opening_exact':c['source_approach_exact_transform']and c['real_opening_source_binding']})
  evidence.append({'model_digest':digest(m),'source_row_digests':{k:digest(rows[k])for k in REQUIRED},'group_digest':digest(v['groups']),'units':per})
 outcomes=[]
 for now in evidence[1]['units']:
  old=next(u for u in evidence[0]['units']if u['unit']==now['unit']);same=old['source_service_program_hash']==now['source_service_program_hash']and old['ownership']==now['ownership'];complete=same and old['outside_entry_service_reconciled'] and now['outside_entry_service_reconciled'];smallest=min(F(old['bath_union_m2']),F(now['bath_union_m2']));excess=F(now['bath_union_m2'])-smallest
  outcomes.append({'unit':now['unit'],'same_validated_service_program':same,'tested_cohort_min_room_m2':str(smallest),'current_room_excess_m2':str(excess),'R_service_percent':measure_model(models[1])['units'][now['unit']]['service_ratio_percent'],'A_unit_net_m2':measure_model(models[1])['units'][now['unit']]['unit_net_m2'],'additional_exclusive_circulation_m2':'0'if complete else None,'verdict':'PASS_SCOPED_FINITE_SERVICE_COMPACTNESS'if complete and excess==0 else 'UNKNOWN','scope':'BOUND_SOURCE117_SERVICE_PROGRAM; COMPLETE_DECLARED_ENTRY_CIRCULATION_PARTITION; SOURCE_PRIVATE_DOMAIN_HAS_NO_SERVICE_TRAVERSAL; NO_GLOBAL_MINIMUM'})
 if before!=digest([record,result,baseline_record,baseline_result]):raise ValueError('INPUT_MUTATION')
 return {'schema':'ENGINEERING359_SERVICE_COMPACTNESS_CLOSURE','verdict':'PASS_SCOPED_FINITE_SERVICE_COMPACTNESS'if all(u['verdict'].startswith('PASS_')for u in outcomes)else'UNKNOWN','units':outcomes,'evidence':evidence,'source274_required_subclaims':next(r for r in json.loads((ROOT/'staging274_evaluator_transport_fix/quality_contract.json').read_text())['rules']if r['id']=='SERVICE_COMPACTNESS'),'source_formula':'R_service=100*A_bath_WC_union/A_unit_net; combined room counted once; A_exclusive_service_circulation separately reconciled; finite actually validated baseline not theoretical minimum','source274_rule_sha256':hashlib.sha256((ROOT/'staging274_evaluator_transport_fix/quality_contract.json').read_bytes()).hexdigest(),'definition':'Exact cellwise circulation coverage. Shared atoms require actual nonservice traversal. Sole-service atoms must be wholly source-bound service approach/threshold; otherwise explicit additional exclusive area or unknown. Internal source bath bundle counted once.','engineering_scope_exclusions':['Private nonservice tail necessity remains Q04','Unassigned public noncirculation floor purpose remains Q11','No assertion of global service minimum'],'live_authority':False,'new_fresh_execution':False,'all_parent_acceptance':False,'audit_status':'PENDING_DEFINITION_AUDIT'}
if __name__=='__main__':
 args=[json.loads((ROOT/p).read_text())for p in ['staging359_hall_clamp/actual359.json','review359_source_validation/result.json','staging358_comparative/row_candidate358.json','review358_source_validation/result.json']];out=assess(*args);Path(__file__).with_name('service_closure_actual359.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(out['verdict'],out['units'])
