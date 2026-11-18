"""Independent named public-use checks; no producer imports or acceptance flags.
Sources: Blueprint286,293–295,377–382,3988–3990; reference gate102 .4m
chair-study displacement is not law. No population/seat count inferred from area
or sofa length. Missing complete inventory/scenario remains named NOT_EVALUATED.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
B=F('.7')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def q(r):
 a=tuple(F(str(x))for x in r)
 if len(a)!=4 or a[0]>=a[2]or a[1]>=a[3]:raise ValueError('BAD_RECT')
 return a
def hit(a,b):return max(a[0],b[0])<min(a[2],b[2])and max(a[1],b[1])<min(a[3],b[3])
def covered(r,parts):
 xs=sorted({r[0],r[2]}|{p[i]for p in parts for i in(0,2)if r[0]<p[i]<r[2]});ys=sorted({r[1],r[3]}|{p[i]for p in parts for i in(1,3)if r[1]<p[i]<r[3]})
 return all(any(p[0]<=a and b<=p[2]and p[1]<=c and d<=p[3]for p in parts)for a,b in zip(xs,xs[1:])for c,d in zip(ys,ys[1:]))
def sweeps(path):
 if not isinstance(path,list)or len(path)<2:raise ValueError('ROUTE_MISSING')
 pts=[tuple(F(str(x))for x in p)for p in path];out=[]
 for a,b in zip(pts,pts[1:]):
  if len(a)!=2 or len(b)!=2 or a==b or(a[0]!=b[0]and a[1]!=b[1]):raise ValueError('NONORTHOGONAL_ROUTE')
  out.append((min(a[0],b[0])-B/2,min(a[1],b[1])-B/2,max(a[0],b[0])+B/2,max(a[1],b[1])+B/2))
 return out

def examine(model):
 errors=[];pending=[];rows=[];gid=digest(model)
 def fail(code,**kw):errors.append({'code':code,**kw})
 def wait(code):pending.append(code)
 try:
  walls={k:q(v)for k,v in model['walls'].items()};doors=model.get('operations',{}).get('doors',[]);chair_ops=model.get('operations',{}).get('dining_chairs',[])
  for u in model['units']:
   uid=u['id'];fixtures={k:q(v)for k,v in u['fixtures'].items()};acts={k:q(v)for k,v in u.get('activities',{}).items()};rooms={k:list(map(q,v))for k,v in u['rooms'].items()};owner=list(map(q,u['ownership']));program=u.get('public_program',{})
   private=[p for k,rs in rooms.items()if k.startswith('bed')or k=='bath'for p in rs]
   kitchen=rooms.get('kitchen',[])+[v for k,v in acts.items()if k.startswith('kitchen')]
   kmotion=[]
   for k in model.get('operations',{}).get('kitchen',[]):
    if k.get('unit')==uid:
     for piece in k.get('motion_envelopes',[]):kmotion.append(q(piece))
   # Missing motion data cannot be excused by a kitchen room label.
   if not any(k.get('unit')==uid and k.get('motion_envelopes')for k in model.get('operations',{}).get('kitchen',[])):wait('PUBLIC_KITCHEN_MOTION_ENVELOPES_MISSING:'+uid)
   chairids={k for k in fixtures if 'dining_chair'in k or u.get('fixture_metadata',{}).get(k,{}).get('kind','').startswith('dining_chair')}
   localops={o['fixture_id']:o for o in chair_ops if o.get('unit')==uid};chair_obstacles=[]
   if set(localops)!=chairids:wait('PUBLIC_CHAIR_MOTION_INVENTORY:'+uid)
   for fid,op in localops.items():
    if fid not in fixtures:fail('UNKNOWN_DINING_CHAIR',unit=uid,fixture=fid);continue
    closed=q(op['closed_rect']);opened=q(op['open_rect']);delta=tuple(F(str(v))for v in op['translation'])
    if closed!=fixtures[fid]or len(delta)!=2 or (delta[0]!=0 and delta[1]!=0)or sum(abs(v)for v in delta)!=F('.4')or tuple(closed[i]+delta[i%2]for i in range(4))!=opened:fail('CHAIR_SOURCE_RIGID_MOTION',unit=uid,fixture=fid);continue
    sweep=(min(closed[0],opened[0]),min(closed[1],opened[1]),max(closed[2],opened[2]),max(closed[3],opened[3]));chair_obstacles.append(sweep)
    if not covered(sweep,owner):fail('CHAIR_MOTION_OUTSIDE',unit=uid,fixture=fid)
    for wid,w in walls.items():
     if hit(sweep,w):fail('CHAIR_MOTION_WALL',unit=uid,fixture=fid,wall=wid)
    for other,f in fixtures.items():
     if other!=fid and hit(sweep,f):fail('CHAIR_MOTION_FIXTURE',unit=uid,fixture=fid,other=other)
    try:
     occ=q(op['occupied_body']);eg=sweeps(op['egress_route'])
     if occ[2]-occ[0]!=B or occ[3]-occ[1]!=B:fail('CHAIR_BODY_PROFILE',unit=uid,fixture=fid)
     # Other occupied seats remain obstacles; same body's contact with its chair
     # is not generalized to any other furniture or route.
     otherocc=[q(z['occupied_body'])for key,z in localops.items()if key!=fid and 'occupied_body'in z]
     for s in eg:
      if not covered(s,owner)or any(hit(s,x)for x in list(walls.values())+[f for key,f in fixtures.items()if key!=fid]+otherocc):fail('CHAIR_EGRESS_COLLISION',unit=uid,fixture=fid)
    except (KeyError,ValueError):wait('CHAIR_OCCUPIED_EGRESS_WITNESS:'+uid+'.'+fid)
   # Public capacity must be explicit on actual fixture/seat instances; no
   # automatic claim that a table rectangle supplies four real chairs.
   capacity=program.get('capacity')
   if not isinstance(capacity,dict):wait('PUBLIC_CAPACITY_SOURCE_AND_SEAT_INSTANCES:'+uid)
   else:
    for name in ('residents','dining_seats','living_seats','sleeping_places','source_basis'):
     if name not in capacity:wait('PUBLIC_CAPACITY_FIELD:'+uid+'.'+name)
    if all(k in capacity for k in ('residents','dining_seats','living_seats','sleeping_places')):
     residents=F(str(capacity['residents']))
     if residents.denominator!=1 or residents<1:fail('PUBLIC_CAPACITY_INVALID',unit=uid)
     for group in ('dining_seats','living_seats','sleeping_places'):
      seen=set();count=0
      for seat in capacity[group]:
       if seat['id']in seen or seat['fixture_id']not in fixtures:fail('PUBLIC_CAPACITY_INSTANCE',unit=uid,group=group)
       seen.add(seat['id']);count+=int(seat.get('places',0))
       if not seat.get('source_basis'):wait('PUBLIC_SEAT_SOURCE:'+uid+'.'+seat['id'])
      if count<residents:fail('PUBLIC_CAPACITY_SHORTFALL',unit=uid,group=group,actual=count,required=str(residents))
     # Integer claims are not independently sufficient evidence of seating use.
     wait('PUBLIC_CAPACITY_INSTANCE_GEOMETRY_PROOF:'+uid)
   entry=u.get('entry_point') or u.get('entry')
   routes={**u.get('routes',{}),**u.get('scenario_routes',{})}
   destinations=program.get('destinations',{})
   for name in ('guest_living','guest_dining','kitchen_to_dining_floor'):
    path=routes.get(name)
    if path is None:wait('PUBLIC_REQUIRED_ROUTE_MISSING:'+uid+'.'+name);continue
    try:body=sweeps(path)
    except ValueError as e:fail('PUBLIC_ROUTE_INVALID',unit=uid,route=name,detail=str(e));continue
    if name.startswith('guest'):
     if entry is None:wait('PUBLIC_ENTRY_BINDING_MISSING:'+uid)
     elif tuple(map(lambda x:F(str(x)),path[0]))!=tuple(map(lambda x:F(str(x)),entry)):fail('PUBLIC_ROUTE_ENTRY_MISMATCH',unit=uid,route=name)
    dst=destinations.get(name)
    if not isinstance(dst,dict)or dst.get('activity_id')not in acts or dst.get('fixture_id')not in fixtures:wait('PUBLIC_DESTINATION_SOURCE_BINDING:'+uid+'.'+name)
    else:
     end=tuple(F(str(v))for v in path[-1]);a=acts[dst['activity_id']];f=fixtures[dst['fixture_id']]
     if not(a[0]<=end[0]<=a[2]and a[1]<=end[1]<=a[3]):fail('PUBLIC_ROUTE_MISSED_DESTINATION',unit=uid,route=name)
     # Require real adjacent activity, not a free-floating label.
     if dst.get('binding')=='actual_dining_operation_standing_endpoint':
      try:
       bind_operation_destination(u,dst,end)
      except (KeyError,ValueError,TypeError)as e:fail('PUBLIC_OPERATION_DESTINATION_BINDING',unit=uid,route=name,detail=str(e))
     elif not ((a[2]==f[0]or a[0]==f[2])and max(a[1],f[1])<min(a[3],f[3])or(a[3]==f[1]or a[1]==f[3])and max(a[0],f[0])<min(a[2],f[2])):fail('PUBLIC_DESTINATION_NOT_FIXTURE_ADJACENT',unit=uid,route=name)
    obstacles=list(walls.values())+list(fixtures.values())+private+chair_obstacles
    if name.startswith('guest'):obstacles+=kitchen+kmotion
    for s in body:
     if not covered(s,owner):fail('PUBLIC_ROUTE_OUTSIDE_OWNER',unit=uid,route=name)
     if any(hit(s,x)for x in obstacles):fail('PUBLIC_ROUTE_FORBIDDEN_INTERSECTION',unit=uid,route=name)
    rows.append({'unit':uid,'route':name,'body_width':str(B),'segments':len(body),'all_occupied_chair_motion_included':set(localops)==chairids})
 except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError)as e:fail('PUBLIC_PROGRAM_MALFORMED',detail=str(e))
 if any(p.startswith('PUBLIC_CAPACITY_INSTANCE_GEOMETRY_PROOF:')for p in pending):
  from program_capacity_audit118 import examine as capacity_audit
  capacity_evidence=capacity_audit(model)
  errors.extend(capacity_evidence['errors'])
  if not capacity_evidence['errors']and not capacity_evidence['pending']:
   pending=[p for p in pending if not p.startswith('PUBLIC_CAPACITY_INSTANCE_GEOMETRY_PROOF:')]
  else:pending.extend(capacity_evidence['pending'])
 return {'errors':errors,'pending':sorted(set(pending)),'evidence':{'status':'FAIL_SCOPED'if errors else'NOT_EVALUATED'if pending else'PASS_PUBLIC_SCOPED','model_hash':gid,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'routes':rows,'source_lines':{'Blueprint':[286,293,294,295,377,378,382,3988,3989,3990],'PRD':[161]},'accepted':False,'scope':'Public route/chair geometry and declared inventory only; no generic sofa seating/population inference, no area-ratio threshold, no whole-plan acceptance.'}}

def examine_dining_module(module):
 if module.get('schema')=='SIX_PLACE_PLANAR_SOURCE_STUDY_V1':
  from dining6_audit121 import examine as six_audit
  r=six_audit(module)
  return {'errors':r['errors'],'pending':[],'evidence':r}
 """Rigid four-chair/pull envelope audit, never substitutes for seated/rise proof.
