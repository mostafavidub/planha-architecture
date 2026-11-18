"""Real connected private circulation for one restricted three-room macro.
No claim that one interface or this shape is a source requirement/minimum.
"""
from fractions import Fraction as F
from contract114 import S
from geometry114 import Q,cells,route

def install(m,u,core,p,L):
 if not p.get('ordered_macro'):return
 uid=u['id'];rs={k:Q(v)for k,v in p['rectangles'].items()if k.startswith('bed')};beds=[rs['bed'+str(i)]for i in(1,2,3)];T=F('.15');left=beds[0][0];right=beds[-1][2];front=beds[0][1];rear=max(r[3]for r in beds)+T;back=rear+1;cx=F(p['ordered_macro']['private_interface_center_x']);half=F('.55')
 def tr(r):a,b,c,d=map(F,r);return list(map(S,[a,b,c,d]if uid=='A'else[a,F(L)-d,c,F(L)-b]))
 # These walls bound the actual circulation connecting all three private
 # functions, not a sight-only screen or an invented usable room.
 wallrects={'left_return':[left-T,rear,left,back+T],'right_return':[right,rear,right+T,back+T],'back_left':[left,rear+1,cx-half,back+T],'back_right':[cx+half,back,right,back+T]}
 for name,r in wallrects.items():
  key=uid+'.private_hall.'+name;q=tr(r);m['walls'][key]=q;m['wall_hosts'][key]=q;m['source_wall_hosts'][key]=q
 gross=[[left,rear,right,back],[cx-half,back,cx+half,back+T]]
 for a,b in zip(beds,beds[1:]):gross.append([a[2]+T,front,b[0]-T,rear])
 parts=cells([tr(q)for q in gross],list(m['walls'].values()))
 u['rooms']['private_circulation']=parts
 m['logical_regions'][uid+'.private_access']={'unit':uid,'parts':parts,'kind':'BOUND_PRIVATE_DOMAIN121'}
 face=back+T;interface=tr([cx-half,face-F('.35'),cx+half,face+F('.35')]);center=[cx,face if uid=='A'else F(L)-face]
 floor=parts+[interface];coords=list(map(Q,floor));box=[min(q[0]for q in coords),min(q[1]for q in coords),max(q[2]for q in coords),max(q[3]for q in coords)]
 obstacles=list(m['walls'].values())+list(u['fixtures'].values())+cells([box],floor);paths={};fail=[]
 for name in rs:
  opening=uid+'.'+name+'.entry';port=next(q for q in m['module_ports']if q['opening_id']==opening);path,why=route(center,port['center'],box,obstacles)
  if path:paths[uid+'.'+name]=path
  else:fail.append({'target':uid+'.'+name,'reason':why})
 m.setdefault('private_domains',[]).append({'unit':uid,'bedrooms':[uid+'.bed'+str(i)for i in(1,2,3)],'parts':parts,'public_interface':{'rect':interface,'open_side':'top'if uid=='A'else'bottom'},'paths':paths,'route_failures':fail,'topology_scope':'ORDERED_THREE_FRONT_ROOMS_REAL_REAR_HALL; limited engineering arrangement, not mandatory owner topology','functional_wall_purpose':'Boundary of actually used common private access to three bedroom ports; not a separate sight screen','quality_comparison':'NOT_EVALUATED_GLOBAL_MINIMUM_OR_SUPERIORITY'})
