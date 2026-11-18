import json,time
from pathlib import Path
from constructor129 import frame
from coarse_t_master133 import propose
from assemble114 import assemble
from world_transform125 import to_world
from private_domain121 import examine
raw={'W':'44.00','L':'32.20','n':2,'requested_count':6}
out=Path('../review133_study/whole_case3');out.mkdir(exist_ok=True)
core,(w,l)=frame(raw,'LEFT_RIGHT');p=propose(core,3)
(out/'proposal.json').write_text(json.dumps(p,indent=2));print('proposal',p['status'],flush=True)
if p.get('rectangles'):
 m=assemble(w,l,core,p);world=to_world(m,core)
 (out/'local.json').write_text(json.dumps(m,indent=2));(out/'world.json').write_text(json.dumps(world,indent=2))
 r=examine(m);(out/'private_topology.json').write_text(json.dumps(r,indent=2));print('topology',r,flush=True)
 print('whole_route_failures',len(m.get('route_failures',[])),m.get('route_failures'),flush=True)
