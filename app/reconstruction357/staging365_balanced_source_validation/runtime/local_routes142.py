"""Route-only diagnostic. Exact orthogonal arrangement, no solver/full gate."""
from fractions import Fraction as F
import heapq
from shared_geometry137 import local_polyline_clear,rect

def search(start,target,body,group,obstacles):
 s=F(body);h=s/2;g=rect(group);start=tuple(map(F,start));target=tuple(map(F,target))
 if s<=0:raise ValueError('POSITIVE_BODY_REQUIRED')
 bounds=(g[0]+h,g[1]+h,g[2]-h,g[3]-h)
 obs=[rect(q)for q in obstacles]
 expanded=[(a-h,b-h,c+h,d+h)for a,b,c,d in obs]
 def blocked(p):
  x,y=p
  return not(bounds[0]<=x<=bounds[2]and bounds[1]<=y<=bounds[3])or any(a<x<c and b<y<d for a,b,c,d in expanded)
 for name,p in [('START',start),('TARGET',target)]:
  if blocked(p):return {'status':name+'_BODY_BLOCKED','path':None}
 xs={bounds[0],bounds[2],start[0],target[0]};ys={bounds[1],bounds[3],start[1],target[1]}
 for a,b,c,d in expanded:
  xs.update(v for v in (a,c)if bounds[0]<=v<=bounds[2]);ys.update(v for v in (b,d)if bounds[1]<=v<=bounds[3])
 xs=sorted(xs);ys=sorted(ys);src=(xs.index(start[0]),ys.index(start[1]));dst=(xs.index(target[0]),ys.index(target[1]))
 def point(n):return(xs[n[0]],ys[n[1]])
 def clear(p,q):
  x,y=p;u,v=q
  if y==v:return not any(b<y<d and max(min(x,u),a)<min(max(x,u),c)for a,b,c,d in expanded)
  return not any(a<x<c and max(min(y,v),b)<min(max(y,v),d)for a,b,c,d in expanded)
 queue=[(F(0),src)];dist={src:F(0)};prev={};visited=0
 while queue:
  cost,n=heapq.heappop(queue)
  if cost!=dist[n]:continue
  visited+=1
  if n==dst:
   nodes=[n]
   while n!=src:n=prev[n];nodes.append(n)
   path=[point(k)for k in reversed(nodes)];out=[]
   for p in path:
    while len(out)>1 and((out[-2][0]==out[-1][0]==p[0])or(out[-2][1]==out[-1][1]==p[1])):out.pop()
    out.append(p)
   if not local_polyline_clear(out,s,g,obs):raise AssertionError('INDEPENDENT_SWEEP_REJECTED')
   return {'status':'EXACT_LOCAL_ROUTE_FOUND','path':out,'length':cost,'visited':visited,'grid_nodes':len(xs)*len(ys)}
  i,j=n;p=point(n)
  for k in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
   if not(0<=k[0]<len(xs)and 0<=k[1]<len(ys)):continue
   q=point(k)
   if blocked(q)or not clear(p,q):continue
   candidate=cost+abs(p[0]-q[0])+abs(p[1]-q[1])
   if k not in dist or candidate<dist[k]:dist[k]=candidate;prev[k]=n;heapq.heappush(queue,(candidate,k))
 return {'status':'DISCONNECTED_IN_THIS_FIXED_LOCAL_SCENARIO','path':None,'visited':visited,'grid_nodes':len(xs)*len(ys)}
