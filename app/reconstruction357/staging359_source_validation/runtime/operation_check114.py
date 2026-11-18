"""Independent witnesses, no producer imports. Unimplemented operation types fail closed."""
from checker114 import rect,F,BODY,intersects,covered,sweeps,digest

def check_operations(model,owners,solidwalls,fixtures,components=None):
 components=set(components or ('doors','closets','kitchen'))
 errors=[];pending=[];ops=model.get('operations',{})
 def err(code,**kw):errors.append(dict(code=code,**kw))
 openings={p['id']:p for p in model.get('openings',[])}
 seen=set()
 for op in ops.get('doors',[]):
  oid=op.get('opening_id');p=openings.get(oid)
  if p is None:err('OPERATION_UNKNOWN_OPENING',opening=oid);continue
  if oid in seen:err('DUPLICATE_DOOR_OPERATION',opening=oid)
  seen.add(oid)
  other_closed=[rect(z['closed_panel'])for z in ops.get('doors',[])if z.get('opening_id')!=oid and z.get('closed_panel')]
  if op.get('kind')not in('sliding_linear','pocket_source113'):pending.append('DOOR_OPERATION_KIND_UNIMPLEMENTED:'+oid);continue
  a=rect(p['rect']);closed=rect(op['closed_panel']);opened=rect(op['open_panel']);delta=tuple(F(x)for x in op['translation'])
  if len(delta)!=2 or (delta[0]!=0 and delta[1]!=0):err('DOOR_NONLINEAR_TRANSLATION',opening=oid);continue
  if tuple(closed[i]+delta[i%2]for i in range(4))!=opened:err('DOOR_PANEL_RIGIDITY',opening=oid)
  horizontal=(a[2]-a[0])>(a[3]-a[1]);axis=0 if horizontal else 1
  if delta[1-axis]!=0 or delta[axis]==0:err('PANEL_TRANSLATION_NOT_ALONG_APERTURE',opening=oid)
  pocket_source=op.get('kind')=='pocket_source113'
  if pocket_source:
   from pathlib import Path
   import json,hashlib
   raw=Path(__file__).with_name('bathroom_source117.json').read_bytes();source=json.loads(raw)
   if hashlib.sha256(raw).hexdigest()!='a31df1090677e03577f359b147052ca2cdf454863da00bdf663eafcc143e9428':err('POCKET_REFERENCE_SOURCE_CHANGED',opening=oid)
   source_key='A.'+oid.rsplit('.',1)[-1];sd=source['doors'].get(source_key)
   if sd is None:err('POCKET_REFERENCE_DOOR_ROLE',opening=oid)
   else:
    sq=rect(sd['closed_panel']);sp=rect(sd['open_panel']);source_size=sorted([sq[2]-sq[0],sq[3]-sq[1]])
    if sorted([closed[2]-closed[0],closed[3]-closed[1]])!=source_size or sum(abs(x)for x in delta)!=abs(sp[0]-sq[0])+abs(sp[1]-sq[1]):err('POCKET_SOURCE_PANEL_DIMENSION_MOTION',opening=oid)
    if closed[axis]-a[axis]!=F('.005')or a[axis+2]-closed[axis+2]!=F('.005')or closed[3-axis]-closed[1-axis]!=F('.03'):err('POCKET_SOURCE_APERTURE_CLEARANCE',opening=oid)
  elif closed[axis]!=a[axis] or closed[axis+2]!=a[axis+2] or closed[3-axis]-closed[1-axis]!=F('.1'):err('DOOR_PANEL_APERTURE_BINDING',opening=oid)
  if not pocket_source and max(opened[axis],a[axis])<min(opened[axis+2],a[axis+2]):err('DOOR_NOT_FULLY_OPEN',opening=oid)
  if pocket_source and max(opened[axis]-a[axis],a[axis+2]-opened[axis+2])<BODY:err('POCKET_SOURCE_FREE_OPEN_WIDTH',opening=oid)
  mount=op.get('mount');host_raw=model.get('wall_hosts',{}).get(p.get('host_wall_id'))
  if pocket_source:pass
  elif not mount or not host_raw:pending.append('ACTUAL_PANEL_MOUNT_NOT_BOUND:'+oid)
  else:
   host=rect(host_raw);normal=1-axis;face=mount.get('face');off=F(mount.get('offset_m',0));th=F(mount.get('panel_thickness_m',0))
   if mount.get('kind')!='surface' or mount.get('host_wall_id')!=p.get('host_wall_id')or face not in ('min','max')or off<0 or th!=F('.1'):err('SURFACE_MOUNT_CONTRACT',opening=oid)
   elif face=='min' and (closed[normal+2]!=host[normal]-off or closed[normal]!=host[normal]-off-th):err('SURFACE_MOUNT_HOST_POSITION',opening=oid)
   elif face=='max' and (closed[normal]!=host[normal+2]+off or closed[normal+2]!=host[normal+2]+off+th):err('SURFACE_MOUNT_HOST_POSITION',opening=oid)
   if not op.get('mount_assumption_unapproved') and not op.get('assumptions'):pending.append('SURFACE_MOUNT_STUDY_ASSUMPTION_NOT_DISCLOSED:'+oid)
  sweep=(min(closed[0],opened[0]),min(closed[1],opened[1]),max(closed[2],opened[2]),max(closed[3],opened[3]))
  for q in other_closed:
   if intersects(sweep,q):err('PANEL_OTHER_CLOSED_DOOR_COLLISION',opening=oid)
  pocket=rect(op['pocket'])
  if not covered(opened,[pocket]+([a]if pocket_source else[])):err('DOOR_POCKET_BINDING',opening=oid)
  # Pocket has to be represented as genuinely empty in floor solids.
  for wid,w in solidwalls.items():
   if intersects(sweep,w):err('PANEL_CONTINUOUS_WALL_COLLISION',opening=oid,wall=wid)
  for uid,fid,q in fixtures:
   if intersects(sweep,q):err('PANEL_CONTINUOUS_FIXTURE_COLLISION',opening=oid,fixture=fid)
  states=op.get('states',[])
  if not states:pending.append('DOOR_ACTOR_STATES_MISSING:'+oid)
  fractions=set()
  for st in states:
   t=F(st['fraction']);fractions.add(t)
   if not 0<=t<=1:err('DOOR_STATE_RANGE',opening=oid)
   panel=tuple(closed[i]+delta[i%2]*t for i in range(4))
   if rect(st['panel_rect'])!=panel:err('DOOR_STATE_PANEL_BINDING',opening=oid)
   actor=rect(st['actor_rect'])
   if actor[2]-actor[0]!=BODY or actor[3]-actor[1]!=BODY:err('ACTOR_BODY_CHANGED',opening=oid)
   host=owners.get(st.get('unit'),[])
   if not covered(actor,host):err('ACTOR_OUTSIDE_OWNERSHIP',opening=oid)
   for wid,w in solidwalls.items():
    if intersects(actor,w):err('ACTOR_WALL_COLLISION',opening=oid,wall=wid)
   if intersects(actor,panel):err('ACTOR_PANEL_COLLISION',opening=oid)
   if any(intersects(actor,q)for q in other_closed):err('ACTOR_OTHER_CLOSED_DOOR_COLLISION',opening=oid)
   for uid,fid,q in fixtures:
    if intersects(actor,q):err('ACTOR_FIXTURE_COLLISION',opening=oid,fixture=fid)
   hand=tuple(F(x)for x in st['hand_point'])
   if not(panel[0]<=hand[0]<=panel[2] and panel[1]<=hand[1]<=panel[3]):err('HAND_NOT_ON_PANEL',opening=oid)
   dx=(actor[0]+actor[2])/2-hand[0];dy=(actor[1]+actor[3])/2-hand[1]
   if dx*dx+dy*dy>BODY*BODY:err('HANDLE_OUT_OF_REACH',opening=oid)
  if fractions!={F(0),F(1)} and not {F(0),F(1)}<=fractions:pending.append('DOOR_ENDPOINT_STATES_MISSING:'+oid)
  # Discrete states alone never establish continuous actor travel or grip.
  ce,cp=trajectory_check(op,closed,delta,owners,list(solidwalls.values())+[q for _,_,q in fixtures]+other_closed);errors.extend({'code':code,'opening':oid}for code in ce);pending.extend(code+':'+oid for code in cp)
  connected=set(p.get('connects',[]));proven=set()
  for seg in op.get('continuous_actor_segments',[]):
   role=seg.get('role_id');parts=[]
   if role not in connected:err('ACTOR_ROLE_NOT_CONNECTED_TO_OPENING',opening=oid);continue
   if '.'in role:
    uid,rid=role.split('.',1)
    unit=next((u for u in model['units']if u['id']==uid),None)
    if unit:
     logical=model.get('logical_regions',{}).get(role)
     if logical is not None:
      if rid in('vanity','WC','shower')and logical.get('unit')==uid and 'parts'in logical:
       parts=[rect(q)for q in logical['parts']]
       if any(not covered(q,[rect(r)for r in unit['rooms'].get('bath',[])])for q in parts):err('SERVICE_REGION_OUTSIDE_ACTUAL_BATH',opening=oid,role=role)
      else:
       from typed_public_access120 import parts as typed_public_parts
       try:parts=typed_public_parts(model,unit,role,opening_id=oid)
       except ValueError as ex:err('UNAUTHORIZED_LOGICAL_ROLE_UNION',opening=oid,role=role,detail=str(ex))
     else:parts=[rect(q)for q in unit['rooms'].get(rid,[])]
   elif role in model.get('common_spaces',{}):
    value=model['common_spaces'][role];parts=[rect(q)for q in value]if isinstance(value[0],list)else[rect(value)]
   if not parts:pending.append('OPERATION_CONNECTED_ROLE_FLOOR_MISSING:'+str(role));continue
   a=rect(seg['actor_start']);b=rect(seg['actor_end']);swept=(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))
   if not covered(swept,parts):err('ACTOR_NOT_ON_DECLARED_DOOR_SIDE',opening=oid,role=role)
   else:proven.add(role)
  if proven!=connected:pending.append('BOTH_CONNECTED_ROLES_OPERATION_NOT_PROVEN:'+oid)
  if pocket_source:
   transfer=op.get('open_transfer_points')
   if not transfer:pending.append('POCKET_SOURCE_OPEN_TRANSFER_MISSING:'+oid)
   else:
    ends={tuple(map(F,transfer[0])),tuple(map(F,transfer[-1]))};stateends={((rect(st['actor_rect'])[0]+rect(st['actor_rect'])[2])/2,(rect(st['actor_rect'])[1]+rect(st['actor_rect'])[3])/2)for st in states if F(st['fraction'])==1}
    if ends!=stateends:err('POCKET_OPEN_TRANSFER_ENDPOINT_BINDING',opening=oid)
    hostfloor=[q for rs in owners.values()for q in rs]
    for q in sweeps(transfer):
     if not covered(q,hostfloor):err('POCKET_TRANSFER_OUTSIDE_REAL_FLOOR',opening=oid)
     if any(intersects(q,w)for w in list(solidwalls.values())+[opened]+other_closed+[q for _,fid,q in fixtures if 'shower_floor'not in fid]):err('POCKET_OPEN_TRANSFER_COLLISION',opening=oid)

 for oid in set(openings)-seen:
  if not source_nonleaf117(model,openings[oid]):pending.append('DOOR_OPERATION_NOT_EVALUATED:'+oid)
 if 'closets'in components:
  ce,cp=check_closets(model,owners,solidwalls,fixtures);errors.extend(ce);pending.extend(cp)
 if 'kitchen'in components:
  ke,kp=check_kitchen_stations(model,owners,solidwalls,fixtures);errors.extend(ke);pending.extend(kp)
 return errors,pending

