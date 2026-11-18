"""Saved actual cabinet module audit, without regeneration or solver."""
import json,copy
from pathlib import Path
from q11_boundary118 import examine_closet_boundary
ROOT=Path(__file__).parent
out={}
for suffix in ['5.45x3.6','6x4.2','6.015x4.205','7x5','6x4.2_reflected']:
 m=json.loads((ROOT/f'evidence/q11_module118_{suffix}.json').read_text());r=examine_closet_boundary(m);out[suffix]=r
 assert r['status']=='PASS_USEFUL_CLOSET_BOUNDARY_ONLY',(suffix,r['errors'],r['pending'])
base=json.loads((ROOT/'evidence/q11_module118_5.45x3.6.json').read_text());mutations={}
for name in ['missing_skin','filled_cavity','missing_operation','missing_closet_route','fake_label_only']:
 m=copy.deepcopy(base)
 if name=='missing_skin':m['operations']['closets'][0]['shell_rects'].pop()
 if name=='filled_cavity':m['walls']['cavity_fill']=['1.32','.17','1.78','2.18']
 if name=='missing_operation':m['operations']['closets'][0]['panels'][0]['continuous_actor_segments']=[]
 if name=='missing_closet_route':del m['unit']['routes']['bed1.closet_front']
 if name=='fake_label_only':m['operations']['closets']=[]
 r=examine_closet_boundary(m);assert r['status']!='PASS_USEFUL_CLOSET_BOUNDARY_ONLY',(name,r);mutations[name]=r
out['mutation_results']=mutations
(ROOT/'evidence/independent118/q11_closet_parameter_and_negative_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('Five actual modules passed local useful-closet-boundary; five mutations rejected. Whole Q11 remains pending.')
