"""Pure full-band counterexample using current candidate request, after own gate."""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from comparison_metrics import digest,rectangle_union_area
ROOT=Path(__file__).resolve().parents[1]
def full_band_current(record):
 p=ROOT/'staging358_core_branch/actual_full_band358.json';source=json.loads(p.read_text());receipt=json.loads((ROOT/'finite_comparison358/core_branch_bound358.json').read_text())
 if hashlib.sha256(p.read_bytes()).hexdigest()!=receipt['artifact_sha256']:raise ValueError('FULL_BAND_ARTIFACT_CHANGED')
 if record['candidate']['request']!=source['raw']or digest(source['full_band_core'])!=source['full_band_core_digest']:raise ValueError('FULL_BAND_INPUT_SOURCE_BINDING')
 for name,h in source['source_before'].items():
  if hashlib.sha256((ROOT/'planha_general150_runtime_work'/name).read_bytes()).hexdigest()!=h or source['source_after'].get(name)!=h:raise ValueError('FULL_BAND_SOURCE_CHANGED')
 # Re-run only the pure exact primitive, no solver/constructor/full-plan/fresh.
 import sys
 sys.path.insert(0,str(ROOT/"planha_general150_runtime_work"))
 from contract114 import full_band_core_first
 raw=record['candidate']['request'];primitive=full_band_core_first(F(raw['W']),F(raw['L']))
 if digest(primitive)!=source['full_band_core_digest']:raise ValueError('FULL_BAND_PRIMITIVE_REPLAY')
 rows=[]
 for u in record['candidate']['model']['units']:
  regions=primitive.get('unit_ownership',{}).get(u['id'],[primitive['units'][u['id']]]);current=rectangle_union_area(u['ownership']);alternate=rectangle_union_area(regions)
  if alternate>=current:raise ValueError('NO_PROTECTED_OWNERSHIP_COUNTEREXAMPLE')
  rows.append({'unit':u['id'],'current_regions_digest':digest(u['ownership']),'alternative_regions_digest':digest(regions),'current_exact_m2':str(current),'alternative_exact_m2':str(alternate),'loss_exact_m2':str(current-alternate)})
 return {'artifact_sha256':receipt['artifact_sha256'],'primitive_digest':digest(primitive),'current_model_digest':digest(record['candidate']['model']),'rows':rows,'pure_primitive_reexecuted':True,'terminal_state':'EXCLUDED_ONLY_FROM_PROTECTED_NONDECREASING_OWNERSHIP_DOMAIN','global_infeasibility':False,'full_plan_constructed':False}
