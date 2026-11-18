import json,sys,traceback,ast
from pathlib import Path
from fractions import Fraction as F
from contract376 import ROOT,W,digest,bind,decision,partial
mode,folder,budget,run_id=sys.argv[1:];P=Path(folder);budget=float(budget)
read=lambda n:json.loads((P/n).read_text())
def write(n,v):
 with(P/n).open('x')as f:json.dump(v,f,indent=2)
def failure(t,e,tb):
 write(mode+'_error.json',{'type':t.__name__,'message':str(e),'traceback':''.join(traceback.format_exception(t,e,tb))});sys.__excepthook__(t,e,tb)
sys.excepthook=failure
if mode=='construct':
 sys.path.insert(0,str(ROOT/'staging369_current_source_validation'))
 from source369 import construct
 parent=json.loads((ROOT/'staging369_controlled_cycle/parent368.json').read_text());envelope=read('request.json')
 if digest(parent['candidate']['request'])!=envelope['raw_digest']:raise ValueError('PARENT_REQUEST')
 write('fixture_record.json',construct(parent,'sofa1_use','-3/2','0',purpose='CONTROLLED_TEST_FIXTURE'))
elif mode in ('fresh_first','fresh_second'):
 sys.path.insert(0,str(ROOT/'staging369_current_source_validation'))
 from evaluate369 import evaluate369
 record=read('fixture_record.json'if mode=='fresh_first'else'repaired_record.json')
 fresh=evaluate369(record,min(90,budget));write(mode+'.json',fresh)
 write(mode+'_binding.json',bind(read('request.json'),record,fresh,run_id,lineage=read('lineage.json')if mode=='fresh_second'else None))
elif mode=='propose':
 sys.path.insert(0,str(ROOT/'staging372_route_aware_repair'))
 from operator372 import propose
 fresh=read('fresh_first.json')
 if decision(fresh['raw_report'])!='REQUIRES_BOUND_OPERATOR_GATE':raise ValueError('NO_REPAIR_DISPATCH')
 plan=propose(read('fixture_record.json'),fresh,read('fresh_first_binding.json'));write('plan.json',plan)
 if plan['status']!='RECONSTRUCTION_AND_FRESH_REVIEW_REQUIRED':raise ValueError('PROPOSAL_NOT_PREPARED')
elif mode=='reconstruct':
 sys.path.insert(0,str(ROOT/'staging372_route_aware_repair'))
 from reconstruct372 import reconstruct
 out=reconstruct(read('fixture_record.json'),read('plan.json'),run_id,ROOT)
 write('repaired_record.json',out['record']);write('lineage.json',out['lineage'])
elif mode=='compare':
 sys.path.insert(0,str(ROOT/'staging372_route_aware_repair'))
 from verify372 import compare as regression
 a,b=read('fresh_first.json'),read('fresh_second.json');child=read('repaired_record.json');lineage=read('lineage.json')
 guard=regression(read('fixture_record.json'),a,read('plan.json'),child,b,lineage);write('regression.json',guard)
 if not guard['mechanics_success']:raise ValueError('REPAIR_REGRESSION_NOT_VERIFIED')
 second=read('fresh_second_binding.json')
 if any(second[k]!=lineage[k]for k in ('run_id','candidate_id','model_digest','record_digest')):raise ValueError('SECOND_REVIEW_LINEAGE_IDENTITY')
 if a['review_id']==b['review_id']or a['model_digest']==b['model_digest']:raise ValueError('NEW_REVIEW_AND_MODEL_REQUIRED')
 lineage.update(review_id=b['review_id'],fresh_digest=digest(b),fresh_review_required=False,source_replay_required=False,test_only=True);write('reviewed_lineage.json',lineage)
 # Unchanged exact Q04 coordinate definitions and comparison, not an ad hoc score.
 ns={'F':F};path=ROOT/'semantic_rules357/comparison_metrics.py';exec(compile(path.read_text(),str(path),'exec'),ns)
 for rel,names in [('finite_comparison358/q04_closure359.py',{'dimensions'}),('finite_comparison365/q04_closure365_v7.py',{'objective','compare'})]:
  path=ROOT/rel;nodes=[n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef)and n.name in names]
  if {n.name for n in nodes}!=names:raise ValueError('Q04_FUNCTIONS')
  exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)
 base=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());bf=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());elig=json.loads((ROOT/'semantic_rules357/eligibility_intrinsic_actual365.json').read_text())
 if elig['evidence']['record_digest']!=digest(base)or elig['evidence']['new_result_digest']!=digest(bf)or elig['verdict']!='PASS'or not elig['eligible']:raise ValueError('BASELINE_ELIGIBILITY')
 m=child['candidate']['model'];bm=base['candidate']['model']
 if child['candidate']['request']!=base['candidate']['request']or m['program']!=bm['program']or m['profile']!=bm['profile']:raise ValueError('COHORT_BRIEF')
 q=ns['compare'](m,bm);write('quality_comparison.json',{'comparison':q,'current_model_digest':digest(m),'current_fresh_digest':digest(b),'current_review_id':b['review_id'],'baseline_model_digest':digest(bm),'baseline_eligibility_reused':True,'current_intrinsic_not_executed':True})
 state='QUALITY_UNRESOLVED'if q['dominance']=='UNKNOWN'else'REPAIR_REVIEWED_FULL_QUALITY_NOT_ESTABLISHED'
 out=partial(state,run_id);out.update(request_digests={k:read('request.json')[k]for k in ('received_digest','raw_digest','canonical_request_digest')},repair_attempted=True,same_run_construction_and_fresh=True,fresh_count=2,initial_binding=read('fresh_first_binding.json'),repaired_lineage=lineage,raw_first_status=a['raw_report']['status'],raw_second_status=b['raw_report']['status'],second_binding=second,current_errors=b['raw_report']['errors'],current_pending=b['raw_report']['pending'],original_pending=b['raw_report'].get('original_pending',[]),comparison=q,prior_qualified_reference={'kind':'balanced365','model_digest':digest(bm),'information_only':True,'selected':False},semantic_state='UNKNOWN_NOT_EXECUTED_COMPARATIVE_SHORT_CIRCUIT'if q['dominance']=='UNKNOWN'else'UNKNOWN_NOT_EXECUTED')
 write('result.json',out)
else:raise ValueError('PHASE')
