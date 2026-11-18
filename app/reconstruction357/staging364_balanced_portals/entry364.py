"""Actual unit-entry surface-slide study; both unit and real lobby actors.
Preserves exact aperture and body dimensions. Hardware remains hypothetical.
"""
from fractions import Fraction as F
from contract114 import S
from geometry114 import Q

def install(m,directions):
 if set(directions)!={"A","B"}or any(type(d)is not int or d not in(-1,1)for d in directions.values()):raise ValueError("EXPLICIT_SLIDE_DIRECTION_REQUIRED")
 seq=lambda q:[S(v)for v in q]
 for opening in m['openings']:
  if opening['id']not in('A.entry','B.entry'):continue
  uid=opening['id'][0];a,b,c,d=Q(opening['rect']);span=c-a;insidebelow=uid=='A';py=b-F('.12')if insidebelow else d+F('.02');closed=(a,py,c,py+F('.1'));delta=(span,F(0));opened=(c,py,c+span,py+F('.1'));x=(a+c)/2
  opening.update(kind='operable_sliding_study',connects=['lobby',uid+'.public_access'],leaf_modeled=True)
  states=[];segments=[]
  inside_y=py-F('.75')if insidebelow else py+F('.15')
  outside_y=d+F('.05')if insidebelow else b-F('.75')
  for side,yy,owner,role in [('inside',inside_y,uid,uid+'.public_access'),('outside',outside_y,'COMMON','lobby')]:
   actor=(a-F('.05'),yy,a+F('.65'),yy+F('.7'));actor_end=(c-F('.65'),yy,c+F('.05'),yy+F('.7'));hand=(a,py+F('.05'));hand_end=(c,py+F('.05'))
   for t,p,h in [(0,closed,hand),(1,opened,hand_end)]:states.append({'unit':owner,'side':side,'role_id':role,'fraction':str(t),'panel_rect':seq(p),'actor_rect':seq(actor if t==0 else actor_end),'hand_point':seq(h)})
   segments.append({'unit':owner,'side':side,'role_id':role,'t0':'0','t1':'1','actor_start':seq(actor),'actor_end':seq(actor_end),'hand_start':seq(hand),'hand_end':seq(hand_end)})
  op={'opening_id':opening['id'],'kind':'sliding_linear','mount':{'kind':'surface','host_wall_id':opening['host_wall_id'],'face':'min'if insidebelow else'max','offset_m':'.02','panel_thickness_m':'.1'},'closed_panel':seq(closed),'open_panel':seq(opened),'translation':seq(delta),'pocket':seq(opened),'rail_envelope':seq((a,py,c+span,py+F('.1'))),'states':states,'continuous_actor_segments':segments,'assumptions':['Provisional surface-mounted entry leaf: span bound to actual aperture,0.10m panel,0.02m offset. Not manufacturer/installation approval.','Both0.7m actors are checked: private public-access union and actual shared lobby floor, not whole-plot ownership.']}
  if directions[uid]==-1:
   def mirror_rect(r):return [S(2*x-F(r[2])),r[1],S(2*x-F(r[0])),r[3]]
   def mirror_point(p):return [S(2*x-F(p[0])),p[1]]
   for k in ('closed_panel','open_panel','pocket','rail_envelope'):op[k]=mirror_rect(op[k])
   op['translation']=[S(-span),'0']
   for st in op['states']:
    st['panel_rect']=mirror_rect(st['panel_rect']);st['actor_rect']=mirror_rect(st['actor_rect']);st['hand_point']=mirror_point(st['hand_point'])
   for seg in op['continuous_actor_segments']:
    for k in ('actor_start','actor_end'):seg[k]=mirror_rect(seg[k])
    for k in ('hand_start','hand_end'):seg[k]=mirror_point(seg[k])
  op['source_slide_direction364']=directions[uid]
  m.setdefault('operations' ,{}).setdefault('doors',[]).append(op)
 return m
