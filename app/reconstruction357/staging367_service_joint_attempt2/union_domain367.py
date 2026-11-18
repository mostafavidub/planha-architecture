"""Pure exact horizontal translation domain; no candidate/receipt/acceptance.
Finite axis-aligned rectangle profiles only. No bounding-box substitute for floor.
"""
from fractions import Fraction as F

def rect(r):
 if type(r) not in (list,tuple) or len(r)!=4:raise ValueError('RECT_REQUIRED')
 if any(type(x) not in(str,int,F) for x in r):raise ValueError('EXACT_COORDINATES')
 a,b,c,d=map(F,r)
 if a>=c or b>=d:raise ValueError('POSITIVE_RECT_REQUIRED')
 return a,b,c,d

def overlap(a,b):return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])
def covered(r,floor):
 xs=sorted({r[0],r[2]}|{x for f in floor for x in(f[0],f[2])if r[0]<x<r[2]})
 for a,c in zip(xs,xs[1:]):
  intervals=sorted((max(r[1],f[1]),min(r[3],f[3]))for f in floor if f[0]<=a and f[2]>=c and max(r[1],f[1])<min(r[3],f[3]))
  top=r[1]
  for lo,hi in intervals:
   if lo>top:return False
   top=max(top,hi)
  if top<r[3]:return False
 return True

def domain(moving,floor,obstacles,lower,upper,max_events=4096):
 """Each moving rect must stay in exact floor union, avoid positive overlaps.
 Bounds are explicit finite candidate translations, NOT feasibility assertions.
 """
 moving=list(map(rect,moving));floor=list(map(rect,floor));obstacles=list(map(rect,obstacles));lo,hi=F(lower),F(upper)
 if not moving or not floor or lo>=hi:raise ValueError('FINITE_NONEMPTY_DOMAIN_REQUIRED')
 if type(max_events)is not int or not 2<=max_events<=4096:raise ValueError('EVENT_CAP')
 if len(moving)+len(floor)+len(obstacles)>4096:raise ValueError('RECT_CAP')
 points={lo,hi}
 for a in moving:
  for b in floor+obstacles:
   for x in(a[0],a[2]):
    for y in(b[0],b[2]):
     if lo<=y-x<=hi:points.add(y-x)
     if len(points)>max_events:raise ValueError('EVENT_CAP_EXCEEDED')
 def feasible(x):
  shifted=[(a+x,b,c+x,d)for a,b,c,d in moving]
  return all(covered(a,floor)and not any(overlap(a,b)for b in obstacles)for a in shifted)
 points=sorted(points)
 return {'schema':'EXACT_TRANSLATION_DOMAIN_NOT_CONSTRUCTION_PROOF','points':[str(x)for x in points if feasible(x)],'open_cells':[[str(a),str(b)]for a,b in zip(points,points[1:])if feasible((a+b)/2)],'critical_event_count':len(points),'accepted':False,'scope':'fixed rectangles, axis aligned translation; zero area contact permitted geometrically, not technical clearance approval'}
