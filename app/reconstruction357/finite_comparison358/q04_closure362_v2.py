"""Bound finite closure v2. COMMON role remains independently unresolved."""
from q04_closure362 import *

def bind_cohort(record):
 ledger=json.loads((HERE/'bound_comparison_actual358.json').read_text());bound=[]
 for member in ledger['members']:
  p=ROOT/member['artifact'];r=json.loads(p.read_text())
  if hashlib.sha256(p.read_bytes()).hexdigest()!=member['artifact_sha256']:raise ValueError('COHORT_ARTIFACT_CHANGED')
  c=r['selected'][0]if member['id']=='baseline351'else r['candidate']
  if digest(c['model'])!=member['model_digest']:raise ValueError('COHORT_MODEL_CHANGED')
  bound.append({'member':member['id'],'artifact_sha256':member['artifact_sha256'],'model_digest':member['model_digest']})
 old=json.loads((ROOT/'staging359_hall_clamp/actual359.json').read_text())
 if digest(old)!=record['trace']['parent_record_digest']or digest(old['candidate']['model'])!=record['trace']['parent_model_digest']:raise ValueError('CLAMPED359_PARENT_CHANGED')
 bound.append({'member':'clamped359','record_digest':digest(old),'model_digest':digest(old['candidate']['model'])})
 return bound

def full_band_current(record):
 p=ROOT/'staging358_core_branch/actual_full_band358.json';source=json.loads(p.read_text());receipt=json.loads((HERE/'core_branch_bound358.json').read_text())
 if hashlib.sha256(p.read_bytes()).hexdigest()!=receipt['artifact_sha256']:raise ValueError('FULL_BAND_ARTIFACT_CHANGED')
 if record['trace']['raw']!=source['raw']or digest(source['full_band_core'])!=source['full_band_core_digest']:raise ValueError('FULL_BAND_INPUT_SOURCE_BINDING')
 for name,h in source['source_before'].items():
  if hashlib.sha256((ROOT/'planha_general150_runtime_work'/name).read_bytes()).hexdigest()!=h or source['source_after'].get(name)!=h:raise ValueError('FULL_BAND_SOURCE_CHANGED')
 # Re-run only the pure exact primitive, no solver/constructor/full-plan/fresh.
 import sys
 sys.path.insert(0,str(ROOT/"planha_general150_runtime_work"))
 from contract114 import full_band_core_first
 raw=record['trace']['raw'];primitive=full_band_core_first(F(raw['W']),F(raw['L']))
 if digest(primitive)!=source['full_band_core_digest']:raise ValueError('FULL_BAND_PRIMITIVE_REPLAY')
 rows=[]
 for u in record['candidate']['model']['units']:
  regions=primitive.get('unit_ownership',{}).get(u['id'],[primitive['units'][u['id']]]);current=rectangle_union_area(u['ownership']);alternate=rectangle_union_area(regions)
  if alternate>=current:raise ValueError('NO_PROTECTED_OWNERSHIP_COUNTEREXAMPLE')
  rows.append({'unit':u['id'],'current_regions_digest':digest(u['ownership']),'alternative_regions_digest':digest(regions),'current_exact_m2':str(current),'alternative_exact_m2':str(alternate),'loss_exact_m2':str(current-alternate)})
 return {'artifact_sha256':receipt['artifact_sha256'],'primitive_digest':digest(primitive),'current_model_digest':digest(record['candidate']['model']),'rows':rows,'pure_primitive_reexecuted':True,'terminal_state':'EXCLUDED_ONLY_FROM_PROTECTED_NONDECREASING_OWNERSHIP_DOMAIN','global_infeasibility':False,'full_plan_constructed':False}

HERE=Path(__file__).resolve().parent
_previous_evaluate=evaluate
def evaluate(record,review):
 cohort=bind_cohort(record);core=full_band_current(record);out=_previous_evaluate(record,review)
 out['schema']='Q04_CURRENT362_BOUND_CLOSURE_V2';out['bound_cohort']=cohort;out['full_band_current_proof']=core
 out['remaining']=[r for r in out['remaining']if r!='INDEPENDENT_FINITE_DOMAIN_AND_COMMON_COST_POLICY_AUDIT_PENDING']
 out['finite_policy_audit']={'status':'INDEPENDENT_SCOPED_AUDIT_CONFIRMED','scope':'12 active branches plus fixed transforms and notch; explicit post-observation common-area engineering cost. Not all sourceparameter domains or wholeQ04.','common_role_not_included':True}
 return out
