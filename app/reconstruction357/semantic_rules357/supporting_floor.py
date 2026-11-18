"""Reconstructed357 exact source-body support study; not recovered353 bytes.
Engineering assumption: connected body-usable supporting floor can supplement a
source-complete activity bundle. This alone never assigns a final functional role.
"""
from fractions import Fraction as F
import time

def analyze(domain,obstacles,anchors,body,seconds=5):
 start=time.monotonic();h=F(body)/2
 if h<=0:raise ValueError('BODY')
 D=[tuple(map(F,r))for r in domain];O=[tuple(map(F,r))for r in obstacles]
 if not D or not anchors:raise ValueError('DOMAIN_ANCHOR')
 if any(len(r)!=4 or r[0]>=r[2]or r[1]>=r[3]for r in D+O):raise ValueError('REGION')
 def tick():
  if time.monotonic()-start>seconds:raise ValueError('SUPPORT_DEADLINE')
 def inside(p,rs,strict=False):
  x,y=p;return any((a<x<c and b<y<d)if strict else(a<=x<=c and b<=y<=d)for a,b,c,d in rs)
 box=(min(r[0]for r in D),min(r[1]for r in D),max(r[2]for r in D),max(r[3]for r in D))
 xs=sorted({v for r in D for v in(r[0],r[2])});ys=sorted({v for r in D for v in(r[1],r[3])});outside=[]
 for a,c in zip(xs,xs[1:]):
  tick()
  for b,d in zip(ys,ys[1:]):
   if not inside(((a+c)/2,(b+d)/2),D):outside.append((a,b,c,d))
 forbidden=[(a-h,b-h,c+h,d+h)for a,b,c,d in O+outside];center=(box[0]+h,box[1]+h,box[2]-h,box[3]-h)
 if center[0]>=center[2]or center[1]>=center[3]:return {'verdict':'FAIL_BODY_CANNOT_FIT_DOMAIN','support_regions':[],'parent_complete':False}
 anchors=[tuple(map(F,p))for p in anchors]
 X=sorted({center[0],center[2]}|{x for r in forbidden for x in(r[0],r[2])if center[0]<=x<=center[2]}|{p[0]for p in anchors});Y=sorted({center[1],center[3]}|{y for r in forbidden for y in(r[1],r[3])if center[1]<=y<=center[3]}|{p[1]for p in anchors})
 if len(X)*len(Y)>30000:raise ValueError('SUPPORT_GRID_CAP')
 def valid(p):return inside(p,[center])and not inside(p,forbidden,True)
 allowed=set()
 for i,x in enumerate(X):
  tick()
  for j,y in enumerate(Y):
   if valid((x,y)):allowed.add((i,j))
 starts={(X.index(x),Y.index(y))for x,y in anchors if valid((x,y))}
 if len(starts)!=len(set(anchors)):return {'verdict':'FAIL_SOURCE_ACTIVITY_ANCHOR_NOT_BODY_USABLE','support_regions':[],'parent_complete':False}
 reached=set();stack=[next(iter(starts))]
 while stack:
  tick();p=stack.pop()
  if p in reached:continue
  reached.add(p);i,j=p
  for q in((i-1,j),(i+1,j),(i,j-1),(i,j+1)):
   if q not in allowed or q in reached:continue
   ii,jj=q
   if valid(((X[i]+X[ii])/2,(Y[j]+Y[jj])/2)):stack.append(q)
 cells=[]
 for i in range(len(X)-1):
  tick()
  for j in range(len(Y)-1):
   if (i,j)in reached and valid(((X[i]+X[i+1])/2,(Y[j]+Y[j+1])/2)):cells.append([str(X[i]-h),str(Y[j]-h),str(X[i+1]+h),str(Y[j+1]+h)])
 # Exact-width corridors can have only line/point configuration-space support.
 for i,j in reached:
  cells.append([str(X[i]-h),str(Y[j]-h),str(X[i]+h),str(Y[j]+h)])
  for ii,jj in((i+1,j),(i,j+1)):
   if (ii,jj)in reached and valid(((X[i]+X[ii])/2,(Y[j]+Y[jj])/2)):cells.append([str(min(X[i],X[ii])-h),str(min(Y[j],Y[jj])-h),str(max(X[i],X[ii])+h),str(max(Y[j],Y[jj])+h)])
 for axis in(0,1,0,1):
  grouped={}
  for raw in cells:
   q=tuple(map(F,raw));other=1-axis;grouped.setdefault((q[other],q[other+2]),[]).append((q[axis],q[axis+2]))
  cells=[]
  for (lo,hi),ivs in grouped.items():
   merged=[]
   for a,b in sorted(ivs):
    if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
    else:merged.append((a,b))
   for a,b in merged:cells.append(list(map(str,(a,lo,b,hi)if axis==0 else(lo,a,hi,b))))
 return {'verdict':'PASS_SOURCE_BODY_SUPPORT_COMPONENT_SCOPED'if starts<=reached else'FAIL_SOURCE_ACTIVITIES_DISCONNECTED','support_regions':cells,'anchor_count':len(starts),'connected_anchors':len(starts&reached),'center_grid_nodes':len(X)*len(Y),'reachable_nodes':len(reached),'body_m':str(2*h),'contact_policy':'AXIS_ALIGNED_BODY_BOUNDARY_CONTACT_ALLOWED','parent_complete':False,'not_claimed':['WHOLE_ROLE_ASSIGNMENT','CIRCULATION_NECESSITY','ALL_EMPTY_SPACE_FUNCTION','WHOLE_PLAN_PASS'],'elapsed_seconds':time.monotonic()-start}
