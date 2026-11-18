"""Reconstructed357 exact measurements. New code, not recovered353 bytes."""
from fractions import Fraction as F
import hashlib,json

def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def rational(x):
 if type(x)not in(str,int):raise ValueError('EXACT_NUMBER_REQUIRED')
 return F(x)
def parts(x):
 if type(x)is not list:raise ValueError('REGION_REQUIRED')
 return [x]if len(x)==4 and all(type(y)in(str,int)for y in x)else x

def rectangle_union_area(rs):
 rs=[tuple(map(rational,r))for r in rs]
 if any(len(r)!=4 or r[0]>=r[2]or r[1]>=r[3]for r in rs):raise ValueError('POSITIVE_RECT_REQUIRED')
 xs=sorted({r[i]for r in rs for i in(0,2)});ys=sorted({r[i]for r in rs for i in(1,3)})
 return sum(((b-a)*(d-c)for a,b in zip(xs,xs[1:])for c,d in zip(ys,ys[1:])if any(x<=(a+b)/2<=X and y<=(c+d)/2<=Y for x,y,X,Y in rs)),F())
def intersect(a,b):
 a,b=list(map(rational,a)),list(map(rational,b));r=[max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3])]
 return list(map(str,r))if r[0]<r[2]and r[1]<r[3]else None

def route_metrics(path):
 if type(path)is not list or len(path)<2:raise ValueError('PATH_REQUIRED')
 points=[tuple(map(rational,p))for p in path]
 if any(len(p)!=2 for p in points):raise ValueError('POINT_REQUIRED')
 total=F();dirs=[]
 for a,b in zip(points,points[1:]):
  dx,dy=b[0]-a[0],b[1]-a[1]
  if bool(dx)==bool(dy):raise ValueError('NONZERO_ORTHOGONAL_SEGMENT_REQUIRED')
  total+=abs(dx)+abs(dy);dirs.append((dx>0,dx<0,dy>0,dy<0))
 return {'length':str(total),'direction_changes':sum(a!=b for a,b in zip(dirs,dirs[1:]))}

def measure_model(model):
 out={'units':{},'common':{},'scope':'EXACT_DECLARED_GEOMETRY_NOT_FUNCTIONAL_NECESSITY'}
 for u in model['units']:
  if u['id']in out['units']:raise ValueError('DUPLICATE_UNIT')
  owned=parts(u['ownership']);overlap=[r for a in owned for b in model['walls'].values()if(r:=intersect(a,b))]
  net=rectangle_union_area(owned)-rectangle_union_area(overlap)
  if net<=0:raise ValueError('POSITIVE_NET_REQUIRED')
  area=rectangle_union_area([r for k in ('bath','WC','toilet')if k in u['rooms']for r in parts(u['rooms'][k])])
  if not any(k in u['rooms']for k in('bath','WC','toilet')):raise ValueError('SERVICE_ROLE_MISSING')
  routes={}
  for k,v in u['routes'].items():
   try:routes[k]=route_metrics(v)
   except ValueError as e:routes[k]={'status':'UNSUPPORTED','code':str(e)}
  out['units'][u['id']]={'unit_net_m2':str(net),'bath_wc_union_m2':str(area),'service_ratio_percent':str(100*area/net),'declared_circulation_union_m2':str(rectangle_union_area([r for k in('private_circulation','entry_circulation')if k in u['rooms']for r in parts(u['rooms'][k])])),'routes':routes,'geometry_fingerprint':digest({'rooms':u['rooms'],'routes':u['routes'],'fixtures':u['fixtures']})}
 out['common']={'areas_m2':{k:str(rectangle_union_area(parts(v)))for k,v in model['common_spaces'].items()},'routes':{k:route_metrics(v)for k,v in model['common_routes'].items()}}
 for prefix in('stair_','lift_'):
  ls=[F(v['length'])for k,v in out['common']['routes'].items()if k.startswith(prefix)]
  out['common'][prefix+'route_spread_m']=str(max(ls)-min(ls))if ls else None
 return out

def compare_vectors(a,b,p,q):
 if not a or set(a)!=set(b)or not p or set(p)!=set(q):raise ValueError('VECTOR_INVENTORY')
 a,b,p,q=({k:rational(v)for k,v in x.items()}for x in(a,b,p,q));protected=all(q[k]<=p[k]for k in p)
 return {'strictly_dominates':protected and all(b[k]<=a[k]for k in a)and any(b[k]<a[k]for k in a),'protected_not_degraded':protected,'rule_acceptance':False,'scope':'ARITHMETIC_ONLY_NEEDS_ELIGIBLE_MATCHED_FUNCTIONAL_COHORT'}
