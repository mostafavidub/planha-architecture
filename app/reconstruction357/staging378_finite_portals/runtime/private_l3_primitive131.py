"""Private L3 prototype only. No whole-plan solve, acceptance or deployment."""
import json
from pathlib import Path
from fractions import Fraction as F
from bedroom_module116 import build as double
from twin_module118 import build as twin
from place_module116 import install
from geometry114 import cells,Q,route
from private_domain121 import examine
from contract114 import digest

def build():
 m={'profile':{'body_m':'.7'},'ordered_macro':True,'walls':{},'wall_hosts':{},'source_wall_hosts':{},'openings':[],'operations':{},'room_metadata':{},'units':[]}
 u={'id':'A','rooms':{},'fixtures':{},'fixture_metadata':{},'activities':{},'routes':{},'ownership':[]}
 m['units']=[u]
 # Left facing pair, right lower double. Source widths/depths stay unchanged.
 jobs=[('bed1',twin('5.45','4.5'),['.15','.15','5.6','4.65'],'right'),('bed2',twin('5.45','4.5'),['.15','4.8','5.6','9.3'],'right'),('bed3',double('5.45','3.6'),['6.9','.15','12.35','3.75'],'left')]
 for name,source,clear,side in jobs:install(source,m,u,'A',name,clear,'20',side)
 # Functional corridor boundary alongside missing fourth bedroom quadrant.
 for name,r in {'right_exposed':['6.75','3.9','6.9','9.45'],'top':['5.6','9.3','6.75','9.45']}.items():
  k='A.private_l3.'+name;m['walls'][k]=r;m['wall_hosts'][k]=r;m['source_wall_hosts'][k]=r
 gross=[['5.75','.15','6.75','9.3']]+[r for rs in m['module_aprons'].values()for r in rs]
 parts=cells(gross,list(m['walls'].values()))
 interface=['5.75','-.2','6.75','.5'];floor=parts+[interface]
 u['rooms']['private_circulation']=parts;u['rooms']['public_interface']=[['5.75','-.2','6.75','.15']]
 u['ownership']=cells([r for rs in u['rooms'].values()for r in rs],[])
 box=['0','-.2','12.5','9.45'];center=['6.25','.15']
 obstacles=list(m['walls'].values())+list(u['fixtures'].values())+cells([box],floor)
 paths={};fail=[]
 for p in m['module_ports']:
  name=p['opening_id'].rsplit('.',1)[0];path,why=route(center,p['center'],box,obstacles)
  if path:paths[name]=path
  else:fail.append({'target':name,'reason':why})
 m['private_domains']=[{'unit':'A','bedrooms':['A.bed1','A.bed2','A.bed3'],'parts':parts,'public_interface':{'rect':interface,'open_side':'bottom'},'paths':paths,'route_failures':fail,'topology_scope':'L3_FACING_AND_STACKED_PRIVATE_PROTOTYPE_NOT_WHOLE_PLAN'}]
 m['private_primitive_scope']={'source_program':'two twin and one double, six persons','clear_corridor_m':'1','actual_room_floor_area_m2':str(sum((Q(r)[2]-Q(r)[0])*(Q(r)[3]-Q(r)[1])for key,rs in u['rooms'].items()if key.startswith('bed')for r in rs)),'unoccupied_upper_right_is_not_private_floor':True,'whole_model_gate':'NOT_RUN','privacy_all_targets':'NOT_RUN','source_placement_full_replay':'NOT_RUN','public_service_fit':'NOT_RUN','accepted':False,'release_allowed':False}
 from wall_union118 import bind_physical_wall_union
 return bind_physical_wall_union(m)
if __name__=='__main__':
 out=Path(__file__).parent/'evidence_l3_primitive131';out.mkdir(exist_ok=True);m=build();r=examine(m)
 (out/'model.json').write_text(json.dumps(m,indent=2));(out/'topology.json').write_text(json.dumps(r,indent=2));print(json.dumps({'hash':digest(m),'errors':r['errors'],'pending':r['pending'],'paths':m['private_domains'][0]['paths']}))