def continuous_hit(a0,a1,b0,b1):
 """Exact existence of positive-area overlap for linearly moving rectangles.
 Partition at every affine edge-order root; strict overlap is invariant between
 consecutive roots. Endpoints also checked, so no temporal sampling assumption.
 """
 times={F(0),F(1)}
 for i,j in ((0,2),(2,0),(1,3),(3,1)):
  v=a0[i]-b0[j];d=(a1[i]-a0[i])-(b1[j]-b0[j])
  if d and 0<=-v/d<=1:times.add(-v/d)
 ts=sorted(times);probes=ts+[(x+y)/2 for x,y in zip(ts,ts[1:])]
 return any(intersects(tuple(a0[i]+(a1[i]-a0[i])*t for i in range(4)),tuple(b0[i]+(b1[i]-b0[i])*t for i in range(4)))for t in probes)

def segment_check(seg,closed,delta,hosts,obstacles):
 """Returns errors for one continuous actor/panel/hand trajectory."""
 e=[];a=rect(seg['actor_start']);b=rect(seg['actor_end']);t0=F(seg['t0']);t1=F(seg['t1'])
 if not 0<=t0<t1<=1:e.append('INVALID_OPERATION_TIME_INTERVAL')
 if any(q[2]-q[0]!=BODY or q[3]-q[1]!=BODY for q in (a,b)):e.append('CONTINUOUS_ACTOR_BODY_CHANGED')
 if a[0]!=b[0]and a[1]!=b[1]:e.append('CONTINUOUS_ACTOR_NON_ORTHOGONAL')
 swept=(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))
 if not covered(swept,hosts):e.append('CONTINUOUS_ACTOR_OUTSIDE_FLOOR')
 p0=tuple(closed[i]+delta[i%2]*t0 for i in range(4));p1=tuple(closed[i]+delta[i%2]*t1 for i in range(4))
 if continuous_hit(a,b,p0,p1):e.append('CONTINUOUS_ACTOR_PANEL_COLLISION')
 for q in obstacles:
  if continuous_hit(a,b,q,q):e.append('CONTINUOUS_ACTOR_OBSTACLE_COLLISION');break
 h0=tuple(F(v)for v in seg['hand_start']);h1=tuple(F(v)for v in seg['hand_end'])
 for actor,panel,hand in ((a,p0,h0),(b,p1,h1)):
  if not(panel[0]<=hand[0]<=panel[2]and panel[1]<=hand[1]<=panel[3]):e.append('CONTINUOUS_HAND_OFF_PANEL')
  dx=(actor[0]+actor[2])/2-hand[0];dy=(actor[1]+actor[3])/2-hand[1]
  if dx*dx+dy*dy>BODY*BODY:e.append('CONTINUOUS_HAND_REACH')
 # Fixed material handle point, rather than an arbitrary grip sliding across panel.
 if tuple(h1[i]-h0[i]for i in (0,1))!=tuple(delta[i]*(t1-t0)for i in (0,1)):e.append('HANDLE_NOT_RIGIDLY_BOUND_TO_PANEL')
 return sorted(set(e))

