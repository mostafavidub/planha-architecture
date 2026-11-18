"""Experimental L3 whole-model installer; never grants whole-plan admission."""
from fractions import Fraction as F
from contract114 import S
from geometry114 import cells,Q,route

def install(m,u,core,p,L):
 uid=u['id'];ox,oy=map(F,p['ordered_macro']['origin']);H=F('9.45')
 def tr(r):
  a,b,c,d=map(F,r);r=[ox+a,oy+b,ox+c,oy+d]
  if uid=='B':r=[r[0],F(L)-r[3],r[2],F(L)-r[1]]
  return list(map(S,r))
 for name,r in {'right_exposed':['6.75','0','6.9','5.55'],'bottom':['5.6','0','6.75','.15']}.items():
  k=uid+'.private_l3.'+name;q=tr(r)
  for field in ('walls','wall_hosts','source_wall_hosts'):m[field][k]=q
 gross=[tr(['5.75','.15','6.75','9.3'])]+[r for key,rs in m['module_aprons'].items()if key.startswith(uid+'.bed')for r in rs]
 parts=cells(gross,list(m['walls'].values()));u['rooms']['private_circulation']=parts
 m['logical_regions'][uid+'.private_access']={'unit':uid,'parts':parts,'kind':'BOUND_PRIVATE_DOMAIN121'}
 interface=tr(['5.75','8.95','6.75','9.65']);face=oy+F('9.3');center=[ox+F('6.25'),face if uid=='A'else F(L)-face]
 floor=parts+[interface];coords=list(map(Q,floor));box=[min(q[0]for q in coords),min(q[1]for q in coords),max(q[2]for q in coords),max(q[3]for q in coords)]
 obstacles=list(m['walls'].values())+list(u['fixtures'].values())+cells([box],floor);paths={};fail=[]
 for name in ('bed1','bed2','bed3'):
  port=next(q for q in m['module_ports']if q['opening_id']==uid+'.'+name+'.entry');path,why=route(center,port['center'],box,obstacles)
  if path:paths[uid+'.'+name]=path
  else:fail.append({'target':uid+'.'+name,'reason':why})
 m.setdefault('private_domains',[]).append({'unit':uid,'bedrooms':[uid+'.bed'+str(i)for i in (1,2,3)],'parts':parts,'public_interface':{'rect':interface,'open_side':'top'if uid=='A'else'bottom'},'paths':paths,'route_failures':fail,'topology_scope':'EXPERIMENTAL_L3_WHOLE_INTEGRATION_NOT_ADMITTED','functional_wall_purpose':'Actual boundary of used private circulation','quality_comparison':'NOT_EVALUATED_GLOBAL_MINIMUM_OR_SUPERIORITY'})
