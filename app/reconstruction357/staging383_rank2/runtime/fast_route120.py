"""Exact same bounded Dijkstra routing, with per-call symmetric edge memoization.
No model cache, changed grid, relaxed collision, altered body or changed budget.
"""
from fractions import Fraction as F
from functools import lru_cache
import heapq,math
from contract114 import S
D=lambda x:F(str(x))
def Q(r):return tuple(map(D,r))
def route(start,end,floor,obstacles,body='.7',max_nodes=18000):
 start,end=Q(start),Q(end);floor=Q(floor);half=D(body)/2;obs=list(map(Q,obstacles))
 # Exact integer lifting, not float rounding. Speeds repeated body-clearance queries.
 den=math.lcm(*(v.denominator for r in [start,end,floor,*obs,(half,)] for v in r))
 start=tuple(int(v*den)for v in start);end=tuple(int(v*den)for v in end);floor=tuple(int(v*den)for v in floor);obs=[tuple(int(v*den)for v in r)for r in obs];half=int(half*den)
 inflated=[(r[0]-half,r[1]-half,r[2]+half,r[3]+half)for r in obs]
 xs=sorted({start[0],end[0],floor[0]+half,floor[2]-half}|{x for r in inflated for x in(r[0],r[2])if floor[0]+half<=x<=floor[2]-half})
 ys=sorted({start[1],end[1],floor[1]+half,floor[3]-half}|{y for r in inflated for y in(r[1],r[3])if floor[1]+half<=y<=floor[3]-half})
 if len(xs)*len(ys)>max_nodes:return None,'ROUTE_NODE_BUDGET'
 @lru_cache(maxsize=None)
 def valid(p):return floor[0]+half<=p[0]<=floor[2]-half and floor[1]+half<=p[1]<=floor[3]-half and not any(r[0]<p[0]<r[2]and r[1]<p[1]<r[3]for r in inflated)
 if not valid(start)or not valid(end):return None,'ROUTE_ENDPOINT_BLOCKED'
 ix={x:i for i,x in enumerate(xs)};iy={y:i for i,y in enumerate(ys)};a=(ix[start[0]],iy[start[1]]);b=(ix[end[0]],iy[end[1]])
 edge_obstacles=[o for o in obs if o[0]<o[2] and o[1]<o[3]]
 @lru_cache(maxsize=None)
 def cached_edge(p,q):
  # Same positive-area intersection as hit(), after excluding degenerate obs.
  x=min(p[0],q[0])-half;y=min(p[1],q[1])-half
  X=max(p[0],q[0])+half;Y=max(p[1],q[1])+half
  return not any(x<o[2] and o[0]<X and y<o[3] and o[1]<Y for o in edge_obstacles)
 def edge(p,q):return cached_edge(p,q)if p<=q else cached_edge(q,p)
 heap=[(0,a)];dist={a:0};prev={}
 while heap:
  dd,k=heapq.heappop(heap)
  if dd!=dist[k]:continue
  if k==b:
   out=[k]
   while out[-1]!=a:out.append(prev[out[-1]])
   points=[(xs[i],ys[j])for i,j in out[::-1]];compact=[]
   for point in points:
    if len(compact)>1 and ((compact[-2][0]==compact[-1][0]==point[0])or(compact[-2][1]==compact[-1][1]==point[1])):compact[-1]=point
    else:compact.append(point)
   return [[S(F(x,den)),S(F(y,den))]for x,y in compact],None
  i,j=k;p=(xs[i],ys[j])
  for ni,nj in((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
   if not 0<=ni<len(xs)or not 0<=nj<len(ys):continue
   q=(xs[ni],ys[nj]);nk=(ni,nj)
   if not valid(q)or not edge(p,q):continue
   cost=dd+abs(p[0]-q[0])+abs(p[1]-q[1])
   if nk not in dist or cost<dist[nk]:dist[nk]=cost;prev[nk]=k;heapq.heappush(heap,(cost,nk))
 return None,'NO_CONNECTED_BODY_ROUTE'