def trajectory_check(op,closed,delta,owners,obstacles,required_sides=None):
 errors=[];pending=[];segments=op.get('continuous_actor_segments',[])
 if not segments:return [],['CONTINUOUS_ACTOR_SEGMENTS_MISSING']
 groups={}
 for seg in segments:
  key=(seg.get('unit'),seg.get('side'))
  if key[1]not in (required_sides or {'inside','outside'}):errors.append('OPERATION_SIDE_UNSPECIFIED')
  groups.setdefault(key,[]).append(seg)
  errors.extend(segment_check(seg,closed,delta,owners.get(key[0],[]),obstacles))
 if {key[1]for key in groups}!=(required_sides or {'inside','outside'}):pending.append('REQUIRED_OPERATION_SIDES_NOT_PROVEN')
 for key,ss in groups.items():
  ss=sorted(ss,key=lambda s:F(s['t0']))
  if F(ss[0]['t0'])!=0 or F(ss[-1]['t1'])!=1:errors.append('OPERATION_TIME_COVERAGE')
  for a,b in zip(ss,ss[1:]):
   if F(a['t1'])!=F(b['t0'])or rect(a['actor_end'])!=rect(b['actor_start'])or tuple(map(F,a['hand_end']))!=tuple(map(F,b['hand_start'])):errors.append('OPERATION_TRAJECTORY_DISCONTINUITY')
  for fraction,keyactor,keyhand in ((F(0),'actor_start','hand_start'),(F(1),'actor_end','hand_end')):
   seg=ss[0]if fraction==0 else ss[-1]
   match=[st for st in op.get('states',[])if F(st['fraction'])==fraction and st.get('unit')==key[0]and st.get('side')==key[1]]
   if len(match)!=1 or rect(match[0]['actor_rect'])!=rect(seg[keyactor])or tuple(map(F,match[0]['hand_point']))!=tuple(map(F,seg[keyhand])):errors.append('CONTINUOUS_ENDPOINT_STATE_BINDING')
 return sorted(set(errors)),pending

