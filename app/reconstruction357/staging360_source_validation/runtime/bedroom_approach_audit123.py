"""Typed source-bound bedroom approach; conservative separation construction.
Not a universal owner rule of simultaneous operation. No producer imports.
"""
from fractions import Fraction as F
from core_wall_audit118 import q,hit,covered
from dining_motion_audit118 import motion,examine_whole,digest

def examine(model,u,role,opening_id=None):
 uid=u['id'];errors=[];logical=model.get('logical_regions',{}).get(role,{})
 def fail(s):errors.append(s)
 if role!=uid+'.bedroom_public_access' or logical.get('unit')!=uid or logical.get('kind')!='BEDROOM_PUBLIC_APPROACH123' or logical.get('source_roles')!=['living','entry_circulation','dining'] or 'parts'in logical:fail('BEDROOM_TYPED_ROLE_CONTRACT')
 floor=[q(r)for name in ('living','entry_circulation','dining')for r in u['rooms'].get(name,[])]
 if any(not u['rooms'].get(k)for k in ('living','entry_circulation','dining')):fail('BEDROOM_PUBLIC_FLOOR_MISSING')
 recs=[p for p in model.get('module_placements',[])if p.get('unit_id')==uid and p.get('id_map',{}).get('M.public_access')==role]
 allowed={};rows=[]
 for p in recs:
  s=p['module'];room=p['room_id'];ids=p['id_map']
  if s.get('schema')not in ('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118')or not room.startswith('bed'):fail('BEDROOM_SOURCE_SCHEMA');continue
  if digest(s)!=p.get('module_hash'):fail('BEDROOM_MODULE_HASH')
  for o in s['openings']:
   if 'M.public_access'not in o['connects']:continue
   oid=ids[o['id']];allowed[oid]=room
   actual=[v for v in model['openings']if v['id']==oid]
   if len(actual)!=1 or set(actual[0]['connects'])!={role,uid+'.'+room}:fail('BEDROOM_SOURCE_OPENING_MAP')
 if not allowed or (opening_id is not None and opening_id not in allowed):fail('BEDROOM_TYPED_OTHER_OPENING')
 for o in model['openings']:
  if role in o['connects']and o['id']not in allowed:fail('BEDROOM_ROLE_USED_BY_NONBEDROOM')
 # Fresh independent whole dining source/isometry/actual-operation binding.
 dining=examine_whole(model)
 if dining['errors']or dining['pending']:fail('BEDROOM_DINING_WITNESS_NOT_BOUND')
 p=u['dining_module_placement'];s=p['module'];mat=[[F(str(v))for v in row]for row in p['transform']['matrix']];t=list(map(F,p['transform']['translation']))
 def tr(r):
  x,y,X,Y=q(r);pts=[(mat[0][0]*a+mat[0][1]*b+t[0],mat[1][0]*a+mat[1][1]*b+t[1])for a in(x,X)for b in(y,Y)]
  return(min(a for a,b in pts),min(b for a,b in pts),max(a for a,b in pts),max(b for a,b in pts))
 obstacles={k:q(r)for k,r in model['walls'].items()};obstacles.update({v['id']+'.'+k:q(r)for v in model['units']for k,r in v['fixtures'].items()})
 for seat in s['seating']['instances']:
  key='dining:'+seat['id'];obstacles[key+':occupied']=tr(seat['occupied_body']);obstacles[key+':pull']=motion(tr(seat['closed_rect']),tr(seat['pulled_rect']))
  for i,seg in enumerate(seat['rise_transfer']['segments']):obstacles[key+':actor:'+str(i)]=motion(tr(seg['actor_start']),tr(seg['actor_end']))
 for oid,room in allowed.items():
  shapes=[('apron',q(r))for r in model.get('module_aprons',{}).get(uid+'.'+room,[])]
  if not shapes:fail('BEDROOM_ACTUAL_APRON_MISSING')
  ports=[z for z in model.get('module_ports',[])if z.get('opening_id')==oid]
  if not ports:fail('BEDROOM_ACTUAL_PORT_MISSING')
  for z in ports:
   if z.get('role_id')!=role:fail('BEDROOM_PORT_ROLE')
   x,y=map(F,z['center']);shapes.append(('port',(x-F('.35'),y-F('.35'),x+F('.35'),y+F('.35'))))
  ds=[d for d in model['operations']['doors']if d['opening_id']==oid]
  if len(ds)!=1:fail('BEDROOM_DOOR_WITNESS_MISSING');continue
  segs=[z for z in ds[0]['continuous_actor_segments']if z['side']=='outside']
  if not segs:fail('BEDROOM_OUTSIDE_ACTOR_MISSING')
  for seg in segs:
   if seg['role_id']!=role or seg['unit']!=uid:fail('BEDROOM_ACTOR_ROLE')
   shapes.append(('door_actor',motion(seg['actor_start'],seg['actor_end'])))
  for kind,r in shapes:
   if not covered(r,floor):fail('BEDROOM_APPROACH_OUTSIDE_TYPED_FLOOR:'+kind)
   for name,ob in obstacles.items():
    if hit(r,ob):fail('BEDROOM_CONSERVATIVE_RESERVATION_COLLISION:'+kind+':'+name)
  rows.append({'opening':oid,'actual_shapes_checked':len(shapes)})
 return {'errors':sorted(set(errors)),'parts':floor,'rows':rows,'scope':'Conservative source-bound construction separates bedroom approach/actor from actual dining occupied/pull/actor trajectories. This method rejects overlap, not a universal simultaneity rule; whole module/isometry/privacy checks remain mandatory.'}
