"""Independently remeasure supplied source-produced core branch artifact."""
from build_ledger import *
from comparison_metrics import rectangle_union_area
from fractions import Fraction as F
p=ROOT/'staging358_core_branch/actual_full_band358.json';x=json.loads(p.read_text());c=json.loads((ROOT/'staging358_comparative/row_candidate358.json').read_text())['candidate'];assert digest(c['model'])==x['current_model_digest'];assert digest(c['request'])==x['raw_digest'];assert digest(x['compact_core'])==x['current_core_digest'];assert digest(x['full_band_core'])==x['full_band_core_digest']
for name,h in x['source_before'].items():
 assert hashlib.sha256((ROOT/'planha_general150_runtime_work'/name).read_bytes()).hexdigest()==h==x['source_after'][name]
proof=[]
for row in x['ownership_rows']:
 u=next(u for u in c['model']['units']if u['id']==row['unit']);assert digest(u['ownership'])==digest(row['before_regions'])
 before=rectangle_union_area(row['before_regions']);after=rectangle_union_area(row['after_regions']);assert str(before)==row['before_exact_m2'] and str(after)==row['after_exact_m2'] and after<before
 proof.append({'unit':u['id'],'before_m2':str(before),'after_m2':str(after),'loss_m2':str(before-after)})
out={'schema':'FULL_BAND358_BRANCH_PROTECTED_COUNTEREXAMPLE','artifact_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'artifact':str(p.relative_to(ROOT)),'model_digest':digest(c['model']),'independently_remeasured':proof,'terminal_state':'INELIGIBLE_FOR_DECLARED_NONDECREASING_OWNERSHIP_COMPARISON_DOMAIN','intrinsically_invalid':False,'global_infeasible':False,'full_plan_constructed':False,'adapter_status':x['adapter_status'],'policy_authority':'ENGINEERING358_CONSERVATIVE_COMPARATIVE_DOMAIN_NOT_UNIVERSAL_OWNER_MINIMUM','parent_acceptance':False,'source_binding':'CURRENT_FROZEN_SOURCE114_PRIMITIVE_ARTIFACT_AND_UNCHANGED_SOURCE_HASHES'}
Path(__file__).with_name('core_branch_bound358.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(proof)