def check_closets(model,owners,walls,fixtures):
 errors=[];pending=[];expected={(u['id'],k)for u in model['units']for k,md in u['fixture_metadata'].items()if md['kind']=='closet'};seen=set()
 def err(code,**kw):errors.append(dict(code=code,**kw))
 for item in model.get('operations',{}).get('closets',[]):
  uid,fid=item.get('unit'),item.get('fixture_id');key=(uid,fid)
  if key not in expected or key in seen:err('CLOSET_OPERATION_INVENTORY',unit=uid,fixture=fid);continue
  seen.add(key);unit=next(u for u in model['units']if u['id']==uid);f=rect(unit['fixtures'][fid]);axis=0 if item['front_axis']=='x'else 1;long=1-axis;side=item['front_side'];panels=item.get('panels',[])
  if len(panels)!=2:err('CLOSET_TWO_HALF_PANELS_REQUIRED',fixture=fid);continue
  if not item.get('assumption') and not item.get('assumptions'):pending.append('CLOSET_HARDWARE_ASSUMPTION_NOT_DISCLOSED:'+uid+'.'+fid)
  lengths=[];closedpanels=[]
  for p in panels:
   a=rect(p['closed_panel']);b=rect(p['open_panel']);d=tuple(map(F,p['translation']));closedpanels.append(a)
   if not covered(a,[f])or not covered(b,[f]):err('CLOSET_PANEL_OUTSIDE_FIXTURE',fixture=fid)
   if a[long+2]-a[long]!=(f[long+2]-f[long])/2:err('CLOSET_HALF_PANEL_LENGTH',fixture=fid)
   if a[axis+2]-a[axis]!=F('.04'):err('CLOSET_STUDY_PANEL_THICKNESS',fixture=fid)
   if d[axis]!=0 or tuple(a[i]+d[i%2]for i in range(4))!=b:err('CLOSET_PANEL_RIGID_TRANSLATION',fixture=fid)
   if abs(d[long])!=(f[long+2]-f[long])/2:err('CLOSET_PANEL_NOT_HALF_OPEN',fixture=fid)
   lengths.append((a[long],a[long+2]));sweep=(min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))
   if not covered(sweep,[rect(p['rail_envelope'])])or not covered(rect(p['rail_envelope']),[f]):err('CLOSET_REAL_RAIL_BINDING',fixture=fid)
   for q in list(walls.values())+[q for u,k,q in fixtures if (u,k)!=key]+[rect(q)for q in item.get('shell_rects',[])]:
    if intersects(sweep,q):err('CLOSET_PANEL_CONTINUOUS_OBSTACLE',fixture=fid)
   ce,cp=trajectory_check(p,a,d,owners,list(walls.values())+[q for _,_,q in fixtures],{'front'})
   errors.extend({'code':c,'unit':uid,'fixture':fid}for c in ce);pending.extend(c+':'+uid+'.'+fid for c in cp)
   for seg in p.get('continuous_actor_segments',[]):
    for ak in ('actor_start','actor_end'):
     q=rect(seg[ak])
     if side=='min'and q[axis+2]>f[axis]or side=='max'and q[axis]<f[axis+2]:err('CLOSET_ACTOR_WRONG_FRONT',fixture=fid)
  lengths.sort()
  if lengths[0][0]!=f[long]or lengths[0][1]!=lengths[1][0]or lengths[1][1]!=f[long+2]:err('CLOSET_CLOSED_FACE_PARTITION',fixture=fid)
  if intersects(*closedpanels):err('CLOSET_RAILS_NOT_DISTINCT',fixture=fid)
  if not item.get('shell_rects'):pending.append('CLOSET_ACTUAL_SHELL_MISSING:'+uid+'.'+fid)
  for q in item.get('shell_rects',[]):
   if not covered(rect(q),[f]):err('CLOSET_SHELL_OUTSIDE_FURNITURE',fixture=fid)
 for uid,fid in expected-seen:pending.append('CLOSET_HALF_PANEL_OPERATION_NOT_EVALUATED:'+uid+'.'+fid)
 return errors,pending

