import json,copy
from pathlib import Path
from q11_boundary118 import examine
ROOT=Path(__file__).parent
m=json.loads((ROOT/'evidence/q11_whole118_case1.json').read_text())['model'];rows={}
for kind in ['delete_actual_global_skin','add_neighbor_on_actor']:
 n=copy.deepcopy(m)
 if kind=='delete_actual_global_skin':n['operations']['closets'][0]['shell_rects'].pop()
 else:
  op=n['operations']['closets'][0];actor=op['panels'][0]['continuous_actor_segments'][0]['actor_start'];n['walls']['new_neighbor']=actor
 r=examine(n);assert r['errors'],(kind,r['pending']);rows[kind]=r
(ROOT/'evidence/independent118/q11_whole_mutations.json').write_text(json.dumps(rows,indent=2));print('Both whole-model skin/neighbor mutations independently rejected')
