"""Exact axis-isometry for module witnesses; never scales furniture or certificates."""
from copy import deepcopy
from fractions import Fraction as F
from contract114 import S,digest

def reflect_x(module):
 m=deepcopy(module);W=F(m['input_program']['width'])
 def point(p):return [S(W-F(str(p[0]))),S(F(str(p[1])))]
 def rect(r):a,b,c,d=map(lambda x:F(str(x)),r);return[S(W-c),S(b),S(W-a),S(d)]
 def vector(v):return[S(-F(str(v[0]))),S(F(str(v[1])))]
 u=m['unit'];m['bounds']=[rect(r)for r in m['bounds']]
 if 'reserved_approach_gross'in m:m['reserved_approach_gross']=[rect(r)for r in m['reserved_approach_gross']]
 for k in('walls','wall_hosts'):m[k]={n:rect(q)for n,q in m[k].items()}
 u['ownership']=[rect(q)for q in u['ownership']];u['rooms']={k:[rect(q)for q in rs]for k,rs in u['rooms'].items()}
 for k in('fixtures','activities'):u[k]={n:rect(q)for n,q in u[k].items()}
 u['routes']={n:[point(p)for p in path]for n,path in u['routes'].items()};u['route_targets']={n:point(p)for n,p in u['route_targets'].items()}
 for op in m['openings']:op['rect']=rect(op['rect'])
 for port in m['external_ports']:port['rect']=rect(port['rect']);port['center']=point(port['center'])
 def motion(op):
  for k in('closed_panel','open_panel','pocket','rail_envelope'):
   if k in op:op[k]=rect(op[k])
  op['translation']=vector(op['translation'])
  for st in op.get('states',[]):
   for k in('panel_rect','actor_rect'):st[k]=rect(st[k])
   st['hand_point']=point(st['hand_point'])
  for seg in op.get('continuous_actor_segments',[]):
   for k in('actor_start','actor_end'):seg[k]=rect(seg[k])
   for k in('hand_start','hand_end'):seg[k]=point(seg[k])
 for op in m['operations'].get('doors',[]):
  motion(op);opening=next(x for x in m['openings']if x['id']==op['opening_id']);a,b,c,d=map(F,opening['rect'])
  if d-b>c-a:op['mount']['face']='min'if op['mount']['face']=='max'else'max'
 for cl in m['operations'].get('closets',[]):
  cl['shell_rects']=[rect(q)for q in cl['shell_rects']]
  if cl['front_axis']=='x':cl['front_side']='max'if cl['front_side']=='min'else'min'
  for p in cl['panels']:motion(p)
 if 'plane_x'in m.get('privacy_construction',{}):m['privacy_construction']['plane_x']=S(W-F(m['privacy_construction']['plane_x']))
 if 'shell_rects'in m.get('privacy_construction',{}):m['privacy_construction']['shell_rects']=[rect(q)for q in m['privacy_construction']['shell_rects']]
 m['isometry_binding']={'base_module_hash':digest(module),'matrix':[[-1,0],[0,1]],'translation':[S(W),'0'],'no_scale':True,'independent_revalidation_required':True}
 return m
