"""Independent common-to-bath non-private witness. No producer PASS accepted."""
from fractions import Fraction as F
from checker114 import rect,sweeps,intersects,covered,digest

def bath_nonprivate_access(m):
 errors=[];pending=[];rows=[]
 for u in m['units']:
  uid=u['id'];private=[];bath=u['rooms'].get('bath',[])
  for key,parts in u['rooms'].items():
   meta=m.get('room_metadata',{}).get(uid+'.'+key,{})
   if key.startswith('bed')or key=='private_corridor'or meta.get('private'):
    private.extend(rect(q)for q in parts)
  origins={tuple(map(F,path[-1]))for name,path in m.get('common_routes',{}).items()if name.endswith('_'+uid)and path}
  if not bath:errors.append({'unit':uid,'code':'NO_NON_ENSUITE_BATH'});continue
  if not origins:pending.append(uid+':NO_CHECKABLE_COMMON_ACCESS_ENDPOINT');continue
  # These source-required wet activities must all have physical witnesses, not
  # merely a graph node named bathroom. Whole common and body-route gates remain.
  for activity in ('WC_front','shower_use','basin_front'):
   path=u.get('routes',{}).get(activity);target=u.get('route_targets',{}).get(activity)
   if not path or target is None:pending.append(uid+':BATH_ACTIVITY_PATH_MISSING:'+activity);continue
   if tuple(map(F,path[0]))not in origins:errors.append({'unit':uid,'activity':activity,'code':'BATH_PATH_NOT_FROM_COMMON_ACCESS_ENDPOINT'})
   if tuple(map(F,path[-1]))!=tuple(map(F,target)):errors.append({'unit':uid,'activity':activity,'code':'BATH_TARGET_BINDING'})
   targetbody=(F(target[0])-F('.35'),F(target[1])-F('.35'),F(target[0])+F('.35'),F(target[1])+F('.35'))
   if not covered(targetbody,[rect(q)for q in bath]):errors.append({'unit':uid,'activity':activity,'code':'BATH_TARGET_NOT_ON_ACTUAL_BATH_FLOOR'})
   hits=[]
   try:path_sweeps=sweeps(path)
   except (ValueError,TypeError):errors.append({'unit':uid,'activity':activity,'code':'BATH_PATH_INVALID'});continue
   for q in path_sweeps:
    if any(intersects(q,p)for p in private):hits.append(list(map(str,q)))
   if hits:errors.append({'unit':uid,'activity':activity,'code':'BATH_PATH_REQUIRES_PRIVATE_FLOOR','sweeps':hits})
   rows.append({'unit':uid,'activity':activity,'deleted_private_regions':len(private),'path_points':path,'source_common_endpoints':[list(map(str,x))for x in sorted(origins)],'private_intersections':len(hits)})
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_LIMITED','witness':{'model_hash':digest(m),'rows':rows,'errors':errors,'pending':pending},'scope':'Every required bath-use target reached from actual common-route endpoint without swept-body intersection with any bedroom or declared private intermediate floor. Common-route, full obstacle and wet operation gates separately mandatory.'}
