"""Real connected private circulation for one restricted three-room macro.
No claim that one interface or this shape is a source requirement/minimum.
"""
import copy
from fractions import Fraction as F
from clamp_geometry359 import clamp
from private_hall_producer121 import install as source_install121
from contract114 import S
from geometry114 import Q,cells,route

def install(m,u,core,p,L):
 if not p.get('ordered_macro'):return
 uid=u['id'];rs={k:Q(v)for k,v in p['rectangles'].items()if k.startswith('bed')};beds=[rs['bed'+str(i)]for i in(1,2,3)];T=F('.15');left=beds[0][0];right=beds[-1][2];front=beds[0][1];rear=max(r[3]for r in beds)+T;back=rear+1;cx=F(p['ordered_macro']['private_interface_center_x']);half=F('.55')
 # Derive exact source-required routes on a disposable intermediate model.
 # Final model has never received old hall geometry: it is built below anew.
 tm,tu=copy.deepcopy(m),copy.deepcopy(u)
 source_install121(tm,tu,core,p,L)
 d=tm['private_domains'][-1]
 if d['route_failures']:raise ValueError('ORIGINAL_SOURCE_PATH_INCOMPLETE')
 def localpoint(q):
  a,b=map(F,q);return [a,b if uid=='A'else F(L)-b]
 def localrect(r):
  a,b,c,d=map(F,r);return [a,b,c,d]if uid=='A'else[a,F(L)-d,c,F(L)-b]
 paths={k:[localpoint(q)for q in v]for k,v in d['paths'].items()}
 if set(paths)!={uid+'.bed'+str(i)for i in(1,2,3)}:raise ValueError('ALL_BED_PORT_PATHS_REQUIRED')
 from operation_reservations359 import extract
 if not u.get('activities'):raise ValueError('SOURCE_ACTIVITY_INVENTORY_MISSING')
 operations={k:localrect(r)for k,r in extract(m['operations'],m['profile']['body_m']).items()}
 from clamp_geometry359 import rect as checked_rect
 operations.update({'activity/'+k:localrect(checked_rect(r))for k,r in u['activities'].items()})
 connectors=[[a[2]+T,front,b[0]-T,rear]for a,b in zip(beds,beds[1:])]
 cl=clamp([left,rear,right,back],connectors,localrect(d['public_interface']['rect']),paths,operations,m['profile']['body_m'])
 left,_,right,_=map(F,cl['hall'])
 m.setdefault('source_hall_clamp359',[]).append({'unit':uid,'source':'private_hall_producer121','proof':cl,'original_required_paths':d['paths'],'scope':'COUNTERFACTUAL_NEW_SOURCE_REBUILD_NOT_ACCEPTED'})
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
 m.setdefault('private_domains',[]).append({'unit':uid,'bedrooms':[uid+'.bed'+str(i)for i in(1,2,3)],'parts':parts,'public_interface':{'rect':interface,'open_side':'top'if uid=='A'else'bottom'},'paths':paths,'route_failures':fail,'topology_scope':'SOURCE359_CLAMPED_ROW_HALL; current-source functions preserved provisionally, independent validation required','functional_wall_purpose':'Boundary of actually used common private access to three bedroom ports; not a separate sight screen','quality_comparison':'NOT_EVALUATED_GLOBAL_MINIMUM_OR_SUPERIORITY'})
