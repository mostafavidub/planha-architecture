from fractions import Fraction as F
from contract114 import S
from geometry114 import cells,Q,route

def install(m,u,core,p,L):
 uid=u['id'];ox,oy=map(F,p['ordered_macro']['origin'])
 def tr(r):
  a,b,c,d=map(F,r);r=[ox+a,oy+b,ox+c,oy+d]
  if uid=='B':r=[r[0],F(L)-r[3],r[2],F(L)-r[1]]
  return list(map(S,r))
 for name,r in {'stem_left':['5.6','11.4','5.75','12.1'],'stem_right':['6.75','11.4','6.9','12.1'],'cap_left':['5.25','5.6','5.4','6.75'],'cap_right':['9.3','5.6','9.45','6.75']}.items():
  for f in('walls','wall_hosts','source_wall_hosts'):m[f][uid+'.private_t.'+name]=tr(r)
 gross=[tr(['5.75','6.75','6.75','12.1']),tr(['5.4','5.75','9.3','6.75'])];parts=cells(gross,list(m['walls'].values()));u['rooms']['private_circulation']=parts;m['logical_regions'][uid+'.private_access']={'unit':uid,'parts':parts,'kind':'BOUND_PRIVATE_DOMAIN121'}
 interface=tr(['5.75','11.75','6.75','12.45']);face=oy+F('12.1');center=[ox+F('6.25'),face if uid=='A'else F(L)-face];floor=parts+[interface];qs=list(map(Q,floor));box=[min(q[0]for q in qs),min(q[1]for q in qs),max(q[2]for q in qs),max(q[3]for q in qs)];obs=list(m['walls'].values())+list(u['fixtures'].values())+cells([box],floor);paths={};fail=[]
 for name in('bed1','bed2','bed3'):
  port=next(q for q in m['module_ports']if q['opening_id']==uid+'.'+name+'.entry');path,why=route(center,port['center'],box,obs)
  if path:paths[uid+'.'+name]=path
  else:fail.append({'target':uid+'.'+name,'reason':why})
 m.setdefault('private_domains',[]).append({'unit':uid,'bedrooms':[uid+'.bed'+str(i)for i in(1,2,3)],'parts':parts,'public_interface':{'rect':interface,'open_side':'top'if uid=='A'else'bottom'},'paths':paths,'route_failures':fail,'topology_scope':'TURN_T133_NOT_ADMITTED','functional_wall_purpose':'Actual boundary of used private circulation','quality_comparison':'NOT_EVALUATED_GLOBAL_MINIMUM_OR_SUPERIORITY'})
