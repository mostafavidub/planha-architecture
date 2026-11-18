"""Construct actual, provisional surface-slide motion studies, never a pass flag.
Mounted panel/actor motions may collide; the independent checker decides.
Hardware sizes here are explicit study assumptions, not owner-approved hardware.
"""
from fractions import Fraction as F
from contract114 import S
from geometry114 import Q

def construct_bedroom_motion_studies(m):
 out=[]
 for o in m['openings']:
  if '.bed'not in o['id']:continue
  uid,room,side=o['id'].split('.');a,b,c,d=Q(o['rect']);host=Q(m['wall_hosts'][o['host_wall_id']]);length=d-b
  inner=side=='left';face='max'if inner else'min';offset=F('.02');thick=F('.1')
  x=host[2]+offset if inner else host[0]-offset-thick
  closed=(x,b,x+thick,d);delta=(F(0),length if uid=='A'else-length);opened=tuple(v+delta[i%2]for i,v in enumerate(closed))
  def seq(q):return [S(v)for v in q]
  states=[];segments=[]
  # Two actual actor paths, not metadata-only claims. They are deliberately
  # checked against the existing room/fixture model and may be rejected.
  for actside in ('inside','outside'):
   normal_sign=1 if inner else -1
   if actside=='outside':normal_sign=-normal_sign
   xx=(closed[2]+F('.05'))if normal_sign==1 else(closed[0]-F('.75'))
   if actside=='outside':xx=host[0]-F('.75')if inner else host[2]+F('.05')
   yy=(b+d)/2-F('.35');actor=(xx,yy,xx+F('.7'),yy+F('.7'));end=actor
   hand=((closed[0]+closed[2])/2,b if uid=='A'else d);hand_end=(hand[0]+delta[0],hand[1]+delta[1]);role=uid+'.'+room if actside=='inside'else uid+'.public_access'
   for t,panel,body,h in [(0,closed,actor,hand),(1,opened,end,hand_end)]:states.append({'unit':uid,'side':actside,'role_id':role,'fraction':str(t),'panel_rect':seq(panel),'actor_rect':seq(body),'hand_point':seq(h)})
   segments.append({'unit':uid,'side':actside,'role_id':role,'t0':'0','t1':'1','actor_start':seq(actor),'actor_end':seq(end),'hand_start':seq(hand),'hand_end':seq(hand_end)})
  out.append({'opening_id':o['id'],'kind':'sliding_linear','mount':{'kind':'surface','host_wall_id':o['host_wall_id'],'face':face,'offset_m':'.02','panel_thickness_m':'.1'},'closed_panel':seq(closed),'open_panel':seq(opened),'translation':seq(delta),'pocket':seq(opened),'rail_envelope':seq((min(closed[0],opened[0]),min(closed[1],opened[1]),max(closed[2],opened[2]),max(closed[3],opened[3]))),'states':states,'continuous_actor_segments':segments,'assumptions':['Surface-mounted 0.10m panel with 0.02m offset is provisional hardware geometry, not an approved specification.','Existing fixture layout is not silently moved; collisions must reject this study.']})
 m.setdefault('operations',{})['doors']=out
 m['operation_study_scope']='Bedroom surface-panel/actor trajectories constructed; not evidence of success. Other operation types remain pending.'
 return m