def check_kitchen_stations(model,owners,walls,fixtures):
 errors=[];pending=[];seen=set()
 def err(code,**kw):errors.append(dict(code=code,**kw))
 for op in model.get('operations',{}).get('kitchen',[]):
  uid=op['unit'];seen.add(uid)
  if op.get('kind')=='REFERENCE113_ESSENTIAL_KITCHEN':
   result=check_reference_kitchen117(model,op);errors.extend(result['errors']);pending.extend(result['pending']);continue
  u=next(u for u in model['units']if u['id']==uid);required={'fridge','sink','prep','cooker'};got=[]
  for st in op.get('workstations',[]):
   fid=st['fixture_id'];got.append(fid)
   if fid not in required:err('KITCHEN_UNKNOWN_STATION',fixture=fid);continue
   f=rect(u['fixtures'][fid]);a=rect(st['actor_rect']);axis=0 if st['front']['axis']=='x'else 1;side=st['front']['side'];hand=tuple(map(F,st['hand_point']))
   if a[2]-a[0]!=BODY or a[3]-a[1]!=BODY:err('KITCHEN_ACTOR_BODY')
   if not covered(a,[rect(q)for q in u['rooms']['kitchen']]):err('KITCHEN_ACTOR_NOT_ON_KITCHEN_FLOOR')
   if side=='min'and a[axis+2]>f[axis]or side=='max'and a[axis]<f[axis+2]:err('KITCHEN_ACTOR_WRONG_FRONT')
   if hand[axis]!=(f[axis]if side=='min'else f[axis+2])or not f[1-axis]<=hand[1-axis]<=f[3-axis]:err('KITCHEN_HAND_NOT_ON_ACTUAL_FRONT')
   dx=(a[0]+a[2])/2-hand[0];dy=(a[1]+a[3])/2-hand[1]
   if dx*dx+dy*dy>BODY*BODY:err('KITCHEN_STATION_REACH')
   if any(intersects(a,q)for q in list(walls.values())+[q for _,_,q in fixtures]):err('KITCHEN_STATION_COLLISION')
  if set(got)!=required or len(got)!=4:err('KITCHEN_STATION_INVENTORY')
  stations={st['fixture_id']:rect(st['actor_rect'])for st in op.get('workstations',[])}
  required_nodes=required|{'dining'};seen_pairs=set()
  for rr in op.get('routes',[]):
   pair=(rr['from'],rr['to']);seen_pairs.add(pair)
   if F(rr.get('body_width',0))!=BODY:err('KITCHEN_ROUTE_BODY_CHANGED')
   path=rr['path'];start=tuple(map(F,path[0]));end=tuple(map(F,path[-1]))
   if pair[0]in stations:
    aa=stations[pair[0]]
    if start!=((aa[0]+aa[2])/2,(aa[1]+aa[3])/2):err('KITCHEN_ROUTE_START_BINDING')
   else:err('KITCHEN_ROUTE_UNKNOWN_START')
   if pair[1]in stations:
    aa=stations[pair[1]]
    if end!=((aa[0]+aa[2])/2,(aa[1]+aa[3])/2):err('KITCHEN_ROUTE_END_BINDING')
   elif pair[1]=='dining':
    aa=(end[0]-BODY/2,end[1]-BODY/2,end[0]+BODY/2,end[1]+BODY/2)
    if not covered(aa,[rect(q)for k,q in u['activities'].items()if k.startswith('dining')]):err('KITCHEN_DINING_TARGET_NOT_ACTIVITY')
   else:err('KITCHEN_ROUTE_UNKNOWN_END')
   for q in sweeps(path):
    if not covered(q,owners[uid]):err('KITCHEN_ROUTE_OUTSIDE_OWNERSHIP')
    if any(intersects(q,z)for z in list(walls.values())+[q for _,_,q in fixtures]):err('KITCHEN_ROUTE_OBSTACLE_COLLISION')
  connected={'fridge'}
  for _ in range(len(required_nodes)):
   for a,b in seen_pairs:
    if a in connected or b in connected:connected.update((a,b))
  if not required_nodes<=connected:pending.append('KITCHEN_TASK_ROUTE_CONNECTIVITY:'+uid)
  # Standing/reaching is not a substitute for refrigerator leaf and drawer use.
  pending.append('KITCHEN_FRIDGE_LEAF_DRAWER_OBJECT_OPERATION_NOT_PROVEN:'+uid)
 for u in model['units']:
  if u['id']not in seen:pending.append('KITCHEN_OPERATION_NOT_EVALUATED:'+u['id'])
 return errors,pending

