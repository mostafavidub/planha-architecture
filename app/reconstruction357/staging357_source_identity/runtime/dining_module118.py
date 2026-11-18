"""Variable four-place dining geometry using immutable reference furniture.
Four distinct chairs are not four proven usable seats until motion/rise checks.
"""
from fractions import Fraction as F
from contract114 import S,digest
import json
from pathlib import Path

def build(width='3.1',depth='3.5',table_offset_x='0',table_offset_y='0'):
 W,H=F(width),F(depth);x=(W-F('.8'))/2+F(table_offset_x);y=(H-F('1.2'))/2+F(table_offset_y)
 seq=lambda q:list(map(S,q));table=(x,y,x+F('.8'),y+F('1.2'))
 chairs={'west':(x-F('.5'),y+F('.35'),x,y+F('.85')),'east':(x+F('.8'),y+F('.35'),x+F('1.3'),y+F('.85')),'front':(x+F('.15'),y-F('.5'),x+F('.65'),y),'back':(x+F('.15'),y+F('1.2'),x+F('.65'),y+F('1.7'))}
 vectors={'west':(-F('.4'),F(0)),'east':(F('.4'),F(0)),'front':(F(0),-F('.4')),'back':(F(0),F('.4'))}
 instances=[]
 for name,q in chairs.items():
  d=vectors[name];pulled=tuple(v+d[i%2]for i,v in enumerate(q))
  instances.append({'id':'seat_'+name,'fixture_id':'chair_'+name,'closed_rect':seq(q),'pulled_rect':seq(pulled),'translation':seq(d),'source_profile':'reference102_0.4m_pull_study_not_regulation','capacity_role':'distinct_dining_place','occupied_body':None,'rise_transfer':None})
 # Actual occupied/rise study witnesses. Own-chair support is explicitly
 # declared, not silently removed from obstacles. This is not validated ergonomics.
 for seat in instances:
  name=seat['id'][5:];q=chairs[name];de=vectors[name];cx=(q[0]+q[2])/2;cy=(q[1]+q[3])/2
  nx,ny=de[0]/F('.4'),de[1]/F('.4');cx+=nx*F('.1');cy+=ny*F('.1')
  body=lambda px,py:seq((px-F('.35'),py-F('.35'),px+F('.35'),py+F('.35')))
  occupied=body(cx,cy);pulledbody=body(cx+de[0],cy+de[1]);standcenter=(cx+de[0]-(F('.85')if ny else 0),cy+de[1]-(F('.85')if nx else 0));standing=body(*standcenter)
  seat['occupied_body']=occupied
  seat['rise_transfer']={'profile':'BODY0.7_PLAN_STUDY_WITH_EXPLICIT_OWN_SEAT_SUPPORT','source_body_m':'.7','closed_occupied_body':occupied,'pulled_occupied_body':pulledbody,'standing_body':standing,'segments':[{'phase':'seated_pull','actor_start':occupied,'actor_end':pulledbody,'chair_start':seat['closed_rect'],'chair_end':seat['pulled_rect'],'own_chair_contact':'seated_support_only'},{'phase':'rise_and_side_exit_study','actor_start':pulledbody,'actor_end':standing,'chair_start':seat['pulled_rect'],'chair_end':seat['pulled_rect'],'own_chair_contact':'UNVALIDATED_VERTICAL_SEAT_TRANSFER_NOT_A_COLLISION_EXEMPTION'}],'other_seats_remain_occupied':True,'human_transfer_and_support_profile_validated':False}
 cat=json.loads(Path(__file__).with_name('fixture_catalog114.json').read_text())
 return {'schema':'DINING_CAPACITY_MODULE118_PROPOSAL','width':S(W),'depth':S(H),'fixture_catalog_hash':digest(cat),'fixtures':{'table':seq(table),**{'chair_'+k:seq(v)for k,v in chairs.items()}},'fixture_metadata':{'table':{'kind':'dining_table'},**{'chair_'+k:{'kind':'dining_chair_front','physical_size_unchanged':True}for k in chairs}},'seating':{'requested_places':4,'distinct_chair_count':4,'instances':instances},'pending':['ALL_OTHER_SEATS_OCCUPIED_PULL_AND_RISE','GUEST_ENTRY_AND_SERVING_ROUTES','BODY_HAND_CONTINUITY_AND_TABLE_ACCESS'],'accepted':False,'size_bounds':'Room dimensions/offsets are candidate parameters, not standard minima.'}
