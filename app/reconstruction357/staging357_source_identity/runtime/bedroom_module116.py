"""Parametric private-bedroom module with actual screened entry and motion.
Clear W/H are parameters; furniture remains reference-sized. No PASS is generated.
The panel/cabinet construction is a declared geometric study, not approved hardware.
"""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from contract114 import S,digest
from geometry114 import cells,Q,route

def build(width,depth):
 W,H=F(str(width)),F(str(depth));T=F('.15');uid='M';catalog=json.loads(Path(__file__).with_name('fixture_catalog114.json').read_text())
 if W<F('5.45')or H<F('3.6'):raise ValueError('MODULE_PROGRAM_BOUNDS_NOT_GLOBAL_INFEASIBILITY')
 seq=lambda r:[S(x)for x in r]
 bed=(W-F('2.1'),(H-F('3.4'))/2+F('.9'),W-F('.1'),(H-F('3.4'))/2+F('2.5'))
 closet=(F('1.3'),F('.15'),F('1.9'),F('2.2'))
 changing=(bed[2]-F('.7'),bed[3]+F('.1'),bed[2],bed[3]+F('.8'))
 aperture=(-T,F('.2'),F(0),F('1.2'))
 walls={'left.lower':seq((-T,-T,0,F('.2'))),'left.upper':seq((-T,F('1.2'),0,H+T)),'right':seq((W,-T,W+T,H+T)),'front':seq((0,-T,W,0)),'back':seq((0,H,W,H+T))}
 floor=cells([[0,0,W,H]],[]);apron_gross=[[-1,0,0,F('2.4')]];apron=cells(apron_gross,list(walls.values()))
 u={'id':uid,'ownership':floor+[seq(q)for q in apron],'rooms':{'bed1':floor,'public_access':[seq(q)for q in apron]},'fixtures':{'bed1.bed':seq(bed),'bed1.closet':seq(closet)},'fixture_metadata':{'bed1.bed':{'kind':'bed','rotation_deg':0},'bed1.closet':{'kind':'closet','rotation_deg':0}},'activities':{'bed1.bed_front':seq((bed[0],bed[1]-F('.9'),bed[2],bed[1])),'bed1.bed_back':seq((bed[0],bed[3],bed[2],bed[3]+F('.9'))),'bed1.closet_front':seq((closet[2],closet[1],closet[2]+F('.7'),closet[3])),'bed1.changing':seq(changing)},'routes':{},'route_targets':{}}
 closed=(F('.02'),F('.2'),F('.12'),F('1.2'));opened=(F('.02'),F('1.2'),F('.12'),F('2.2'));delta=(F(0),F(1))
 def motion_states(cl,op,delta,actor,hand,role,side,actor_end=None):
  actor_end=actor if actor_end is None else actor_end
  he=(hand[0]+delta[0],hand[1]+delta[1]);st=[{'unit':uid,'side':side,'role_id':role,'fraction':str(t),'panel_rect':seq(p),'actor_rect':seq(actor if t==0 else actor_end),'hand_point':seq(h)}for t,p,h in[(0,cl,hand),(1,op,he)]]
  sg=[{'unit':uid,'side':side,'role_id':role,'t0':'0','t1':'1','actor_start':seq(actor),'actor_end':seq(actor_end),'hand_start':seq(hand),'hand_end':seq(he)}]
  return st,sg
 states=[];segments=[]
 for side,actor,role in [('inside',(F('.17'),F('.15'),F('.87'),F('.85')),'M.bed1'),('outside',(F('-.9'),F('.15'),F('-.2'),F('.85')),'M.public_access')]:
  st,sg=motion_states(closed,opened,delta,actor,(F('.07'),F('.2')),role,side,tuple(v+(F('.4')if i%2 else 0)for i,v in enumerate(actor)));states+=st;segments+=sg
 door={'opening_id':'M.bed1.entry','kind':'sliding_linear','mount':{'kind':'surface','host_wall_id':'left','face':'max','offset_m':'.02','panel_thickness_m':'.1'},'closed_panel':seq(closed),'open_panel':seq(opened),'translation':seq(delta),'pocket':seq(opened),'rail_envelope':seq((F('.02'),F('.2'),F('.12'),F('2.2'))),'states':states,'continuous_actor_segments':segments,'assumptions':['Surface-mounted 0.1m panel/0.02m offset is an explicit provisional hardware study; not owner-certified manufacture.']}
 cx,cy,cr,ct=closet;half=(ct-cy)/2;panels=[]
 for i in (0,1):
  xx=cx+F('.02')+i*F('.05');yy=cy+i*half;cl=(xx,yy,xx+F('.04'),yy+half);de=(F(0),half if i==0 else-half);op=tuple(v+de[j%2]for j,v in enumerate(cl));actor=(cx-F('.7'),cy+half-F('.35'),cx,cy+half+F('.35'));hand=(xx,yy+half/2)
  st,sg=motion_states(cl,op,de,actor,hand,'M.bed1','front')
  panels.append({'id':'half'+str(i+1),'closed_panel':seq(cl),'open_panel':seq(op),'translation':seq(de),'rail_envelope':seq((xx,cy,xx+F('.04'),ct)),'states':st,'continuous_actor_segments':sg})
 shell=[(cx+F('.12'),cy,cr,cy+F('.02')),(cx+F('.12'),ct-F('.02'),cr,ct),(cr-F('.02'),cy+F('.02'),cr,ct-F('.02'))]
 closetop={'unit':uid,'fixture_id':'bed1.closet','front_axis':'x','front_side':'min','shell_rects':[seq(q)for q in shell],'panels':panels,'assumptions':['0.04m half panels on two distinct rails and 0.02m carcass are provisional explicit construction assumptions, not approved vendor specifications.']}
 # Reflect only this physical cabinet and its motion across its centre plane.
 # Gross immutable footprint is unchanged; front faces the useful room interior.
 def rq(q):
  a,b,c,d=map(F,q);return seq((cx+cr-c,b,cx+cr-a,d))
 def rp(q):return seq((cx+cr-F(q[0]),F(q[1])))
 closetop['front_side']='max'
 closetop['shell_rects']=[rq(q)for q in closetop['shell_rects']]
 for panel in closetop['panels']:
  for key in ('closed_panel','open_panel','rail_envelope'):panel[key]=rq(panel[key])
  panel['translation'][0]=S(-F(panel['translation'][0]))
  for st in panel['states']:
   st['panel_rect']=rq(st['panel_rect']);st['actor_rect']=rq(st['actor_rect']);st['hand_point']=rp(st['hand_point'])
  for sg in panel['continuous_actor_segments']:
   for key in ('actor_start','actor_end'):sg[key]=rq(sg[key])
   for key in ('hand_start','hand_end'):sg[key]=rp(sg[key])
 # These are the actual 0.02m carcass skins, not an extra sight-only partition.
 # They remain recorded in operations; checker must bind them before opacity use.
 boundary={'kind':'ACTUAL_USABLE_CLOSET_SHELL','fixture_id':'bed1.closet','operation_fixture_id':'bed1.closet','shell_rects':closetop['shell_rects'],'source':'same immutable closet plus declared physical two-panel construction','no_separate_privacy_partition':True}
 start=(F('-.55'),F('.7'));failures=[];obstacles=list(walls.values())+list(u['fixtures'].values())+[seq(opened)]
 for name,a in u['activities'].items():
  a=Q(a);end=((a[0]+a[2])/2,(a[1]+a[3])/2);path,why=route(start,end,[-1,0,W,H],obstacles)
  u['route_targets'][name]=seq(end)
  if path:u['routes'][name]=path
  else:failures.append({'route':name,'reason':why})
 module={'schema':'PRIVATE_ROOM_MODULE116','contract_version':'PRIVATE_ROOM_GEOMETRY_OPERATIONS_V1','fixture_catalog_hash':digest(catalog),'input_program':{'width':S(W),'depth':S(H),'bedrooms':1,'body_m':'.7','fixture_sizes':'immutable reference catalogue','bounds_are_search_scope_not_regulations':True},'bounds':[seq((-1,-T,W+T,H+T))],'unit':u,'walls':walls,'wall_hosts':{'left':seq((-T,-T,0,H+T)),**{k:v for k,v in walls.items()if not k.startswith('left.')}},'openings':[{'id':'M.bed1.entry','rect':seq(aperture),'host_wall_id':'left','connects':['M.public_access','M.bed1']}],'operations':{'doors':[door],'closets':[closetop]},'external_ports':[{'id':'M.port','opening_id':'M.bed1.entry','rect':seq((-1,0,-T,F('2.4'))),'center':seq(start),'role_id':'M.public_access','body_width':'.7','reserved_approach_required':True}],'logical_regions':{},'room_metadata':{'M.bed1':{'role':'bedroom','private':True}},'reserved_approach_gross':[seq(q)for q in apron_gross],'route_failures':failures,'privacy_construction':boundary,'q11_functional_boundary':{'kind':'ACTUAL_USABLE_CLOSET_SHELL','fixture_id':'bed1.closet','operation_fixture_id':'bed1.closet','shell_indices':[0,1,2],'no_separate_privacy_partition':True},'placement_contract':{'allowed_transforms':['translation','axis_reflection'], 'uniform_scale_allowed':False,'revalidate_after_placement':True,'port_and_window_orientation_must_be_bound':True},'accepted':False,'release_allowed':False}
 module['source_binding']={'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'fixture_source_sha256':catalog['source_file_sha256']}
 return module

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--width',default='6');ap.add_argument('--depth',default='4.2');ap.add_argument('--out',default='evidence/module116_6x4.2.json');args=ap.parse_args();m=build(args.width,args.depth);Path(args.out).write_text(json.dumps(m,indent=2));print(json.dumps({'file':args.out,'route_failures':m['route_failures'],'closet':m['unit']['fixtures']['bed1.closet'],'bed':m['unit']['fixtures']['bed1.bed']}))
