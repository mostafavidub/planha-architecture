"""Fixed physical witness replay. No generation or larger solver budget."""
import json,time
from pathlib import Path
from fractions import Fraction as F
from contract114 import core_first,digest
from search114 import propose
from checker114 import evaluate
from witness_binding118 import binding
ROOT=Path(__file__).resolve().parent
source=ROOT.parent/'planha_general117/evidence/general117_complete_explicit2.json'
p=json.loads(source.read_text());m=p['internal_proposals'][0]['model'];proposal=p['search_evidence']['attempts'][0]
t=time.monotonic();gate=evaluate(m)
out={'source_file':str(source),'model_hash':digest(m),'proposal_hash':digest(proposal),'raw':{'W':'18','L':'24','n':2,'program':{'bedrooms_per_unit':2}},'program_scope':'Explicit 2-bedroom witness, NOT default 3-bedroom feasibility.','fresh_gate':gate,'validation_seconds':time.monotonic()-t,'model_proposal_binding':binding(m,proposal),'fixed_replay':propose(core_first(F(18),F(24)),2,time_limit=3,fixed_witness=proposal)}
(ROOT/'evidence/fixed_witness118_explicit2_after_generalization.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(gate['status'],out['fixed_replay']['status']);print(out['fixed_replay'].get('diagnostic',{}).get('violations'));print(out['fixed_replay'].get('solver_seconds'))
