"""Fresh constructor run on preserved master proposal, no solver repetition."""
import json,time
from pathlib import Path
from fractions import Fraction as F
from contract114 import core_first,digest
from assemble114 import assemble
from engine114 import revision,generation_context,evaluate,_GATE_CACHE
P=Path(__file__).resolve().parent
prior=json.loads((P/'evidence/compact118_first_actual.json').read_text());proposal=prior['search_evidence']['attempts'][0]
raw={'W':'18','L':'24','n':2,'requested_count':6,'program':{'bedrooms_per_unit':2}}
core=core_first(F(18),F(24));t=time.monotonic();m=assemble(F(18),F(24),core,proposal);assembly_seconds=time.monotonic()-t
trace={'schema':'CONSTRUCTION_TRACE118_V1','raw':raw,'core':core,'proposal':proposal,'model_hash':digest(m),'source_revision':revision()};context=generation_context(m['inputs'],trace);t=time.monotonic();gate=evaluate(m,workflow_context=context)
out={'model':m,'gate':gate,'generation_context':context,'assembly_seconds':assembly_seconds,'validation_seconds':time.monotonic()-t,'no_solver_run':True,'preserved_proposal_hash':digest(proposal),'source_revision':revision()}
t=time.monotonic();hit=evaluate(m,workflow_context=context);hit_seconds=time.monotonic()-t
t=time.monotonic();forced=evaluate(m,workflow_context=context,force=True);forced_seconds=time.monotonic()-t
out['cache_actual_proof']={'hit_gate_exact_equal':hit==gate,'forced_gate_exact_equal':forced==gate,'hit_seconds':hit_seconds,'forced_seconds':forced_seconds,'computations':_GATE_CACHE.computations,'hits':_GATE_CACHE.hits}
(P/'evidence/compact118_reassembled_actual.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(gate['status'],'errors',gate['errors'],'pending',gate['pending'],flush=True)
