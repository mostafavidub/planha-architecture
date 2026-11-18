"""Replays saved proposal only. No solver/render/deployment."""
import json
from pathlib import Path
from constructor129 import build,context
from evaluate_hierarchical129 import evaluate
out=Path('evidence_stagger_admission132');out.mkdir(exist_ok=True)
raw={'W':'30.95','L':'21.37','n':2,'requested_count':6};p=json.loads(Path('evidence_stagger132/proposal.json').read_text())
packet=build(raw,'LEFT_RIGHT',p);ctx=context(raw,p,packet)
for name,obj in [('packet',packet),('context',ctx)]: (out/(name+'.json')).write_text(json.dumps(obj,indent=2))
print('saved rebuilt packet',flush=True)
r=evaluate(packet,ctx);(out/'gate.json').write_text(json.dumps(r,indent=2))
print(json.dumps({'status':r['status'],'errors':r['errors'],'pending':r['pending']},default=str),flush=True)
