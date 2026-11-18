"""Parametric essential-kitchen component; immutable appliances and actual access.
Reference113 motion profile is a declared hypothetical geometric program, not
complete cooking, vendor hardware, ventilation or regulatory certification.
"""
import json,hashlib
from pathlib import Path
from fractions import Fraction as F
from contract114 import S,digest
from geometry114 import cells,route,Q

def build(width,depth):
 W,H=F(str(width)),F(str(depth));T=F('.15');uid='K';seq=lambda q:[S(x)for x in q]
 if W<F('2.35')or H<F('3.05'):raise ValueError('KITCHEN_MODULE_CURRENT_BOUNDS_NOT_GLOBAL_INFEASIBILITY')
 catalog=json.loads(Path(__file__).with_name('fixture_catalog114.json').read_text())
 fixtures={k:seq([0,y,w,Y])for k,w,y,Y in [('cooker',F('.6'),F('.05'),F('.75')),('prep',F('.6'),F('.75'),F('1.45')),('sink',F('.6'),F('1.45'),F('2.15')),('fridge',F('.7'),F('2.25'),F('2.95'))]}
 aperture=[F('.6'),-T,F('1.6'),F(0)]
 walls={'left':seq([-T,-T,0,H+T]),'right':seq([W,-T,W+T,H+T]),'back':seq([0,H,W,H+T]),'front.left':seq([0,-T,F('.6'),0]),'front.right':seq([F('1.6'),-T,W,0])}
 hosts={'left':walls['left'],'right':walls['right'],'back':walls['back'],'front':seq([0,-T,W,0])}
 apron_gross=[[F('.45'),-1,F('1.75'),0]];apron=cells(apron_gross,list(walls.values()));floor=[seq([0,0,W,H])]
 work=(F('1.1'),F('1.5'));port=(F('1.1'),F('-.55'));u={'id':uid,'ownership':floor+apron,'rooms':{'kitchen':floor,'public_access':apron},'fixtures':fixtures,'fixture_metadata':{k:{'kind':k,'rotation_deg':0}for k in fixtures},'activities':{'kitchen_work':seq([F('.75'),F('.05'),F('1.45'),F('2.95')])},'routes':{},'route_targets':{'kitchen_work':seq(work)}}
 p,why=route(port,work,[0,-1,W,H],list(walls.values())+list(fixtures.values()));fail=[]
 if p:u['routes']['kitchen_work']=p
 else:fail.append({'route':'kitchen','reason':why})
 # All witness coordinates derive from actual fixture fronts, never a receipt.
 q=Q(fixtures['fridge']);front,hy=q[2],q[3]
 fridge={'fixture_id':'fridge','hinge':seq([front,hy]),'angle_range_degrees':[0,90],'leaf_radius_m':'.7','leaf_half_thickness_m':'.03','grip_radius_m':'.74','actor_offset_m':['.45','-.45'],'body_m':'.7','interval_count':360,'closed_actor':seq([front+F('.45'),hy-F('1.19')]),'open_actor':seq([front+F('1.19'),hy-F('.45')]),'open_access':seq([front+F('.4'),hy-F('.45')]),'shelf_target':seq([front-F('.15'),hy-F('.45')]),'held_target':seq([front+F('.15'),hy-F('.45')]),'object_half_size_m':'.03'}
 drawers={};stations=[]
 for k in ('sink','prep','cooker'):
  q=Q(fixtures[k]);fr=q[2];cy=(q[1]+q[3])/2;closed=(fr+F('.45'),cy);opened=(fr+F('1.05'),cy)
  stations.append({'fixture_id':k,'actor_rect':seq([closed[0]-F('.35'),cy-F('.35'),closed[0]+F('.35'),cy+F('.35')]),'hand_point':seq([fr,cy]),'front':{'axis':'x','side':'max'}})
  if k!='cooker':drawers[k]={'fixture_id':k,'closed_actor':seq(closed),'open_actor':seq(opened),'translation':seq([F('.6'),0]),'travel_m':'.6','closed_tray':seq([q[0]+F('.02'),q[1]+F('.02'),fr,q[3]-F('.02')]),'open_tray':seq([q[0]+F('.62'),q[1]+F('.02'),fr+F('.6'),q[3]-F('.02')]),'grip_closed':seq([fr+F('.03'),cy]),'grip_open':seq([fr+F('.63'),cy]),'storage_target':seq([fr+F('.45'),cy]),'held_target':seq([opened[0]-F('.25'),cy]),'own_tray_body_gap_m':'.1','object_half_size_m':'.03','tray_lip_height_m':'.15','object_bottom_height_m':'.20'}
 q=Q(fixtures['fridge']);act=(q[2]+F('.4'),q[3]-F('.45'));stations.append({'fixture_id':'fridge','actor_rect':seq([act[0]-F('.35'),act[1]-F('.35'),act[0]+F('.35'),act[1]+F('.35')]),'hand_point':seq([q[2],act[1]]),'front':{'axis':'x','side':'max'}})
 op={'unit':uid,'profile':'REFERENCE113_ESSENTIAL_KITCHEN_V1','canonical_isometry':{'matrix':[[-1,0],[0,1]],'translation':['0','0']},'front_binding':{'axis':'x','side':'max','back_wall_id':'left','fixture_ids':['fridge','sink','prep','cooker']},'fridge':fridge,'drawers':drawers,'workstations':stations,'workpoint':seq(work),'source_contract':'audit_lr_kitchen/check.py via kitchen_check113.py','assumptions':['Reference113 hypothetical 0.7m body, 0.6m drawer travel, 0.06m object; compatible shelf/worktop height assumed.','Object bottom at0.20m above0.15m drawer lip; not full cooking/washing or vendor hardware certification.','Oven loading remains optional/unestablished; essential fridge/drawer/surface witnesses must be freshly checked.']}
 op['kind']='REFERENCE113_ESSENTIAL_KITCHEN';op['canonical_transform']=op['canonical_isometry'];op['access_point']=seq(work);op['assumption_notes']=op['assumptions'];op['assumptions']={'body_m':'.7','drawer_travel_m':'.6','object_size_m':'.06','drawer_lip_m':'.15','held_object_bottom_m':'.20','scope_hypothetical':True};op['front_bindings']={k:{'axis':'x','side':'max','back_wall_id':'left'}for k in fixtures}
 m={'schema':'KITCHEN_MODULE117','contract_version':'REFERENCE113_ESSENTIAL_KITCHEN_V1','fixture_catalog_hash':digest(catalog),'input_program':{'width':S(W),'depth':S(H),'body_m':'.7','spatial_program':'fridge,sink,prep,cooker with immutable reference footprints'},'bounds':[seq([-T,-1,W+T,H+T])],'unit':u,'walls':walls,'wall_hosts':hosts,'openings':[{'id':'K.kitchen.entry','rect':seq(aperture),'host_wall_id':'front','connects':['K.public_access','K.kitchen'],'kind':'permanent_open_arch','hardware':None}],'operations':{'kitchen':[op]},'external_ports':[{'id':'K.port','opening_id':'K.kitchen.entry','rect':seq([F('.45'),-1,F('1.75'),-T]),'center':seq(port),'role_id':'K.public_access','body_width':'.7'}],'reserved_approach_gross':[seq(q)for q in apron_gross],'route_failures':fail,'placement_contract':{'allowed_transforms':['translation','axis_reflection'],'uniform_scale_allowed':False,'revalidate_after_placement':True},'source_binding':{'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'fixture_source_sha256':catalog['source_file_sha256']},'accepted':False,'release_allowed':False}
 return m

if __name__=='__main__':
 m=build('2.35','3.05');Path('evidence/kitchen117_2.35x3.05.json').write_text(json.dumps(m,indent=2));print({'route_failures':m['route_failures'],'opening':m['openings'][0]})
