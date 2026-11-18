"""Exact descriptive distances over stored orthogonal route union, not eligibility."""
from fractions import Fraction as F
import heapq
from common import rows,digest

def point(p):
 if type(p)is not list or len(p)!=2 or any(type(x)not in(int,str)for x in p):raise ValueError('EXACT_POINT')
 return tuple(map(F,p))
def graph(paths):
 segs=[];points=set()
 for path in paths:
  if type(path)is not list or len(path)<2:raise ValueError('PATH_INVENTORY')
  ps=list(map(point,path));points.update(ps)
  for a,b in zip(ps,ps[1:]):
   if a==b:continue
   if a[0]!=b[0]and a[1]!=b[1]:raise ValueError('ORTHOGONAL_REQUIRED')
   segs.append((a,b))
 def on(p,a,b):return min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])
 for a,b in segs:
  for c,d in segs:
   if a[0]==b[0]and c[1]==d[1]:
    p=(a[0],c[1])
    if on(p,a,b)and on(p,c,d):points.add(p)
 g={p:{}for p in points}
 for a,b in segs:
  ps=sorted(p for p in points if on(p,a,b))
  for p,q in zip(ps,ps[1:]):g[p][q]=g[q][p]=abs(p[0]-q[0])+abs(p[1]-q[1])
 return g

def distance(g,start,end):
 if start not in g or end not in g:return None
 d={start:F(0)};todo=[(F(0),start)]
 while todo:
  cost,p=heapq.heappop(todo)
  if p==end:return cost
  if d[p]!=cost:continue
  for q,w in g[p].items():
   n=cost+w
   if q not in d or n<d[q]:d[q]=n;heapq.heappush(todo,(n,q))
 return None

def evaluate(model,raw):
 rows(model,raw);out=[]
 for u in model['units']:
  routes=u['routes'];g=graph(list(routes.values()));roots={point(p[0])for p in routes.values()}
  if len(roots)!=1:raise ValueError('SOURCE_COMMON_ROOT_REQUIRED')
  beds={k:point(v[-1])for k,v in routes.items()if k.startswith('bed')and k.endswith(('bed_front','bedA_front','bedB_front'))}
  if not beds:raise ValueError('BED_TARGET_INVENTORY')
  required=['WC_front','shower_use','basin_front']+u['spatial_role_bindings']['living_activity_group']['access_route_ids']
  targets={'entry':next(iter(roots)),**{k:point(routes[k][-1])for k in required}}
  pairs=[]
  for b,p in beds.items():
   for t,q in targets.items():
    v=distance(g,p,q);pairs.append({'bed_target':b,'destination':t,'stored_network_length_m':None if v is None else str(v)})
  out.append({'unit':u['id'],'pairs':pairs,'bed_targets':sorted(beds)})
 return {'model_hash':digest(model),'raw_hash':digest(raw),'units':out,'scope':'DESCRIPTIVE_STORED_ROUTE_UNION_ONLY; no new path feasibility, no private-crossing admission, no comparison eligibility','parent_complete':False}