# Transferred essential motion contract: reference113 audit_lr_kitchen/check.py.
# No historical coordinates, receipts, producer imports or fixed plot depth.
def _kbox(points,pad=0):
 ps=[tuple(map(F,p))for p in points];p=F(pad)
 return(min(x[0]for x in ps)-p,min(x[1]for x in ps)-p,max(x[0]for x in ps)+p,max(x[1]for x in ps)+p)
def _segment_hits(a,b,r):
 a,b=tuple(map(F,a)),tuple(map(F,b));times={F(0),F(1)}
 for axis in (0,1):
  d=b[axis]-a[axis]
  if d:
   for edge in(r[axis],r[axis+2]):
    t=(edge-a[axis])/d
    if 0<=t<=1:times.add(t)
 ts=sorted(times)
 return any(r[0]<a[0]+(b[0]-a[0])*t<r[2]and r[1]<a[1]+(b[1]-a[1])*t<r[3]for t in ts+[(x+y)/2 for x,y in zip(ts,ts[1:])])

def audit_canonical_kitchen117(floor,fixtures,walls,access):
 """Continuous conservative quarter-turn leaf boxes and exact linear drawer/
 actor/object sweeps. Canonical cabinet fronts face -x. Same scoped113 assumptions.
 """
 import math
 errors=[];rows={};obs=dict(walls);obs.update(fixtures);eps=F('0.000000001')
 def check(q,ob=None,host=True):
  ob=obs if ob is None else ob
  return (['outside_kitchen']if host and not covered(q,floor)else[])+[k for k,z in ob.items()if intersects(q,z)]
 def path(ps,ob=None):return [(i,check(_kbox([a,b],'.35'),ob))for i,(a,b)in enumerate(zip(ps,ps[1:]))if check(_kbox([a,b],'.35'),ob)]
 q=fixtures['fridge'];hx,hy=q[0],q[3]
 if (q[2]-q[0],q[3]-q[1])!=(F('.7'),F('.7')):errors.append('fridge_dimensions')
 def state(theta):
  grip=(F(str(float(hx)-.74*math.sin(theta))),F(str(float(hy)-.74*math.cos(theta))))
  actor=(grip[0]-F('.45'),grip[1]-F('.45'))
  tip=(F(str(float(hx)-.7*math.sin(theta))),F(str(float(hy)-.7*math.cos(theta))))
  return grip,actor,tip
 for i in range(360):
  a,b=state(i*math.pi/720),state((i+1)*math.pi/720)
  leaf=_kbox([(hx,hy),a[2],b[2]],F('.03')+eps);body=_kbox([a[1],b[1]],F('.35')+eps);hand=_kbox([a[0],a[1],b[0],b[1]],eps)
  hits=check(body,{**obs,'own_leaf_box':leaf})+check(hand)
  if hits:errors.append({'fridge_interval':i,'hits':hits})
  hits=check(leaf,{k:z for k,z in obs.items()if k!='fridge'},False)
  if hits:errors.append({'fridge_leaf_interval':i,'hits':hits})
 start=state(0)[1];end=state(math.pi/2)[1];shelf_access=(hx-F('.4'),hy-F('.45'));openleaf=(hx-F('.73'),hy-F('.03'),hx+F('.03'),hy+F('.03'))
 if path([access,start]):errors.append('fridge_closed_approach')
 if path([end,shelf_access],{**obs,'leaf':openleaf}):errors.append('fridge_open_access')
 target=(hx+F('.15'),shelf_access[1]);held=(hx-F('.15'),shelf_access[1]);shell={'fridge_shell_back':(q[2]-F('.05'),q[1],q[2],q[3]),'fridge_shell_low':(q[0],q[1],q[2],q[1]+F('.05')),'fridge_shell_high':(q[0],q[3]-F('.05'),q[2],q[3])}
 ro={**{k:z for k,z in obs.items()if k!='fridge'},**shell,'leaf':openleaf}
 if check(_kbox([target,held],'.03'),ro):errors.append('fridge_object')
 if any(_segment_hits(shelf_access,target,z)for z in ro.values()):errors.append('fridge_hand')
 for role in('sink','prep','cooker'):
  q=fixtures[role];front=q[0];cy=(q[1]+q[3])/2;closed=(front-F('.45'),cy);rs=[]
  if path([access,(closed[0],access[1]),closed]):rs.append('approach')
  if check(_kbox([closed],'.35')):rs.append('surface_body')
  if any(_segment_hits(closed,(front+F('.15'),cy),z)for k,z in obs.items()if k!=role):rs.append('surface_hand')
  if role!='cooker':
   opened=(closed[0]-F('.6'),cy);other={k:z for k,z in obs.items()if k!=role};tray=(front-F('.6'),q[1]+F('.02'),q[2]-F('.02'),q[3]-F('.02'))
   if check(_kbox([closed,opened],'.35')):rs.append('body_translation')
   if check(tray,other):rs.append('tray_translation')
   grip0=(front-F('.03'),cy)
   if any(_segment_hits(opened,grip0,z)for z in other.values()):rs.append('hand_translation')
   if front-F('.6')-(opened[0]+F('.35'))!=F('.1'):rs.append('own_tray_separation')
   target=(front-F('.45'),cy);held=(opened[0]+F('.25'),cy)
   if check(_kbox([target,held],'.03'),other):rs.append('object_path')
   interior=(front-F('.55'),q[1]+F('.05'),q[2]-F('.65'),q[3]-F('.05'))
   if not covered(_kbox([target],'.03'),[interior]):rs.append('object_not_inside_drawer')
   if any(_segment_hits(opened,target,z)for z in other.values()):rs.append('storage_hand')
  rows[role]={'errors':rs};errors.extend({'role':role,'error':e}for e in rs)
 return {'errors':errors,'fridge_interval_count':360,'interval_rounding_padding_m':str(eps),'drawers_and_surfaces':rows,'accepted':False,'scope':'Reference113 essential hypothetical refrigerator/drawer/worktop motions; not hardware certification, full cooking, oven loading, daylight or ventilation.'}

