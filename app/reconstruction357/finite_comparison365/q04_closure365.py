"""PolicyV365 post-observation refinement: all four common-route task costs.
New current-source artifact; no source362 receipt becomes source365 authority.
"""
import sys,json,hashlib,importlib.util
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'finite_comparison358'),str(ROOT/'semantic_rules357')]
from comparison_metrics import digest,rectangle_union_area,route_metrics
from q04_closure359 import dimensions,purpose_complete
from branch_registry362 import build as registry362
from group_readsets365_v2 import build as group365
from circulation_role365 import evaluate as role365
from q04_closure362_v2 import full_band_current

def read(path):
 p=ROOT/path;return json.loads(p.read_text()),{'path':path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def objective(model):
 values=dimensions(model);values['COMMON/lobby_floor_m2']=rectangle_union_area(model['common_spaces']['lobby']);bindings={};required={s+'_'+u['id']for s in ('stair','lift')for u in model['units']}
 if set(model['common_routes'])!=required:raise ValueError('FULL_COMMON_ROUTE_INVENTORY')
 opens={o['id']:o for o in model['openings']}
 for name,path in sorted(model['common_routes'].items()):
  src,uid=name.split('_');p,q=opens[src+'.entry'],opens[uid+'.entry'];a,b,c,d=map(F,p['rect']);x,y,X,Y=map(F,q['rect']);start=list(map(F,path[0]));end=list(map(F,path[-1]));center=((a+c)/2,(b+d)/2);target=((x+X)/2,(y+Y)/2)
  metric=route_metrics(path);values['COMMON/'+name+'/length']=F(metric['length']);values['COMMON/'+name+'/turns']=F(metric['direction_changes'])
  bindings[name]={'task':[src,uid],'start_offset_from_source_portal_midplane':[str(start[i]-center[i])for i in range(2)],'end_offset_from_unit_portal_midplane':[str(end[i]-target[i])for i in range(2)],'body_profile':model['profile']['body_m'],'source_aperture_width':str(max(c-a,d-b)),'destination_aperture_width':str(max(X-x,Y-y)),'scenario':'CONCEPT_REQUIRED_COMMON_TRANSFER_WITH_SOURCE_INTERIOR_POSE_ANCHORS','path':path}
 return values,bindings

def compare(current,alternate):
 a,ca=objective(current);b,cb=objective(alternate)
 if set(a)!=set(b)or set(ca)!=set(cb):raise ValueError('OBJECTIVE_TASK_INVENTORY_CHANGED')
 for name in ca:
  if {k:v for k,v in ca[name].items()if k!='path'}!={k:v for k,v in cb[name].items()if k!='path'}:raise ValueError('COMPARABLE_POINTS_OR_SCENARIO_CHANGED:'+name)
 worse=[{'metric':k,'current':str(a[k]),'alternative':str(b[k]),'alternative_increase':str(b[k]-a[k])}for k in sorted(a)if b[k]>a[k]]
 return {'dominance':'FALSE'if worse else'UNKNOWN','strict_worse_witnesses':worse,'alternative_improvements':[{'metric':k,'current':str(a[k]),'alternative':str(b[k])}for k in sorted(a)if b[k]<a[k]],'all_common_task_bindings':cb,'all_dimension_count':len(a),'unknown_protected_metrics_not_promoted':True}

def evaluate(record,review):
 before=digest([record,review]);view=group365(record,review,source_profile='SOURCE_BALANCED365');m=record['candidate']['model'];values,bindings=objective(m);pairs=[]
 for name,path in [('baseline351','actual_run/actual_response.json'),('translated357','staging357_comparative/attached_service_final357.json'),('row358','staging358_comparative/row_candidate358.json'),('clamped359','staging359_hall_clamp/actual359.json'),('notched362','staging362_core_notch/actual362.json')]:
  x,pin=read(path);c=x['selected'][0]if name=='baseline351'else x['candidate']
  if c['request']!=record['candidate']['request']or c['model']['program']!=m['program']or c['model']['profile']!=m['profile']:raise ValueError('SAME_BRIEF_PROGRAM_PROFILE')
  pairs.append({'id':name,'artifact':pin,'model_digest':digest(c['model']),'comparison':compare(m,c['model'])})
 domains=registry362();failed,fp=read('staging364_balanced_portals/actual364.json');diag,dp=read('review364_diagnostic/geometry_operations.json');selector,sp=read('review365_launcher/selector_preselection.json')
 branch={'id':'BALANCED_PORTAL_SOURCE365_DETERMINISTIC_OPERATION_DOMAIN_SELECTOR','source':'staging365_balanced_portals/selector365.py','source_sha256':hashlib.sha256((ROOT/'staging365_balanced_portals/selector365.py').read_bytes()).hexdigest(),'current_source_trace_digest':digest(record['trace']),'selection_evidence':sp,'selection_result':selector,'historical_failed_prototype':{'record':fp,'model_digest':digest(failed['candidate']['model']),'primitive_evidence':dp,'operation_result':diag['door_operations'],'status':'FAILED_OPERATION_PROTOTYPE_RETAINED_NOT_ELIGIBLE'},'version_relation':'Same balanced-portal family, NOT identical parameters: 364 chose a boundary without operation-domain viability; 365 selects midpoint from source obstacle/operation feasible interval. No claim all continuous parameter alternatives exhausted.'}
 role=role365(record,review);coreproof=full_band_current(record);pending=[];gate=None
 gatepath=ROOT/'semantic_rules357/eligibility_intrinsic365.py'
 if not gatepath.exists():pending.append('CURRENT365_INTRINSIC_CALLBACK_NOT_YET_IMPLEMENTED')
 else:
  spec=importlib.util.spec_from_file_location('_current365_eligibility',gatepath);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);gate=module.evaluate(record,review,seconds=30)
  if gate.get('verdict')!='PASS'or not gate.get('eligible'):pending.append('CURRENT365_INTRINSIC_CALLBACK_NOT_PASS')
 if not purpose_complete(role):pending.append('CURRENT365_PRIVATE_ENTRY_PURPOSE_NOT_CLOSED')
 pending+=['CURRENT365_COMMON_ROLE_NOT_YET_BOUND','NEW_POLICY_DOMAIN_AND_TRANSITIVE_FREEZE_AUDIT_PENDING']
 if any(x['comparison']['dominance']!='FALSE'for x in pairs):pending.append('UNRESOLVED_COMPARATIVE_ALTERNATIVE')
 if before!=digest([record,review]):raise ValueError('INPUT_MUTATION')
 return {'schema':'Q04_POLICY_V365_CURRENT_SOURCE_PENDING','verdict':'UNKNOWN','remaining':pending,'model_digest':digest(m),'record_digest':digest(record),'fresh_result_digest':digest(review),'source_profile':'SOURCE_BALANCED365','group_digest':digest(view['groups']),'current_intrinsic_gate':gate,'current_role':role,'current_full_band_source_proof':coreproof,'all_objectives':{k:str(v)for k,v in values.items()},'current_common_task_bindings':bindings,'alternatives':pairs,'prior_domain':domains,'new_balanced_branch':branch,'policy':'Post-observation engineering refinement V365 includes ALL source-required unit route costs, unit circulation union, common lobby union, and all four common-route lengths/turns with matched source/destination pose offsets/profile/scenario. No cherry-picked lift-only improvement or invented negligible tolerance.','tradeoff':'Current balanced stairs are longer than362 while lift tasks shorten; this is not Pareto improvement across all access tasks.','accepted':False,'all_parent_acceptance':False,'new_fresh_execution':False,'global_optimum':False}
if __name__=='__main__':
 r,_=read('staging365_balanced_portals/actual365.json');f,_=read('review365_balanced_source_validation/result.json');out=evaluate(r,f);p=HERE/'q04_current365_pending_v2.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2));print(out['remaining'])
