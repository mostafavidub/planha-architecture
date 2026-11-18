"""Exact one-dimensional operation-translation domains; no candidate construction."""
import json,sys,hashlib,time
from pathlib import Path
from fractions import Fraction as F
B=Path(__file__).resolve().parents[1];sys.path.insert(0,str(B/'semantic_rules357'))
from modules_spatial import rect,intersection,difference
P=B/'staging362_core_notch/actual362.json'
def domains(record):
 m=record['candidate']['model'];results={};deadline=time.monotonic()+5
 if type(m)is not dict or type(m.get('units'))is not list or len(m['units'])!=2:raise ValueError('FINITE_TWO_UNIT_MODEL_REQUIRED')
 for uid in ('A','B'):
  original=next(o for o in m['operations']['doors']if o['opening_id']==uid+'.entry');opening=next(o for o in m['openings']if o['id']==uid+'.entry');x0=(F(opening['rect'][0])+F(opening['rect'][2]))/2
  host=rect(m['wall_hosts'][opening['host_wall_id']]);unit=next(u for u in m['units']if u['id']==uid);inside=list(map(rect,unit['rooms']['living']+unit['rooms']['entry_circulation']));outside=list(map(rect,m['common_spaces']['lobby']))
  obs=[(k,rect(r))for k,r in m['walls'].items()]+[(u['id']+'.'+k,rect(r))for u in m['units']for k,r in u['fixtures'].items()]+[(o['opening_id']+'.closed',rect(o['closed_panel']))for o in m['operations']['doors']if o['opening_id']!=uid+'.entry']
  actor_rects=[rect(s['actor_rect'])for s in original['states']if s['unit']=='COMMON'];lobby=list(map(rect,m['common_spaces']['lobby']))
  if len(lobby)!=1:raise ValueError('SINGLE_RECT_LOBBY_PROFILE_ONLY')
  left=min(a[0]for a in actor_rects)-x0;right=max(a[2]for a in actor_rects)-x0;lo=lobby[0][0]-left;hi=lobby[0][2]-right
  if lo>=hi:raise ValueError('EMPTY_ACTOR_DOMAIN')
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
    a=rect(seg['actor_start']);b=rect(seg['actor_end']);actors.append((relative((min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))),outside if seg['side']=='outside'else inside))
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
