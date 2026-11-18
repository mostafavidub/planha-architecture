"""Replays saved proposal only. No solver/render/deployment."""
import json
from pathlib import Path
from constructor129 import build,context
from evaluate_hierarchical129 import evaluate
out=Path('../review133_study/admission133');out.mkdir(exist_ok=True)
raw={'W':'44.00','L':'32.20','n':2,'requested_count':6};p=json.loads(Path('../review133_study/whole_case3/proposal.json').read_text())
packet=build(raw,'LEFT_RIGHT',p);ctx=context(raw,p,packet)
for name,obj in [('packet',packet),('context',ctx)]: (out/(name+'.json')).write_text(json.dumps(obj,indent=2))
print('saved rebuilt packet',flush=True)
r=evaluate(packet,ctx);(out/'gate.json').write_text(json.dumps(r,indent=2))
print(json.dumps({'status':r['status'],'errors':[{'code':e.get('code'),'requirement_id':e.get('requirement_id'),'errors':e.get('witness',{}).get('errors')}if isinstance(e,dict)else e for e in r['errors']],'pending':r['pending']},default=str),flush=True)