Consumes dining_module118 saved geometry; no generator or producer status used.
"""
 errors=[];pending=[];witness=[]
 try:
  W,H=F(str(module['width'])),F(str(module['depth']));floor=[(F(0),F(0),W,H)];fs={k:q(v)for k,v in module['fixtures'].items()};instances=module['seating']['instances'];seen=set();source=json.loads(Path(__file__).with_name('fixture_catalog114.json').read_text())
  if module.get('fixture_catalog_hash')!=digest(source):errors.append({'code':'DINING_SOURCE_CATALOG_BINDING'})
  chairs={k for k in fs if k.startswith('chair_')};count=module['seating']['requested_places']
  if len(instances)!=count or {s['fixture_id']for s in instances}!=chairs or len(chairs)!=count:errors.append({'code':'DINING_SEAT_INVENTORY'})
  tablekey=next((k for k in fs if 'table'in k),None)
  if tablekey is None:errors.append({'code':'DINING_TABLE_MISSING'})
  elif sorted((fs[tablekey][2]-fs[tablekey][0],fs[tablekey][3]-fs[tablekey][1]))!=[F('.8'),F('1.2')]:errors.append({'code':'DINING_TABLE_SOURCE_SIZE'})
  for s in instances:
   fid=s['fixture_id'];closed=q(s['closed_rect']);opened=q(s['pulled_rect']);de=tuple(F(str(v))for v in s['translation'])
   if s['id']in seen:errors.append({'code':'DINING_DUPLICATE_SEAT_ID'})
   seen.add(s['id'])
   if fid not in fs or fs[fid]!=closed or(closed[2]-closed[0],closed[3]-closed[1])!=(F('.5'),F('.5')):errors.append({'code':'DINING_CHAIR_SOURCE_BINDING','seat':s['id']})
   if len(de)!=2 or sum(abs(v)for v in de)!=F('.4')or de[0]*de[1]!=0 or tuple(closed[i]+de[i%2]for i in range(4))!=opened:errors.append({'code':'DINING_PULL_RIGIDITY','seat':s['id']})
   sweep=(min(closed[0],opened[0]),min(closed[1],opened[1]),max(closed[2],opened[2]),max(closed[3],opened[3]))
   if not covered(sweep,floor):errors.append({'code':'DINING_PULL_OUTSIDE','seat':s['id']})
   if any(hit(sweep,r)for k,r in fs.items()if k!=fid):errors.append({'code':'DINING_PULL_FIXTURE_COLLISION','seat':s['id']})
   if s.get('occupied_body')is None or s.get('rise_transfer')is None:pending.append('DINING_OCCUPIED_BODY_AND_RISE_MISSING:'+s['id'])
   else:
    # Real occupied-body/transition model is not yet source-qualified. Keep this
    # distinct from the already checkable chair translation; never self-certify.
    pending.append('DINING_OCCUPIED_BODY_RISE_PROFILE_AND_CONTINUOUS_CHECK_REQUIRED:'+s['id'])
   witness.append({'seat':s['id'],'fixture_id':fid,'actual_pull_sweep':[str(v)for v in sweep]})
  pending.extend(['DINING_GUEST_DESTINATION_ROUTE_REQUIRED','DINING_SERVING_ROUTE_REQUIRED'])
 except (KeyError,ValueError,TypeError,IndexError)as e:errors.append({'code':'DINING_MODULE_MALFORMED','detail':str(e)})
 return {'errors':errors,'pending':sorted(set(pending)),'evidence':{'model_hash':digest(module),'status':'FAIL_SCOPED'if errors else'NOT_EVALUATED','actual_distinct_chairs':len(locals().get('chairs',[])),'chair_pull_witness':witness,'scope':'Source .5×.5 chairs and .8×1.2 table; .4 pull study only, not complete four-person occupancy/rise/use proof','accepted':False}}


def bind_operation_destination(unit,dst,end):
 """Prove a standing station from a real rigid placed dining module, not adjacency fiction."""
 from dining_motion_audit118 import examine as motion_audit
 p=unit['dining_module_placement'];m=p['module']
 if digest(m)!=p['module_hash']:raise ValueError('MODULE_HASH')
 report=motion_audit(m)
 if report['errors']:raise ValueError('MODULE_CONTINUOUS_GEOMETRY')
 matrix=[[F(str(v))for v in row]for row in p['transform']['matrix']];t=tuple(F(str(v))for v in p['transform']['translation'])
 if len(matrix)!=2 or any(len(row)!=2 for row in matrix)or any(sum(abs(v)for v in row)!=1 for row in matrix)or any(sum(abs(matrix[i][j])for i in range(2))!=1 for j in range(2)):raise ValueError('NONRIGID_TRANSFORM')
 def rect(r):
  r=q(r);pts=[(matrix[0][0]*x+matrix[0][1]*y+t[0],matrix[1][0]*x+matrix[1][1]*y+t[1])for x in(r[0],r[2])for y in(r[1],r[3])]
  return(min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts))
 if len(set(p['id_map'].values()))!=len(m['fixtures']):raise ValueError('ID_MAP_NOT_INJECTIVE')
 for key,r in m['fixtures'].items():
  if rect(r)!=q(unit['fixtures'][p['id_map'][key]]):raise ValueError('ACTUAL_FIXTURE_NOT_SOURCE_RIGID')
 seat=next((s for s in m['seating']['instances']if p['id_map'][s['fixture_id']]==dst['fixture_id']),None)
 if seat is None:raise ValueError('SEAT_NOT_FOUND')
 standing=rect(seat['rise_transfer']['standing_body'])
 if q(unit['activities'][dst['activity_id']])!=standing:raise ValueError('ACTUAL_ACTIVITY_NOT_STANDING_BODY')
 if tuple(end)!=((standing[0]+standing[2])/2,(standing[1]+standing[3])/2):raise ValueError('ENDPOINT_NOT_STANDING_CENTER')
 return {'module_hash':p['module_hash'],'seat_id':seat['id'],'scope':'Actual post-pull standing station; vertical seated transfer still not proven'}
