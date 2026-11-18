"""Exact one-dimensional operation-translation domains; no candidate construction."""
import json,sys,hashlib,time
from pathlib import Path
from fractions import Fraction as F
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'semantic_rules357'))
from union_domain367 import rect,overlap,covered
def intersection(a,b):return overlap(a,b)
def difference(parts,floor):return [p for p in parts if not covered(p,floor)]
P=B/'staging365_service_grammar/candidate365.json'
EXPECTED_RECORD_SHA='8807b7f2e8ba841d8e1a38ba6787f72161c9d04f64d69e71112859be92976ad9'
def bound_record():
 data=P.read_bytes()
 if hashlib.sha256(data).hexdigest()!=EXPECTED_RECORD_SHA:raise ValueError('SOURCE_SERVICE_RECORD_CHANGED')
 return json.loads(data)
def search_bounds(actors):
 if not actors:raise ValueError('ACTOR_BOUND_REQUIRED')
 lows=[];highs=[]
 for a,floor in actors:
  if not floor:raise ValueError('FLOOR_REQUIRED')
  lows.append(min(r[0]for r in floor)-a[0]);highs.append(max(r[2]for r in floor)-a[2])
 return max(lows),min(highs)
def domains(model):
 m=model;results={};deadline=time.monotonic()+5
 if type(m)is not dict or type(m.get('units'))is not list or len(m['units'])!=2:raise ValueError('FINITE_TWO_UNIT_MODEL_REQUIRED')
 for uid in ('A','B'):
  original=next(o for o in m['operations']['doors']if o['opening_id']==uid+'.entry');opening=next(o for o in m['openings']if o['id']==uid+'.entry');x0=(F(opening['rect'][0])+F(opening['rect'][2]))/2
  host=rect(m['wall_hosts'][opening['host_wall_id']]);unit=next(u for u in m['units']if u['id']==uid);inside=list(map(rect,unit['rooms']['living']+unit['rooms']['entry_circulation']));outside=list(map(rect,m['common_spaces']['lobby']))
  obs=[(k,rect(r))for k,r in m['walls'].items()]+[(u['id']+'.'+k,rect(r))for u in m['units']for k,r in u['fixtures'].items()]+[(o['opening_id']+'.closed',rect(o['closed_panel']))for o in m['operations']['doors']if o['opening_id']!=uid+'.entry']
  actor_rects=[rect(s['actor_rect'])for s in original['states']if s['unit']=='COMMON'];lobby=list(map(rect,m['common_spaces']['lobby']))
  if not lobby or not actor_rects or not original.get('continuous_actor_segments'):raise ValueError('OPERATION_FLOOR_EVIDENCE_REQUIRED')
  sign=1 if F(original['translation'][0])>0 else -1
  if F(original['translation'][1])!=0 or F(original['translation'][0])==0:raise ValueError('HORIZONTAL_SLIDING_PROFILE_ONLY')
  if len(obs)>4096:raise ValueError('OBSTACLE_CAP_EXCEEDED')
  for direction in(-1,1):
   if time.monotonic()>deadline:raise ValueError('SOURCE_DOMAIN_DEADLINE')
   rev=direction!=sign;r=rect(original['rail_envelope'])
   def relative(r):
    a,b,c,d=r;return (x0-c,b,x0-a,d)if rev else(a-x0,b,c-x0,d)
   rail=relative(r);actors=[]
   for seg in original['continuous_actor_segments']:
    a=rect(seg['actor_start']);b=rect(seg['actor_end'])
    if seg['side']not in('inside','outside')or (a[2]-a[0],a[3]-a[1])!=(b[2]-b[0],b[3]-b[1])or (a[0]!=b[0]and a[1]!=b[1]):raise ValueError('SOURCE_RIGID_AXIS_ACTOR_SEGMENT_REQUIRED')
    actors.append((relative((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))),outside if seg['side']=='outside'else inside))
   # Intersect projection bounds AFTER direction reflection. These are only
   # necessary bounds; exact floor-union predicates remain below.
   boundactors=actors+[(relative(a),outside)for a in actor_rects]
   lo,hi=search_bounds(boundactors)
   if lo>hi:
    results[uid+':'+str(direction)]={'feasible_points':[],'feasible_open_cells':[],'reason':'EMPTY_REFLECTED_ACTOR_DOMAIN'};continue
   shapes=[rail]+[a for a,_ in actors];critical={lo,hi}
   allrects=[r for _,r in obs]+inside+outside+[host]
   for a in shapes:
    for r in allrects:
     for edge in(r[0],r[2]):
      for off in(a[0],a[2]):
       q=edge-off
       if lo<=q<=hi:critical.add(q)
   if len(critical)>4096:raise ValueError('CRITICAL_EVENT_CAP_EXCEEDED')
   def at(q):
    if time.monotonic()>deadline:raise ValueError('SOURCE_DOMAIN_DEADLINE')
    def shift(r):return(r[0]+q,r[1],r[2]+q,r[3])
    rr=shift(rail);errors=[]
    if rr[0]<host[0]or rr[2]>host[2]:errors.append('RAIL_HOST_EXTENT')
    for name,r in obs:
     if intersection(rr,r):errors.append('PANEL:'+name)
    for i,(a,floor)in enumerate(actors):
     a=shift(a)
     if difference([a],floor):errors.append('ACTOR_FLOOR:'+str(i))
     for name,r in obs:
      if intersection(a,r):errors.append('ACTOR:'+name)
    return sorted(set(errors))
   cs=sorted(critical);points=[str(x)for x in cs if not at(x)];cells=[[str(a),str(b)]for a,b in zip(cs,cs[1:])if not at((a+b)/2)]
   results[uid+':'+str(direction)]={'feasible_points':points,'feasible_open_cells':cells,'critical_points':len(cs),'checks':'continuous panel rail and rectangular actor swept envelope vs all walls/fixtures/other closed panels; exact public-floor coverage','baseline_errors':at(x0)}
 return results
