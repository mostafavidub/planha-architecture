"""All named historical alternatives retained; new finite rank2 stays unassessed."""
import ast,json,hashlib,sys
from fractions import Fraction as F
from pathlib import Path
from gate381 import ROOT,D,validate
SEM=ROOT/'semantic_rules357'
def read(path):return json.loads((ROOT/path).read_text())
def kernels():
 import comparison_metrics as metrics
 ns={'F':F,**{k:getattr(metrics,k)for k in('measure_model','route_metrics','rectangle_union_area')}}
 for path,names in [('finite_comparison358/q04_closure359.py',{'dimensions'}),('finite_comparison365/q04_closure365_v7.py',{'objective','compare'})]:
  code=(ROOT/path).read_text();nodes=[n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef)and n.name in names]
  if {n.name for n in nodes}!=names:raise ValueError('UNCHANGED_COMPARISON_FUNCTIONS')
  exec(compile(ast.Module(body=nodes,type_ignores=[]),'<UNCHANGED_Q04>','exec'),ns)
 return ns

def evaluate(record,fresh):
 binding=validate(record,fresh);m=record['candidate']['model'];ns=kernels();pairs=[];ledger=read('finite_comparison358/bound_comparison_actual358.json')
 first={x['id']:x for x in ledger['members']}
 definitions=[('baseline351','actual_run/actual_response.json',None,None),('translated357','staging357_comparative/attached_service_final357.json','review357_source_validation/result.json','eligibility_intrinsic_actual357_finalpin.json'),('row358','staging358_comparative/row_candidate358.json','review358_source_validation/result.json','eligibility_intrinsic_actual358.json'),('clamped359','staging359_hall_clamp/actual359.json','review359_source_validation/result.json','eligibility_intrinsic_actual359.json'),('notched362','staging362_core_notch/actual362.json','review362_source_validation/result.json','eligibility_intrinsic_actual362.json'),('service_anchor365','staging365_service_grammar/candidate365.json','review365_service_source_validation/result.json','eligibility_intrinsic_service_actual365.json'),('balanced365','staging365_balanced_portals/actual365.json','review365_balanced_source_validation/result.json','eligibility_intrinsic_actual365.json'),('joint367','review367_joint_attempt2/actual367.json','review367_joint_source_validation_attempt2/result.json','eligibility_intrinsic_actual367.json')]
 for name,path,fp,ep in definitions:
  r=read(path);c=r['selected'][0]if name=='baseline351'else r['candidate'];bm=c['model'];eligible=False;why=[]
  if c['request']!=record['candidate']['request']or any(bm[k]!=m[k]for k in('program','profile','inputs')):raise ValueError('SAME_BRIEF_PROGRAM_PROFILE:'+name)
  if name=='baseline351':
   row=first[name];e=row['eligibility'];proof=e['result']
   if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=row['artifact_sha256']or D(bm)!=row['model_digest']or D(proof)!=e['result_digest']:raise ValueError('BASE351_LEDGER_BINDING')
   eligible=proof['verdict']=='PASS'and proof['eligible']and proof['evidence']['model_digest']==D(bm)
   history={'type':'PINNED_OLD_LEDGER_INTRINSIC_PROOF','proof':proof,'ledger_digest':D(ledger),'recomputed':False}
  else:
   bf=read(fp);proof=read('semantic_rules357/'+ep)
   if bf['input_record_digest']!=D(r)or bf['model_digest']!=D(bm)or proof['evidence']['record_digest']!=D(r)or proof['evidence']['new_result_digest']!=D(bf)or proof['evidence']['model_digest']!=D(bm):raise ValueError('BASELINE_OWN_FRESH_ELIGIBILITY:'+name)
   eligible=proof['verdict']=='PASS'and proof['eligible'];history={'type':'PINNED_OWN_FRESH_AND_INTRINSIC_PROOF','fresh_digest':D(bf),'proof':proof,'recomputed':False}
  comparison=ns['compare'](m,bm)
  pairs.append({'id':name,'artifact':path,'artifact_sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'model_digest':D(bm),'eligible':eligible,'historical_eligibility':history,'comparison':comparison,'retained':True})
 sys.path.insert(0,str(ROOT/'finite_comparison358'));from q04_closure362_v2 import full_band_current
 fullband=full_band_current(record)
 sys.path.insert(0,str(ROOT/'finite_comparison367'));from source_property366 import evaluate as draft366
 joint=read('review367_joint_attempt2/actual367.json');draft=draft366(joint)
 from comparison_metrics import rectangle_union_area
 area=rectangle_union_area(m['common_spaces']['lobby'])
 if area!=rectangle_union_area(joint['candidate']['model']['common_spaces']['lobby']):raise ValueError('DRAFT366_CURRENT_AREA_REBIND')
 draft.update(current_model_digest=D(m),current=str(area),binding_note='Exact measured common area equals bound367 value; source property only, no366 construction or eligibility claim.')
 failed=read('staging364_balanced_portals/actual364.json');diag=read('review364_diagnostic/geometry_operations.json')
 from family378 import enumerate_family,load_parent
 choices=enumerate_family(load_parent())
 return {'schema':'CURRENT378_NAMED_HISTORICAL_COHORT381','binding':binding,'pairs':pairs,'all_named_historical_pairs_recomputed':len(pairs)==8,'all_named_historical_dominance_refuted':all(x['comparison']['dominance']=='FALSE'for x in pairs),'all_historical_eligibility_bound':all(x['eligible']for x in pairs),'historical_eligibility_recomputed':False,'current_intrinsic_source':'RECOMPUTED_ESSENTIAL381_CURRENT379_IN_SAME_SEMANTIC_RUN','full_band_current':fullband,'draft366_conditional_property':draft,'failed364_retained':{'record_digest':D(failed),'diagnostic_digest':D(diag),'operation_result':diag['door_operations'],'eligible':False,'global_infeasibility_claimed':False},'new_finite_family':{'choices':choices,'rank0':'ORIGINAL_MIDPOINT365_COMPARISON_RETAINED','rank1':'CURRENT378_ACTUAL_SCOPED_PASS','rank2':'UNASSESSED_NO_MODEL_NO_FRESH_NO_DOMINANCE_PROOF'},'remaining':['REGISTERED_FINITE378_RANK2_NOT_CONSTRUCTED_OR_REVIEWED'],'scope_exclusions':['CONTINUOUS_DOMAIN_AND_GLOBAL_OPTIMALITY_NOT_CLAIMED'],'full_q04_closed':False,'verdict':'UNKNOWN_NEW_FINITE_MEMBER_UNASSESSED','global_optimum':False,'accepted':False}
