"""Current379 essential semantic reassessment; unresolved role DAG stays UNKNOWN."""
import ast,json,sys,time,copy
from fractions import Fraction as F
from gate381 import HERE,ROOT,D,validate
SEM=ROOT/'semantic_rules357'
sys.path.insert(0,str(SEM));sys.path.insert(0,str(HERE))
RULES=('SPACE_ACCOUNTING','GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','CIRCULATION_NECESSITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','OPENINGS_REAL','KITCHEN_PROXIMITY','DISTINCTNESS_AND_FAIRNESS')
def q04(model):
 import comparison_metrics as metrics
 ns={'F':F,**{k:getattr(metrics,k)for k in('measure_model','route_metrics','rectangle_union_area')}};sources={}
 for path,names in [('finite_comparison358/q04_closure359.py',{'dimensions'}),('finite_comparison365/q04_closure365_v7.py',{'objective','compare'})]:
  code=(ROOT/path).read_text();nodes=[n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef)and n.name in names]
  if {n.name for n in nodes}!=names:raise ValueError('Q04_EXTRACTION')
  for n in nodes:sources[n.name]={'source':path,'function_digest':D(ast.get_source_segment(code,n))}
  exec(compile(ast.Module(body=nodes,type_ignores=[]),'<UNCHANGED_Q04_FUNCTIONS>','exec'),ns)
 base=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());bf=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());be=json.loads((SEM/'eligibility_intrinsic_actual365.json').read_text());bm=base['candidate']['model']
 if bf['input_record_digest']!=D(base)or bf['model_digest']!=D(bm)or be['evidence']['record_digest']!=D(base)or be['evidence']['new_result_digest']!=D(bf)or not be['eligible']or be['verdict']!='PASS':raise ValueError('BASELINE_ELIGIBILITY_BINDING')
 if any(model[k]!=bm[k]for k in('inputs','program','profile')):raise ValueError('COMPARISON_PROGRAM_PROFILE')
 av,ab=ns['objective'](model);bv,bb=ns['objective'](bm)
 return {'comparison':ns['compare'](model,bm),'source_functions':sources,'current_model_digest':D(model),'baseline_model_digest':D(bm),'baseline_eligibility_digest':D(be),'baseline_eligibility_reused_not_recomputed':True,'current_objectives':{k:str(v)for k,v in av.items()},'baseline_objectives':{k:str(v)for k,v in bv.items()},'current_task_bindings':ab,'baseline_task_bindings':bb,'full_cohort_executed':False,'full_q04_closed':False,'positive_dominance_proven':False,'remaining_cohort_retained':['baseline351','translated357','row358','clamped359','notched362','service_anchor365','joint367','draft366_property'],'scope':'EXACT_BASELINE365_DIAGNOSTIC_NOT_FULL_Q04'}

def run(record,fresh):
 start=time.monotonic();binding=validate(record,fresh);before=D([record,fresh]);m=record['candidate']['model'];raw=fresh['raw_report'];evidence={};errors={}
 import common
 from adapters381 import audit_loaded
 origins_before=audit_loaded()
 common.REGISTRY_NAME='method_registry_source365.json'
 from groups381 import build
 view=build(record,fresh);evidence['nine_prerequisites']=view['groups']
 def capture(key,fn):
  try:evidence[key]=fn()
  except Exception as error:errors[key]=type(error).__name__+':'+str(error)
 from primitive381 import evaluate as primitive
 capture('primitive',lambda:primitive(m,raw,source_profile='SOURCE_BALANCED365',post_fresh={**view,'seconds':10}))
 import closure_openings,intrinsic_access365,room381,eligibility381,bedroom381,author233_spatial_mapping
 capture('openings',lambda:closure_openings.evaluate(m,raw))
 capture('intrinsic_access',lambda:intrinsic_access365.evaluate(m,raw,profile='SOURCE_BALANCED365'))
 capture('intrinsic_eligibility',lambda:eligibility381.evaluate(record,fresh,seconds=30))
 capture('room_program',lambda:room381.evaluate(record,fresh))
 capture('bedroom_grouping',lambda:bedroom381.evaluate(record,fresh,seconds=15))
 capture('q04_baseline365',lambda:q04(m))
 closures=evidence.get('primitive',{}).get('source_closures',{})
 capture('author_mapping',lambda:author233_spatial_mapping.evaluate(view['envelope'],closures.get('living_closure',{}),closures.get('guest_closure',{})))
 base={}
 for module in('modules_structure','modules_spatial','modules_comparison'):
  capture('base_'+module,lambda module=module:__import__(module).evaluate(m,raw))
  base.update(evidence.get('base_'+module,{}))
 missing={
 'SPACE_ACCOUNTING':['CURRENT_FINAL_ROLE_DAG_NOT_PORTED','FULL_Q04_COHORT_NOT_EXECUTED'],
 'CIRCULATION_NECESSITY':['CURRENT_FINAL_ROLE_DAG_NOT_PORTED','FULL_Q04_COHORT_NOT_EXECUTED'],
 'COMMON_CORE_COMPACTNESS':['CURRENT_FINAL_ROLE_DAG_COMMON_Q04_Q12_NOT_PORTED'],
 'PRIVACY_WITHOUT_FAKE_BAFFLE':['CURRENT_WALL_PURPOSE_AND_WHOLE_ROLE_DAG_NOT_PORTED'],
 'SERVICE_COMPACTNESS':['FIXED365_SERVICE_WRAPPER_REQUIRES_CURRENT_SOURCE_ADAPTER'],
 'DISTINCTNESS_AND_FAIRNESS':['ONLY_ONE_BRANCH_OF_TWO_REQUESTED','NO_QUALIFIED_OPTION_SET']}
 quality=[]
 for rid in RULES:
  entry={'rule_id':rid,'verdict':'UNKNOWN','model_digest':binding['model_digest'],'scope':'CURRENT379_STORED_ARTIFACT_ONLY','missing':missing.get(rid,['INDEPENDENT_AUDIT_OF_CURRENT_EVIDENCE_REQUIRED']),'base_result':base.get(rid),'old_parent_pass_reused':False}
  if rid in missing:entry['blocker_kind']='TECHNICAL_INTEGRATION_OR_UNEXECUTED_COMPARISON_NOT_MODEL_VIOLATION'
  keys={'OPENINGS_REAL':'openings','LIVING_USEFUL_CONTIGUITY':'primitive','GUEST_ROUTE_INDEPENDENCE':'primitive','KITCHEN_PROXIMITY':'primitive','ROOM_PROGRAM_CAPACITY':'room_program','BEDROOM_GROUPING':'bedroom_grouping'}
  key=keys.get(rid)
  if key:entry.update(evidence_key=key,evidence_digest=D(evidence[key])if key in evidence else None)
  quality.append(entry)
 origins_after=audit_loaded()
 validate(record,fresh)
 if D([record,fresh])!=before:raise ValueError('INPUT_MUTATION')
 return {'schema':'CURRENT379_ESSENTIAL_SEMANTICS381','binding':binding,'module_origins':{'before':origins_before,'after':origins_after},'quality':quality,'evidence':evidence,'errors':errors,'evidence_bindings':{k:{**binding,'evidence_digest':D(v)}for k,v in evidence.items()},'fresh_checker_executed':False,'construction_executed':False,'semantic_reassessment_executed':True,'semantic_qualification':'UNKNOWN_PENDING_FULL_ROLE_AND_COMPARISON_CLOSURE','accepted':False,'delivery_allowed':False,'request_fulfilled':False,'seconds':time.monotonic()-start}
