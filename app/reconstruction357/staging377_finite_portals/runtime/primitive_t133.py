"""Three-room T-source primitive only. No whole-plan acceptance or runtime integration."""
from fractions import Fraction as F
from contract114 import S
from geometry114 import cells,route,Q
from source_rotation133 import build
from place_module133 import install

def make():
 m={'ordered_macro':{'kind':'T133_PRIMITIVE_NOT_ADMITTED'},'walls':{},'wall_hosts':{},'source_wall_hosts':{},'openings':[],'operations':{},'room_metadata':{},'profile':{'body_m':'.7'},'logical_regions':{},'accepted':False}
 u={'id':'A','ownership':[['-2','-2','15','14']],'rooms':{},'fixtures':{},'fixture_metadata':{},'activities':{},'routes':{},'scenario_routes':{}}
 for name,role,rect,side in [('bed1','double',['5.55','5.95','9.15','11.4'],'bottom'),('bed2','twin',['.15','.15','5.6','4.65'],'right'),('bed3','twin',['6.9','.15','12.35','4.65'],'left')]:install(build(role),m,u,'A',name,rect,30,side)
 for key,r in {'stem_bottom_left':['5.6','-.55','5.75','.15'],'stem_bottom_right':['6.75','-.55','6.9','.15'],'cap_left':['5.25','4.8','5.4','5.8'],'cap_right':['9.3','4.8','9.45','5.8']}.items():
  for fld in('walls','wall_hosts','source_wall_hosts'):m[fld]['A.t133.'+key]=r
 gross=[['5.75','-.55','6.75','4.8'],['5.4','4.8','9.3','5.8']]
 parts=cells(gross,list(m['walls'].values()));u['rooms']['private_circulation']=parts;u['rooms']['public_interface']=[['5.75','-.9','6.75','-.55']]
 interface=['5.75','-.9','6.75','-.2'];center=['6.25','-.55'];floor=parts+[interface];q=list(map(Q,floor));box=[min(z[0]for z in q),min(z[1]for z in q),max(z[2]for z in q),max(z[3]for z in q)];obs=list(m['walls'].values())+list(u['fixtures'].values())+cells([box],floor);paths={};fail=[]
 for name in ('bed1','bed2','bed3'):
  port=next(p for p in m['module_ports']if p['opening_id']=='A.'+name+'.entry');path,why=route(center,port['center'],box,obs)
  if path:paths['A.'+name]=path
  else:fail.append({'bed':name,'reason':why})
 m['units']=[u];m['private_domains']=[{'unit':'A','bedrooms':['A.bed1','A.bed2','A.bed3'],'parts':parts,'public_interface':{'rect':interface,'open_side':'bottom'},'paths':paths,'route_failures':fail,'topology_scope':'T133_PRIMITIVE_ONLY'}]
 return m
if __name__=='__main__':
 import json
 from pathlib import Path
 from private_domain121 import examine
 m=make();o=Path('../review133_study/primitive');o.mkdir(exist_ok=True,parents=True);(o/'model.json').write_text(json.dumps(m,indent=2));r=examine(m);(o/'topology.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
