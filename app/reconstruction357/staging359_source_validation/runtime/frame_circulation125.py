"""Source-bound125 common grammar only; not whole-plan/quality admission.
Q04/IR-P10 functional circulation remains enforced by circulation_integrity119.
No producer import; current geometry and source frame are examined afresh.
"""
from fractions import Fraction as F
from frame_audit125 import evaluate_core,digest,equal,rectangle


def rect(r):
 r=tuple(F(str(x)) for x in r)
 if len(r)!=4 or r[0]>=r[2] or r[1]>=r[3]:raise ValueError('NONPOSITIVE_RECT')
 return r

def subtract(r,c):
 x,y,X,Y=r;a,b,A,B=c;a=max(a,x);b=max(b,y);A=min(A,X);B=min(B,Y)
 if a>=A or b>=B:return [r]
 return [z for z in ((x,y,a,Y),(A,y,X,Y),(a,y,A,b),(a,B,A,Y)) if z[0]<z[2] and z[1]<z[3]]

def residual(a,b):
 rs=[rect(r) for r in a]
 for c in b:rs=[s for r in rs for s in subtract(r,rect(c))]
 return rs

def same_union(a,b):return not residual(a,b) and not residual(b,a)

def examine(model,core=None,local=None):
 errors=[];pending=[];w={}
 if core is None:return {'status':'NOT_EVALUATED','errors':[],'pending':['FRAME125_ACTUAL_CORE_CONTEXT_REQUIRED'],'witness':w}
 try:
  if core['kind']!='LOCAL_FRAME_OF_LEFT_RIGHT_COMMON_CORE125':raise ValueError('CORE_KIND')
  a=evaluate_core(core);w['fresh_frame_audit']=a
  errors.extend('FRAME:'+s for s in a['errors'])
  src=core['physical_core_model'];fb=model['frame_binding125']
  if fb['schema']!='ACTUAL_LOCAL_TO_WORLD_D4_V1' or fb['core_contract_hash']!=digest(core) or not equal(fb['world_from_local'],core['world_from_local']):errors.append('CORE_FRAME_HASH_BINDING')
  if not equal(model['inputs'],src['inputs']):errors.append('WORLD_INPUT_BINDING')
  if not equal(model['profile']['body_m'],src['body_m']):errors.append('BODY_PROFILE_BINDING')
  mapped=set();supported={'PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118','BATHROOM_MODULE117','KITCHEN_MODULE117'}
  for p in model['module_placements']:
   mod=p['module'];T=p['transform'];matrix=T['matrix']
   if mod['schema'] not in supported:pending.append('UNSUPPORTED_CIRCULATION_MODULE_GRAMMAR')
   if digest(mod)!=p['module_hash']:errors.append('MODULE_SOURCE_HASH')
   if len(matrix)!=2 or any(len(row)!=2 for row in matrix) or any(F(str(x)) not in (-1,0,1)for row in matrix for x in row) or any(sum(F(str(matrix[k][i]))*F(str(matrix[k][j]))for k in range(2))!=int(i==j)for i in range(2)for j in range(2)):raise ValueError('MODULE_NOT_D4')
   for k,r in mod['walls'].items():
    target=p['id_map'][k]
    if target in mapped:errors.append('DUPLICATE_MODULE_WALL_OWNER:'+target)
    mapped.add(target)
    if not equal(rectangle(r,T),model['walls'][target]):errors.append('MODULE_WALL_GEOMETRY:'+target)
  if model.get('private_domains'):
   from private_hall_binding129 import examine as hall_binding
   h=hall_binding(model,local,core);w['actual_private_hall_source']=h
   errors.extend(h['errors']);pending.extend(h['pending'])
   if not h['errors'] and not h['pending']:mapped.update(h['boundary_wall_ids'])
  actual=[r for k,r in model['walls'].items() if k not in mapped]
  if not same_union(actual,list(src['walls'].values())):errors.append('NONMODULE_WALL_SOURCE_UNION')
  w['nonmodule_wall_count']=len(actual);w['source_wall_count']=len(src['walls'])
  for name in ('stair','lift'):
   if not equal(model['common_spaces'][name],src[name]):errors.append('COMMON_CORE_GEOMETRY:'+name)
  if not same_union(model['common_spaces']['lobby'],src['common_floor']):errors.append('COMMON_FLOOR_SOURCE_UNION')
  units={u['id']:u for u in model['units']}
  if len(units)!=len(model['units']) or set(units)!=set(src['units']):errors.append('UNIT_INVENTORY')
  for uid,rs in src['units'].items():
   if not same_union(units[uid]['ownership'],rs):errors.append('OWNERSHIP_SOURCE:'+uid)
  from core_partition_audit125 import audit as audit_partition
  actual_component=dict(src, routes=model['common_routes'])
  current_routes=audit_partition(actual_component)
  errors.extend('ACTUAL_COMMON_ROUTE:'+e for e in current_routes['errors'])
  w['actual_common_route_audit']=current_routes
  portals={o['id']:o for o in model['openings']}
  if len(portals)!=len(model['openings']):errors.append('DUPLICATE_PORTAL_ID')
  # Source common_core125 uses unit ownership endpoints A/B. The actual
  # assemble114 interface resolves them ONLY to the same unit's public access
  # (living + analytical entry floor), never to a bathroom/private room.
  role_map={'A':'A.public_access','B':'B.public_access','lobby':'lobby','stair':'stair','lift':'lift'}
  source_pairs={'A.entry':{'A','lobby'},'B.entry':{'B','lobby'},'stair.entry':{'stair','lobby'},'lift.entry':{'lift','lobby'}}
  host_ids={'A.entry':'A.unit_boundary','B.entry':'B.unit_boundary','stair.entry':'core.stair.right','lift.entry':'core.lift.left'}
  if len(src['openings'])!=4 or {o['id']for o in src['openings']}!=set(source_pairs):errors.append('SOURCE_COMMON_PORTAL_INVENTORY')
  for uid in ('A','B'):
   logical=model['logical_regions'].get(uid+'.public_access')
   if logical!={'unit':uid,'source_roles':['living','entry_circulation']}:errors.append('COMMON_ENTRY_PUBLIC_ROLE_BINDING:'+uid)
  for o in src['openings']:
   z=portals[o['id']]
   expected=source_pairs[o['id']]
   if len(o['connects'])!=2 or set(o['connects'])!=expected:errors.append('SOURCE_COMMON_PORTAL_ROLES:'+o['id'])
   if len(z.get('connects',[]))!=2 or set(z['connects'])!={role_map[v]for v in expected}:errors.append('COMMON_PORTAL_ENDPOINT_ROLES:'+o['id'])
   if z['host_wall_id']!=host_ids[o['id']]:errors.append('COMMON_PORTAL_HOST_ROLE:'+o['id'])
   if not equal(z['rect'],o['rect']):errors.append('COMMON_PORTAL_GEOMETRY:'+o['id'])
   # Host IDs differ by frame grammar; bind actual host geometry, not the label.
   host=rect(model['wall_hosts'][z['host_wall_id']]); sh=rect(src['wall_hosts'][o['host']])
   # World host may include physically present corner overlaps, not arbitrary material.
   material=list(src['walls'].values())+[v['rect']for v in src['openings']]
   if residual([sh],[host]) or residual([host],material):errors.append('COMMON_PORTAL_HOST:'+o['id'])
   axis=0 if sh[2]-sh[0]<sh[3]-sh[1] else 1
   if (host[axis],host[axis+2])!=(sh[axis],sh[axis+2]):errors.append('COMMON_PORTAL_HOST_THICKNESS:'+o['id'])
  # Preserve private/room grammar rather than waiving it with the common frame.
  binding=None
  if model.get('private_domains'):
   from private_binding121 import examine as private
   binding=private(model);errors.extend(binding['errors']);pending.extend(binding['pending'])
  for uid,u in units.items():
   beds={k for k in u['rooms'] if k.startswith('bed')}
   extra={'private_circulation'} if len(beds)==3 and binding is not None else set()
   if beds not in ({'bed1'},{'bed1','bed2'},{'bed1','bed2','bed3'}) or set(u['rooms'])!=beds|{'bath','kitchen','dining','living','entry_circulation'}|extra:pending.append(uid+':UNSUPPORTED_OR_RENAMED_ROOM_CIRCULATION_GRAMMAR')
   if len(beds)==1:
    ps=[p for p in model['module_placements'] if p['module']['schema']in {'PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118'} and any(v.startswith(uid+'.bed1.')for v in p['id_map'].values())]
    if len(ps)!=1:pending.append(uid+':SINGLE_BEDROOM_SOURCE_PLACEMENT_MISSING')
   elif len(beds)==2:
    from paired_private_zone118 import examine as paired
    zones=paired(model)['zones']
    if not any(z['unit']==uid and z['status']=='PASS_TWO_BEDROOM_PRIVATE_APPROACH_TOPOLOGY' and set(z['bedrooms'])=={uid+'.bed1',uid+'.bed2'}for z in zones):pending.append(uid+':NO_INDEPENDENT_REAL_PAIRED_PRIVATE_ZONE')
   elif binding is None or binding['errors'] or binding['pending']:pending.append(uid+':PRIVATE_DOMAIN_NOT_BOUND')
 except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError) as ex:errors.append('FRAME125_GRAMMAR_SCHEMA:'+str(ex))
 return {'status':'FAIL' if errors else 'NOT_EVALUATED' if pending else 'PASS_COMMON_SOURCE_GRAMMAR_ONLY','errors':sorted(set(errors)),'pending':sorted(set(pending)),'witness':w,'whole_model_evaluated':False,'accepted':False,'scope':'Only source grammar/common binding. All actual unit access, source operations, body routes, privacy and functional floor accounting remain separate mandatory fresh checks.'}

def grammar(model,core=None,local=None):
 r=examine(model,core,local)
 return r['errors']+r['pending']
