"""Build review candidate only; static schema pin requires explicit code review."""
import json,hashlib
from pathlib import Path
R=Path(__file__).parent
base=json.loads((R/'world_record_schema131.json').read_text());records=base['records'];added={}
def walk(v,path='root',key=''):
 if key in ('module','source_contract'):return
 if isinstance(v,dict):
  keys=sorted(k for k in v if not(path=='root'and k=='frame_binding125'))
  if path!='root.physical_wall_network.solids'and keys not in records.get(path,[]):
   records.setdefault(path,[]).append(keys);added.setdefault(path,[]).append(keys)
  for k,z in v.items():
   if path=='root'and k=='frame_binding125':continue
   walk(z,path+'.'+k,k)
 elif isinstance(v,list):
  for z in v:walk(z,path+'[]')
p=json.loads((R/'evidence_access_admission132/packet.json').read_text())
for k in ('local_model','world_model'):walk(p[k])
base.update(schema='WORLD_RECORDS132_ACCESS_REVIEW_CANDIDATE',scope='Closed record shapes for L3 source role ordering and two actual circulation boundaries. Review candidate; no geometry or admission waiver.')
(R/'world_record_schema132.json').write_text(json.dumps(base,indent=2,sort_keys=True)+'\n');(R/'evidence_access_admission132/schema_additions.json').write_text(json.dumps(added,indent=2,sort_keys=True))
print(hashlib.sha256((R/'world_record_schema132.json').read_bytes()).hexdigest(),len(added))
