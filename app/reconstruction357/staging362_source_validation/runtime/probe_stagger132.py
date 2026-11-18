import json,time
from pathlib import Path
from constructor129 import frame
from coarse_stagger_master132 import propose
from assemble114 import assemble
from world_transform125 import to_world
from private_domain121 import examine
raw={'W':'30.95','L':'21.37','n':2,'requested_count':6}
out=Path('evidence_stagger132');out.mkdir(exist_ok=True)
core,(w,l)=frame(raw,'LEFT_RIGHT');p=propose(core,3)
(out/'proposal.json').write_text(json.dumps(p,indent=2));print('proposal',p['status'],flush=True)
if p.get('rectangles'):
 m=assemble(w,l,core,p);world=to_world(m,core)
 (out/'local.json').write_text(json.dumps(m,indent=2));(out/'world.json').write_text(json.dumps(world,indent=2))
 r=examine(m);(out/'private_topology.json').write_text(json.dumps(r,indent=2));print('topology',r,flush=True)
 from private_hall_binding129 import examine as binding
 r=binding(world,m,core);(out/'source_binding.json').write_text(json.dumps(r,indent=2));print('binding',r['status'],r['errors'],r['pending'],flush=True)
