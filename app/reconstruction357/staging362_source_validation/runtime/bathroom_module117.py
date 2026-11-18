"""Source-rigid bathroom module. No acceptance receipts inherited from 113.
Only far exterior boundaries extend; equipment/portals/pocket assemblies remain
source-sized. Actor .7 and source .03 pocket panels retain their actual contract.
"""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from contract114 import S,digest
from geometry114 import Q,cells,route
P=Path(__file__).parent

def build(width='3.15',depth='2.25'):
 W,H=F(str(width)),F(str(depth));T=F('.15');ox,oy=F('.25'),F('6.725');uid='S'
 if not F('3.15')<=W<=F('4.3') or not F('2.25')<=H<=F('3.1'):raise ValueError('BATHROOM_STUDY_BOUNDS_NOT_GLOBAL_INFEASIBILITY')
 sourcepath=P/'bathroom_source117.json';s=json.loads(sourcepath.read_text());catalog=json.loads((P/'fixture_catalog114.json').read_text());su=s['unit'];seq=lambda q:[S(v)for v in q]
 def shift(q):return tuple(F(str(v))-(ox if i%2==0 else oy)for i,v in enumerate(q))
 def clip(q,box):
  q=Q(q);a=(max(q[0],box[0]),max(q[1],box[1]),min(q[2],box[2]),min(q[3],box[3]));return a if a[0]<a[2]and a[1]<a[3]else None
 box=(-T,-T,F('3.3'),F('2.4'));solids={};hosts={}
 for dest,src in [(solids,s['actual_solids']),(hosts,s['walls'])]:
  for k,v in src.items():
   q=clip(shift(v),box)
   if q:
    # Boundary expansion, not equipment or pocket scaling.
    q=tuple(x+(W-F('3.15')if i%2==0 else H-F('2.25'))if x>=(F('3.15')if i%2==0 else F('2.25'))else x for i,x in enumerate(q));dest[k]=seq(q)
 fixtures={k:seq(shift(su['fixtures'][k]))for k in ['WC_iranian','shower_floor','basin']}
 acts={k:seq(shift(su['activities'][k]))for k in ['WC_front','WC_use','shower_use','basin_front']}
 # Basin and its own standing activity rigidly follow the rear wall.
 for key,table in [('basin',fixtures),('basin_front',acts)]:
  table[key]=seq(tuple(F(v)+(H-F('2.25')if i%2 else 0)for i,v in enumerate(table[key])))
 floor=cells([[0,0,W,H]],list(solids.values()));apron_gross=[[F('.7'),F('-.95'),F('2.3'),0]];apron=cells(apron_gross,list(solids.values()))
 u={'id':uid,'ownership':floor+apron,'rooms':{'bath':floor,'public_access':apron},'fixtures':fixtures,'fixture_metadata':{k:{'kind':k,'rotation_deg':0}for k in fixtures},'activities':acts,'routes':{},'route_targets':{}}
 logical={uid+'.vanity':{'unit':uid,'parts':cells([[F('1.05'),0,F('2'),H]],list(solids.values()))},uid+'.WC':{'unit':uid,'parts':cells([[F('2.15'),0,W,H]],list(solids.values()))},uid+'.shower':{'unit':uid,'parts':cells([[0,0,F('.9'),H]],list(solids.values()))}}
 ops=[];openings=[]
 for name,old in s['doors'].items():
  short=name.split('.')[1];oid=uid+'.'+short;opening=next(o for o in s['openings']if o['id']==name);conn=[uid+'.public_access',uid+'.bath']if short=='bath'else[uid+'.vanity',uid+'.'+short]
  openings.append({'id':oid,'rect':seq(shift(opening['rect'])),'host_wall_id':old['host_wall'],'connects':conn,'kind':'pocket_source113'})
  cl,op,pock=[shift(old[k])for k in ('closed_panel','open_panel','pocket')];delta=(op[0]-cl[0],op[1]-cl[1]);states=[];segments=[]
  for side in old['sides']:
   role=conn[0 if side['side']=='outside'else 1]
   for piece in side['pieces']:
    a0,a1=shift(piece['actor0']),shift(piece['actor1']);h0,h1=shift(piece['grip0']),shift(piece['grip1']);body=lambda a:seq((a[0]-F('.35'),a[1]-F('.35'),a[0]+F('.35'),a[1]+F('.35')))
    for t,a,h in [(F(piece['t0']),a0,h0),(F(piece['t1']),a1,h1)]:states.append({'unit':uid,'side':side['side'],'role_id':role,'fraction':S(t),'panel_rect':seq(tuple(cl[i]+delta[i%2]*t for i in range(4))),'actor_rect':body(a),'hand_point':seq(h)})
    segments.append({'unit':uid,'side':side['side'],'role_id':role,'t0':piece['t0'],'t1':piece['t1'],'actor_start':body(a0),'actor_end':body(a1),'hand_start':seq(h0),'hand_end':seq(h1)})
  ops.append({'opening_id':oid,'kind':'pocket_source113','closed_panel':seq(cl),'open_panel':seq(op),'translation':seq(delta),'pocket':seq(pock),'host_wall_id':old['host_wall'],'opaque_skin_m':old['opaque_skin_m'],'states':states,'continuous_actor_segments':segments,'open_transfer_points':[seq(shift(p))for p in old['open_transfer_points']],'source_contract':'Actual .03m reference pocket panel, source clearance and skins; not surface .1m assumption.'})
 start=(F('1.525'),F('-.5'));fail=[];base_obstacles=list(solids.values())+[o['open_panel']for o in ops]
 for name,q in acts.items():
  q=Q(q);end=((q[0]+q[2])/2,(q[1]+q[3])/2);obstacles=base_obstacles+[v for k,v in fixtures.items()if not(name=='WC_use'and k=='WC_iranian')and not(name=='shower_use'and k=='shower_floor')];path,why=route(start,end,[0,F('-.95'),W,H],obstacles);u['route_targets'][name]=seq(end)
  if path:u['routes'][name]=path
  else:fail.append({'route':name,'reason':why})
 return {'schema':'BATHROOM_MODULE117','contract_version':'REFERENCE113_POCKET_BATH_STUDY','fixture_catalog_hash':digest(catalog),'input_program':{'width':S(W),'depth':S(H),'body_m':'.7'},'bounds':[seq((-T,F('-.95'),W+T,H+T))],'unit':u,'walls':solids,'wall_hosts':hosts,'logical_regions':logical,'openings':openings,'operations':{'doors':ops},'external_ports':[{'id':'S.port','opening_id':'S.bath','rect':seq((F('.7'),F('-.95'),F('2.3'),-T)),'center':seq(start),'role_id':'S.public_access','body_width':'.7','reserved_approach_required':True}],'reserved_approach_gross':[seq(q)for q in apron_gross],'route_failures':fail,'source_binding':{'source_snapshot_sha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_model_hash':s['model_hash'],'fixture_source_sha256':catalog['source_file_sha256']},'placement_contract':{'allowed_transforms':['translation','axis_reflection'],'uniform_scale_allowed':False,'revalidate_after_placement':True},'accepted':False,'release_allowed':False,'scope':['No inherited acceptance; independent operation, privacy and placement checks required.','WC_use/shower_use/shower_floor privacy targets retained; basin_front functional route, not an invented privacy target.','Only own WC_use/WC_iranian and shower_use/shower_floor task-target exceptions follow reference lr_target_125x20_revision.py:73; neither is globally walkable.']}
if __name__=='__main__':
 m=build();(P/'evidence/bathroom117_3.15x2.25.json').write_text(json.dumps(m,indent=2));print(json.dumps({'schema':m['schema'],'route_failures':m['route_failures'],'doors':len(m['operations']['doors'])}))