def check_reference_kitchen117(model,op):
 errors=[];pending=[];uid=op['unit'];unit=next(u for u in model['units']if u['id']==uid)
 def err(code,**kw):errors.append(dict(code=code,unit=uid,**kw))
 try:
  if op.get('kind')!='REFERENCE113_ESSENTIAL_KITCHEN':err('KITCHEN_MOTION_CONTRACT_KIND')
  required={'body_m':'.7','drawer_travel_m':'.6','object_size_m':'.06','drawer_lip_m':'.15','held_object_bottom_m':'.20'}
  for k,v in required.items():
   if F(op.get('assumptions',{}).get(k,0))!=F(v):err('KITCHEN_SOURCE_MOTION_PARAMETER',parameter=k)
  if op.get('assumptions',{}).get('scope_hypothetical')is not True:err('KITCHEN_HYPOTHETICAL_SCOPE_NOT_DISCLOSED')
  transform=op['canonical_transform'];matrix=[[F(v)for v in row]for row in transform['matrix']];offset=tuple(map(F,transform['translation']))
  if len(matrix)!=2 or any(sum(abs(v)for v in row)!=1 for row in matrix)or any(sum(abs(matrix[i][j])for i in(0,1))!=1 for j in(0,1))or any(v not in(-1,0,1)for row in matrix for v in row):raise ValueError('CANONICAL_TRANSFORM_NOT_ISOMETRY')
  def pt(q):return tuple(sum(matrix[i][j]*F(q[j])for j in(0,1))+offset[i]for i in(0,1))
  def tr(q):
   q=rect(q);ps=[pt((x,y))for x in(q[0],q[2])for y in(q[1],q[3])];return(min(x[0]for x in ps),min(x[1]for x in ps),max(x[0]for x in ps),max(x[1]for x in ps))
  for name in('fridge','sink','prep','cooker'):
   fb=op.get('front_bindings',{}).get(name)
   if not fb:err('KITCHEN_ACTUAL_FRONT_BINDING_MISSING',fixture=name);continue
   axis=0 if fb['axis']=='x'else 1;sign=1 if fb['side']=='max'else-1;normal=[F(0),F(0)];normal[axis]=sign
   if tuple(sum(matrix[i][j]*normal[j]for j in(0,1))for i in(0,1))!=(-1,0):err('KITCHEN_FRONT_NOT_CANONICAL_NEGATIVE_X',fixture=name)
   fixture=rect(unit['fixtures'][name]);wall=rect(model['walls'][fb['back_wall_id']])
   touching=(fixture[axis]==wall[axis+2])if sign==1 else(fixture[axis+2]==wall[axis])
   if not touching or wall[1-axis]>fixture[1-axis]or wall[3-axis]<fixture[3-axis]:err('KITCHEN_BACK_NOT_ON_ACTUAL_WALL',fixture=name)
  floor=[tr(q)for q in unit['rooms']['kitchen']];fx={k:tr(q)for k,q in unit['fixtures'].items()if k!='shower_floor'};walls={k:tr(q)for k,q in model['walls'].items()}
  for other in model['units']:
   if other['id']!=uid:walls.update({other['id']+'.fixture.'+k:tr(q)for k,q in other['fixtures'].items()})
  access=pt(op['access_point']);body=(access[0]-BODY/2,access[1]-BODY/2,access[0]+BODY/2,access[1]+BODY/2)
  if not covered(body,floor):err('KITCHEN_ACCESS_BODY_NOT_ON_FLOOR')
  actual_access=tuple(map(F,op['access_point']))
  if not any(tuple(map(F,path[-1]))==actual_access for path in unit.get('routes',{}).values()if path):err('KITCHEN_ACCESS_NOT_ROUTE_BOUND')
  evidence=audit_canonical_kitchen117(floor,fx,walls,access)
  if evidence['errors']:err('KITCHEN_REFERENCE113_ESSENTIAL_MOTION_FAILURE',details=evidence['errors'])
 except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as ex:err('KITCHEN_OPERATION_SCHEMA',detail=str(ex));evidence={}
 return {'errors':errors,'pending':pending,'evidence':evidence,'status':'FAIL_SCOPED'if errors else'PASS_SCOPED_ESSENTIAL_KITCHEN','accepted':False}

