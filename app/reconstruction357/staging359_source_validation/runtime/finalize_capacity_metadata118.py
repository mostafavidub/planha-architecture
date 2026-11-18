"""No generation: explicit claim/capacity metadata on saved actual geometry."""
import json
from pathlib import Path
from copy import deepcopy
from public_witness118 import bind_capacity
from checker114 import evaluate
from contract114 import digest
P=Path(__file__).resolve().parent
before=json.loads((P/'evidence/capacity118_whole18x24_explicit2.json').read_text());m=deepcopy(before['internal_proposals'][0]['model']);old=digest(m)
m['scope_declaration']={'kind':'CONCEPT_DRAFT_ONLY','technical_approval':False,'legal_approval':False,'daylight_sufficiency':False,'ventilation_sufficiency':False,'vertical_core_certified':False,'opening_rights':'UNVERIFIED','execution_ready':False}
for u in m['units']:bind_capacity(u)
g=evaluate(m);out={'model':m,'gate':g,'before_model_hash':old,'metadata_only':True,'no_solver_or_route_regeneration':True}
(P/'evidence/capacity118_whole18x24_metadata_bound.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(g['status'],len(g['errors']),len(g['pending']))
