"""Independent exact geometric preflight only, not capacity/operation acceptance."""
import json
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
P=Path(__file__).resolve().parent
Q=lambda r:tuple(F(str(v))for v in r)
def overlap(a,b):return max(a[0],b[0])<min(a[2],b[2])and max(a[1],b[1])<min(a[3],b[3])
def check(m):
 errors=[];W,H=F(m['width']),F(m['depth']);fs={k:Q(v)for k,v in m['fixtures'].items()}
 for k,q in fs.items():
  expected=(F('.8'),F('1.2'))if k=='table'else(F('.5'),F('.5'))
  if(q[2]-q[0],q[3]-q[1])!=expected:errors.append('SIZE:'+k)
  if not 0<=q[0]<q[2]<=W or not 0<=q[1]<q[3]<=H:errors.append('BOUNDS:'+k)
 for(a,q),(b,r)in combinations(fs.items(),2):
  if overlap(q,r):errors.append('STATIC_COLLISION:'+a+':'+b)
 for s in m['seating']['instances']:
  q=Q(s['closed_rect']);r=Q(s['pulled_rect']);d=list(map(F,s['translation']));sweep=(min(q[0],r[0]),min(q[1],r[1]),max(q[2],r[2]),max(q[3],r[3]))
  if tuple(v+d[i%2]for i,v in enumerate(q))!=r:errors.append('MOTION:'+s['id'])
  if not 0<=sweep[0]<sweep[2]<=W or not 0<=sweep[1]<sweep[3]<=H:errors.append('SWEEP_BOUNDS:'+s['id'])
  for k,p in fs.items():
   if k!=s['fixture_id']and overlap(sweep,p):errors.append('PULL_STATIC_COLLISION:'+s['id']+':'+k)
 return {'errors':errors,'capacity_accepted':False,'scope':'Rigid chair translation against table/other chair solids only; occupied bodies, rising and access remain unproven.'}
r=[]
for f in [P/'evidence'/name for name in ('dining118_3.1x3.5.json','dining118_3.6x4.2.json','dining118_3.115x3.505.json')]:
 m=json.loads(f.read_text());r.append({'file':f.name,**check(m)})
(P/'evidence/dining118_geometry_preflight.json').write_text(json.dumps(r,indent=2));print(r)