def pocket_host_geometry117(model,opening,solidwalls):
 """113 pocket host is the adjacent receiving wall, NOT the opening rectangle."""
 from checker114 import encloses
 q=rect(opening['rect']);host=rect(model['wall_hosts'][opening['host_wall_id']]);ops=[o for o in model.get('operations',{}).get('doors',[])if o['opening_id']==opening['id']and o.get('kind')=='pocket_source113'];errors=[]
 if len(ops)!=1:return ['POCKET_SOURCE_ACTUAL_OPERATION_BINDING']
 op=ops[0];axis=0 if q[2]-q[0]>q[3]-q[1]else 1;normal=1-axis
 if q[normal]!=host[normal]or q[normal+2]!=host[normal+2]or not(q[axis+2]==host[axis]or host[axis+2]==q[axis]):errors.append('POCKET_HOST_NOT_ADJACENT_COLLINEAR_WALL')
 void=rect(op['pocket']);parts=[r for r in solidwalls.values()if encloses(host,r)]+[void]
 if not covered(host,parts):errors.append('POCKET_HOST_SKIN_VOID_PARTITION')
 if any(intersects(q,w)for w in solidwalls.values()):errors.append('POCKET_APERTURE_NOT_ACTUALLY_CUT')
 return errors


def source_nonleaf117(model,p):
 """Only source-bound kitchen arches and two actual core interfaces, not flags alone.
 Whole placement gate independently checks every transformed source field.
 """
 oid=p.get('id','');links=set(p.get('connects',[]))
 if p.get('kind')=='permanent_open_arch' and p.get('hardware') is None:
  for pl in model.get('module_placements',[]):
   src=pl.get('module',{})
   if src.get('schema')!='KITCHEN_MODULE117' or pl.get('room_id')!='kitchen':continue
   uid=pl.get('unit_id');mapping=pl.get('id_map',{})
   public_role=mapping.get('K.public_access')
   if public_role not in(uid+'.public_access',uid+'.kitchen_public_access')or links!={uid+'.kitchen',public_role}:continue
   try:
    from typed_public_access120 import parts as typed_public_parts
    unit=next(u for u in model['units']if u['id']==uid)
    typed_public_parts(model,unit,public_role,opening_id=oid)
   except (KeyError,ValueError,TypeError,StopIteration):continue
   for opening in src.get('openings',[]):
    if mapping.get(opening.get('id'))==oid and opening.get('kind')=='permanent_open_arch' and opening.get('hardware') is None and not src.get('operations',{}).get('doors'):
     try:
      if pl.get('module_hash')!=digest(src)or p.get('host_wall_id')!=mapping.get(opening['host_wall_id']):continue
      mat=[[F(x)for x in row]for row in pl['transform']['matrix']];off=list(map(F,pl['transform']['translation']))
      from d4_contract125 import matrix as d4_matrix
      try:mat=d4_matrix(mat)
      except ValueError:continue
      r=rect(opening['rect']);pts=[tuple(sum(mat[i][j]*v[j]for j in(0,1))+off[i]for i in(0,1))for v in((r[0],r[1]),(r[2],r[3]))]
      expected=(min(v[0]for v in pts),min(v[1]for v in pts),max(v[0]for v in pts),max(v[1]for v in pts))
      if rect(p['rect'])!=expected or links!={mapping.get(k,k)for k in opening['connects']}:continue
      if any(o.get('opening_id')==oid for o in model.get('operations',{}).get('doors',[])):continue
      return True
     except (KeyError,ValueError,TypeError,IndexError):continue
 if oid not in ('stair.entry','lift.entry'):return False
 role=oid.split('.')[0]
 if p.get('kind')!='core_access_interface' or p.get('leaf_modeled') is not False or links!={role,'lobby'}:return False
 if p.get('operation_witness_status')!='NOT_MODELED_HARDWARE_OUTSIDE_CONCEPT_INTERFACE':return False
 try:
  core=rect(model['common_spaces'][role]);a=rect(p['rect']);host=rect(model['wall_hosts'][p['host_wall_id']])
  if not covered(a,[host]):return False
  touch=((a[2]==core[0] or a[0]==core[2])and core[1]<=a[1]<a[3]<=core[3])or((a[3]==core[1]or a[1]==core[3])and core[0]<=a[0]<a[2]<=core[2])
  return touch and min(a[2]-a[0],a[3]-a[1])<=F('.15') and max(a[2]-a[0],a[3]-a[1])>=BODY
 except (KeyError,ValueError,TypeError):return False
