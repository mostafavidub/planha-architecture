"""Authorized exact read-only Q04 diagnostic; no intrinsic/full DAG execution."""
import ast,hashlib,json,sys
from pathlib import Path
from fractions import Fraction as F
W=Path(__file__).resolve().parent.parent;R=W/'reconstruction357';P=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'staging373_current_semantics'))
from gate373 import load_inputs,validate,D
I=load_inputs();binding=validate(I['record'],I['fresh'],I['lineage'])
freeze=json.loads((W/'review373_preaudit/source_freeze.json').read_text())['files']
def checked(path):
 p=R/path;b=p.read_bytes();key=str(p.relative_to(W))
 if hashlib.sha256(b).hexdigest()!=freeze[key]:raise ValueError('PINNED_SOURCE_OR_BASELINE_CHANGED:'+key)
 return b
base=json.loads(checked('staging365_balanced_portals/actual365.json'));bf=json.loads(checked('review365_balanced_source_validation/result.json'));be=json.loads(checked('semantic_rules357/eligibility_intrinsic_actual365.json'))
if bf['input_record_digest']!=D(base)or bf['model_digest']!=D(base['candidate']['model'])or be['evidence']['record_digest']!=D(base)or be['evidence']['new_result_digest']!=D(bf)or be['verdict']!='PASS'or not be['eligible']:raise ValueError('BASELINE_ELIGIBILITY_BINDING')
if any(base['candidate'][k]!=I['record']['candidate'][k]for k in ('request',)):raise ValueError('SAME_REQUEST')
for k in ('program','profile'):
 if base['candidate']['model'][k]!=I['record']['candidate']['model'][k]:raise ValueError('SAME_PROGRAM_PROFILE')
metrics={};exec(compile(checked('semantic_rules357/comparison_metrics.py'),'<PINNED_COMPARISON_METRICS>','exec'),metrics)
ns={'F':F,**{k:metrics[k]for k in ('measure_model','route_metrics','rectangle_union_area')}}
extracted={}
for path,names in [('finite_comparison358/q04_closure359.py',{'dimensions'}),('finite_comparison365/q04_closure365_v7.py',{'objective','compare'})]:
 code=checked(path).decode();nodes=[n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef)and n.name in names]
 if {n.name for n in nodes}!=names:raise ValueError('EXTRACTION_INVENTORY')
 for n in nodes:extracted[n.name]={'source':path,'source_sha256':hashlib.sha256(code.encode()).hexdigest(),'function_sha256':hashlib.sha256(ast.get_source_segment(code,n).encode()).hexdigest()}
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'<UNCHANGED_Q04_FUNCTIONS>','exec'),ns)
a=I['record']['candidate']['model'];b=base['candidate']['model'];result=ns['compare'](a,b);av,ab=ns['objective'](a);bv,bb=ns['objective'](b)
rejected=[]
for stage,recordfile,freshfile in [('369','fixture_record.json','fresh_first.json'),('371','repaired_record.json','fresh.json')]:
 folder=W/('review'+stage+('_current_family_actual_v1'if stage=='369'else'_actual_v1'));r=json.loads((folder/recordfile).read_text());f=json.loads((folder/freshfile).read_text())
 if f['input_record_digest']!=D(r)or f['model_digest']!=D(r['candidate']['model']):raise ValueError('REJECTED_RECORD_BINDING')
 rejected.append({'id':'controlled'+stage,'retained':True,'eligible_for_this_comparison':False,'reason':'ACTUAL_FULL_RAW_FAIL_NOT_INTRINSICALLY_QUALIFIED','record_digest':D(r),'fresh_digest':D(f),'model_digest':f['model_digest'],'raw_status':f['raw_report']['status'],'raw_errors':f['raw_report']['errors'],'pending':f['raw_report']['pending'],'original_pending':f['raw_report']['original_pending']})
out={'schema':'374_EARLY_EXACT_Q04_DIAGNOSTIC','binding':binding,'source_functions':extracted,'current_model_digest':D(a),'alternative_model_digest':D(b),'baseline_record_digest':D(base),'baseline_fresh_digest':D(bf),'baseline_eligibility_digest':D(be),'baseline_eligibility_reused_not_recomputed':True,'current_intrinsic_eligibility_executed':False,'current_eligibility':'UNKNOWN_PENDING_CURRENT_INTRINSIC_GENERATOR','comparison':result,'current_objectives':{k:str(v)for k,v in av.items()},'alternative_objectives':{k:str(v)for k,v in bv.items()},'current_task_bindings':ab,'alternative_task_bindings':bb,'retained_rejected':rejected,'remaining_cohort':['baseline351','translated357','row358','clamped359','notched362','service_anchor365','joint367','draft366_property'],'remaining_cohort_not_executed_or_deleted':True,'decision':'STOP_UNRESOLVED_BASELINE_COMPARISON'if result['dominance']=='UNKNOWN'else'BASELINE_NONDominance_WITNESS_ONLY_FULL_COHORT_AND_INTRINSIC_PENDING','positive_dominance_proven':False,'full_q04_closed':False,'accepted':False,'delivery_allowed':False,'test_only':True}
(P/'result.json').write_text(json.dumps(out,indent=2));print(json.dumps({'comparison':result,'decision':out['decision']},indent=2))
