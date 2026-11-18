"""Reuse the two saved 118 master witnesses; no solver or program changes."""
import json,time
from pathlib import Path
from fractions import Fraction as F
from assemble114 import assemble
from contract114 import core_first,digest
from checker114 import evaluate
P=Path(__file__).resolve().parent
for case in (1,2):
 before=json.loads((P/f'evidence/general118_changed_case{case}.json').read_text());raw=before['input_exact'];W,L=F(raw['W']),F(raw['L']);proposal=before['search_evidence']['attempts'][0];t=time.monotonic()
 try:
  m=assemble(W,L,core_first(W,L),proposal);g=evaluate(m)
  out={'case':case,'raw':raw,'proposal_hash':digest(proposal),'unchanged_proposal':True,'before_model_hash':digest(before['internal_proposals'][0]['model']),'model':m,'gate':g,'elapsed_seconds':time.monotonic()-t,'no_solver_run':True}
  print(case,g['status'],g['errors'],g['pending'],flush=True)
 except Exception as e:
  out={'case':case,'error':type(e).__name__+':'+str(e),'elapsed_seconds':time.monotonic()-t,'no_solver_run':True};print(out,flush=True)
 (P/f'evidence/q11_whole118_case{case}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
