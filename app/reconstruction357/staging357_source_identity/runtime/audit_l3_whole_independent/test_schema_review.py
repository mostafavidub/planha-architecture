import json,copy,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P))
from world_inventory125 import examine as inventory
from private_l3_binding131 import examine as binding
from frame_audit125 import digest
p=json.loads((P/'evidence_l3_admission131/packet.json').read_text());a=p['local_model'];b=p['world_model'];c=p['core']
def check(l,w):return {'inventory':inventory(l,w,c),'binding':binding(w,l,c)}
out={'baseline':check(a,b),'mutations':{}}
for case in ('shared_unknown','world_origin','shared_origin','world_scalar','shared_scalar','shared_rectangles','shared_door_sides','world_source_transform','shared_source_transform'):
 l,w=copy.deepcopy(a),copy.deepcopy(b)
 if case=='shared_unknown':
  for m in(l,w):m['ordered_macro']['extra_field']=1
 if case in('world_origin','shared_origin'):
  w['ordered_macro']['origin'][0]='0'
  if case=='shared_origin':l['ordered_macro']['origin'][0]='0'
 if case in('world_scalar','shared_scalar'):
  w['ordered_macro']['private_interface_center_x']='0'
  if case=='shared_scalar':l['ordered_macro']['private_interface_center_x']='0'
 if case=='shared_rectangles':
  for m in(l,w):m['ordered_macro']['rectangles']['bed1'][0]='0'
 if case=='shared_door_sides':
  for m in(l,w):m['ordered_macro']['bed_door_sides']['bed1']='left'
 if case in('world_source_transform','shared_source_transform'):
  w['module_placements'][0]['transform']['translation'][0]='0'
  if case=='shared_source_transform':l['module_placements'][0]['transform']['translation'][1]='0'
 w['frame_binding125']['local_model_hash']=digest(l)
 r=check(l,w);out['mutations'][case]={k:{'errors':v['errors'],'pending':v['pending']}for k,v in r.items()}
(Path(__file__).parent/'schema_review_tests.json').write_text(json.dumps(out,indent=2))
print('baseline',[(k,v['errors'],v['pending'])for k,v in out['baseline'].items()]);print(json.dumps(out['mutations'],indent=2))
