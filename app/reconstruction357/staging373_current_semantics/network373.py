"""New current-view gate around unchanged365 network kernel; no old verdict reuse."""
from gate373 import validate_views,D

def evaluate(envelope,result,prerequisites,seconds):
 validate_views(envelope,result)
 rawrows={r['requirement_id']:r for r in result['raw_fresh_report']['rule_contract_evidence']['requirements']}
 for g in prerequisites:
  r=rawrows[g['requirement_id']]
  if g.get('row_hash')!=D(r)or g.get('witness_hash')!=D(r['evidence']['witness']):raise ValueError('GROUP_BINDING')
 from network365 import _kernel
 return _kernel(envelope,result,prerequisites,seconds)
