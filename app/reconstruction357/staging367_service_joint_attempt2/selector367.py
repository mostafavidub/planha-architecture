"""Finite exact two-entry selection from audited fixed-service operation domains.
Convex cell vertex-average is deterministic interior search, not optimal design.
"""
from fractions import Fraction as F
import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent

def merge(row):
 pts=set(map(F,row['feasible_points']));out=[]
 for a,b in row['feasible_open_cells']:
  a,b=F(a),F(b)
  if out and out[-1][1]==a and a in pts:out[-1]=(out[-1][0],b)
  else:out.append((a,b))
 return out

def clip(poly,a,b,c):
 out=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  fp=a*p[0]+b*p[1]-c;fq=a*q[0]+b*q[1]-c
  if fp<=0:out.append(p)
  if (fp<0 and fq>0)or(fp>0 and fq<0):
   t=fp/(fp-fq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
 return list(dict.fromkeys(out))

def select(record,domain_result):
 if domain_result.get('status')!='COMPLETED_PURE_OPERATION_DOMAIN' or domain_result.get('source_unchanged')is not True:raise ValueError('DOMAIN_NOT_COMPLETE')
 m=record['candidate']['model'];core=record['candidate']['packet']['core'];ops={o['id']:o for o in m['openings']}
 roots={u:F(m['common_routes']['stair_'+u][-1][1])for u in('A','B')};mid=(roots['A']+roots['B'])/2
 def limits(name):
  r=list(map(F,core[name]));o=list(map(F,ops[name+'.entry']['rect']));w=o[3]-o[1]
  if w<=0:raise ValueError('PORTAL_WIDTH')
  return r[1]+w/2,r[3]-w/2
 sl,su=limits('stair');ll,lu=limits('lift');dl=max(2*(ll-mid),2*(mid-su));du=min(2*(lu-mid),2*(mid-sl))
 choices=[]
 for da in(1,-1):
  for db in(1,-1):
   for a,z in merge(domain_result['domains']['A:'+str(da)]):
    for b,y in merge(domain_result['domains']['B:'+str(db)]):
     poly=[(a,b),(z,b),(z,y),(a,y)]
     # Balance equations require both entries between the actual source poses.
     sx=F(m['common_routes']['stair_A'][0][0]);lx=F(m['common_routes']['lift_A'][0][0])
     if sx>=lx:raise ValueError('SOURCE_POSE_ORDER')
     for aa,bb,cc in [(1,0,lx),(-1,0,-sx),(0,1,lx),(0,-1,-sx)]:poly=clip(poly,aa,bb,cc)
     poly=clip(poly,1,-1,du);poly=clip(poly,-1,1,-dl)
     if len(poly)<3:continue
     area=abs(sum(p[0]*q[1]-q[0]*p[1]for p,q in zip(poly,poly[1:]+poly[:1])))/2
     if not area:continue
     xA=sum(p[0]for p in poly)/len(poly);xB=sum(p[1]for p in poly)/len(poly)
     choices.append((int(da<0)+int(db<0),-area,xA,xB,da,db,poly))
 if not choices:raise ValueError('NO_POSITIVE_AREA_BALANCED_PARAMETER_CELL')
 _,area,a,b,da,db,poly=min(choices);d=a-b
 return {'entry_x':{'A':str(a),'B':str(b)},'slide_direction':{'A':da,'B':db},'portal_y':{'stair':str(mid-d/2),'lift':str(mid+d/2)},'parameter_polygon':[[str(x),str(y)]for x,y in poly],'policy':'MINIMIZE_SOURCE_DIRECTION_CHANGES_THEN_LARGEST_PARAMETER_CELL_VERTEX_AVERAGE; engineering search ordering only','scope':'NECESSARY_PARAMETER_SELECTION_NOT_RECONSTRUCTED_PATH_OR_OPERATION_PROOF','accepted':False}
