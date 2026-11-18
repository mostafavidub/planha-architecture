from fractions import Fraction as F
from contract114 import S
from geometry114 import cells,Q,route

def install(m,u,core,p,L):
 uid=u['id'];ox,oy=map(F,p['ordered_macro']['origin'])
 def tr(r):
  a,b,c,d=map(F,r);r=[ox+a,oy+b,ox+c,oy+d]
  if uid=='B':r=[r[0],F(L)-r[3],r[2],F(L)-r[1]]
  return list(map(S,r))
 for name,r in {'bottom':['5.6','0','6.9','.15'],'stem_left':['5.6','4.65','5.75','6.9'],'stem_right':['6.75','4.65','6.9','5.75'],'cap_lower':['6.75','5.6','12.8','5.75'],'cap_upper_left':['5.6','6.75','7.85','6.9'],'cap_upper_right':['8.85','6.75','16.7','6.9'],'cap_end':['16.55','5.6','16.7','6.9']}.items():
  for f in('walls','wall_hosts','source_wall_hosts'):m[f][uid+'.private_sidecar.'+name]=tr(r)
 gross=[tr(['5.75','.15','6.75','6.75']),tr(['5.75','5.75','16.55','6.75'])];parts=cells(gross,list(m['walls'].values()));u['rooms']['private_circulation']=parts;m['logical_regions'][uid+'.private_access']={'unit':uid,'parts':parts,'kind':'BOUND_PRIVATE_DOMAIN121'}
 interface=tr(['7.85','6.4','8.85','7.1']);face=oy+F('6.75');center=[ox+F('8.35'),face if uid=='A'else F(L)-face];floor=parts+[interface];qs=list(map(Q,floor));box=[min(q[0]for q in qs),min(q[1]for q in qs),max(q[2]for q in qs),max(q[3]for q in qs)];obs=list(m['walls'].values())+list(u['fixtures'].values())+cells([box],floor);paths={};fail=[]
 for name in('bed1','bed2','bed3'):
  port=next(q for q in m['module_ports']if q['opening_id']==uid+'.'+name+'.entry');path,why=route(center,port['center'],box,obs)
  if path:paths[uid+'.'+name]=path
  else:fail.append({'target':uid+'.'+name,'reason':why})
 m.setdefault('private_domains',[]).append({'unit':uid,'bedrooms':[uid+'.bed'+str(i)for i in(1,2,3)],'parts':parts,'public_interface':{'rect':interface,'open_side':'top'if uid=='A'else'bottom'},'paths':paths,'route_failures':fail,'topology_scope':'SIDECAR_T136_NOT_ADMITTED','functional_wall_purpose':'Actual boundary of used private circulation','quality_comparison':'NOT_EVALUATED_GLOBAL_MINIMUM_OR_SUPERIORITY'})
