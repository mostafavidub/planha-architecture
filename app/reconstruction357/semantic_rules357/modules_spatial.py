"""Reconstructed357 spatial evidence adapter. Not byte-recovered353 code."""
import hashlib,json
from fractions import Fraction as F

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def rect(v):
 if type(v)is not list or len(v)!=4 or any(type(x)not in(str,int)for x in v):raise ValueError('EXACT_RECT_REQUIRED')
 r=tuple(F(x)for x in v)
 if r[0]>=r[2]or r[1]>=r[3]:raise ValueError('POSITIVE_RECT_REQUIRED')
 return r
def intersection(a,b):
 r=max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3]);return r if r[0]<r[2]and r[1]<r[3]else None
def union_area(rs):
 if not rs:return F(0)
 xs=sorted({r[i]for r in rs for i in(0,2)});a=F(0)
 for x,y in zip(xs,xs[1:]):
  ivs=sorted((r[1],r[3])for r in rs if r[0]<y and r[2]>x);end=None;length=F(0)
  for b,t in ivs:
   if end is None or b>end:length+=t-b;end=t
   elif t>end:length+=t-end;end=t
  a+=(y-x)*length
 return a
def subtract_rect(a,b):
 q=intersection(a,b)
 if q is None:return[a]
 x,y,xx,yy=q
 return[r for r in[(a[0],a[1],x,a[3]),(xx,a[1],a[2],a[3]),(x,a[1],xx,y),(x,yy,xx,a[3])]if r[0]<r[2]and r[1]<r[3]]
def difference(source,covers,cap=20000):
 remaining=list(source)
 for c in covers:
  remaining=[p for r in remaining for p in subtract_rect(r,c)]
  if len(remaining)>cap:raise ValueError('REGION_WORK_CAP')
 return remaining
def ownership_overlap(model):
 units=model['units'];ids=[u['id']for u in units]
 if not ids or len(ids)!=len(set(ids)):raise ValueError('UNIQUE_UNITS')
 out=[]
 for i,u in enumerate(units):
  for v in units[i+1:]:
   overlaps=[z for a in u['ownership']for b in v['ownership']if(z:=intersection(rect(a),rect(b)))];out.append({'units':[u['id'],v['id']],'intersection_area_m2':str(union_area(overlaps))})
 return out
def source_sweeps(path,body):
 out=[];h=F(body)/2
 if h<=0:raise ValueError('BODY')
 for a,b in zip(path,path[1:]):
  if any(type(x)not in(str,int)for x in a+b):raise ValueError('EXACT_POINT_REQUIRED')
  a,b=tuple(map(F,a)),tuple(map(F,b))
  if len(a)!=2 or len(b)!=2 or(a[0]!=b[0]and a[1]!=b[1]):raise ValueError('ORTHOGONAL_PATH_REQUIRED')
  out.append((min(a[0],b[0])-h,min(a[1],b[1])-h,max(a[0],b[0])+h,max(a[1],b[1])+h))
 return out
def residual_function_extent(model):
 out=[]
 for u in model['units']:
  role=u['spatial_role_bindings']['open_public_envelope'];source=[rect(r)for r in role['regions']]
  if role['source_room_key']!='living'or sorted(source)!=sorted(rect(r)for r in u['rooms']['living']):raise ValueError('PUBLIC_SOURCE_EXTENT')
  known=[rect(r)for r in u['fixtures'].values()]+[rect(r)for r in u['activities'].values()]
  for mapping in(u['routes'],u['scenario_routes']):
   for path in mapping.values():known+=source_sweeps(path,model['profile']['body_m'])
  rem=difference(source,known)
  out.append({'unit':u['id'],'open_public_area_m2':str(union_area(source)),'outside_declared_object_activity_path_area_m2':str(union_area(rem)),'unresolved_rectangles':[list(map(str,r))for r in rem],'status':'UNRESOLVED_NOT_PROVED_FUNCTIONLESS','missing':['WHOLE_FUNCTIONAL_REGION_SOURCE_ROLE_AND_INDEPENDENT_USE'],'contract':'Q11 unknown_predicate: unresolved>0 is not automatically geometric FAIL','source_extent_digest':digest(role['regions'])})
 return out
RULES={
 'SPACE_ACCOUNTING':(('partition_ledger','unit_independence'),('ALL_POSITIVE_AREA_FINAL_ROLE_FUNCTION',)),
 'LIVING_USEFUL_CONTIGUITY':(('fixture_inventory_use','chair_capacity_movement'),('SOURCE_COMPLETE_SITTING_AND_CONNECTED_ACCESS','R_LIV_APPLICABILITY')),
 'GUEST_ROUTE_INDEPENDENCE':(('guest_living_route','guest_dining_route','bath_nonprivate_access'),('ALL_FOUR_RELATIONS_SOURCE_SCENARIOS',)),
 'PRIVACY_WITHOUT_FAKE_BAFFLE':(('privacy_scenarios','q11_functional_boundary'),('ALL_SOURCE_REQUIRED_VISIBILITY','EVERY_WALL_CONSTRUCTIVE_PURPOSE'))}
def evaluate(model,raw_report):
 try:
  from common import rows
  rs=rows(model,raw_report);binding=True
 except (ImportError,ValueError,KeyError,TypeError):rs={};binding=False
 out={}
 for rid,(deps,missing0)in RULES.items():
  missing=list(missing0);evidence=[];codes=[];metrics={}
  if not binding:missing.append('SOURCE_FRESH_BINDING_REQUIRED')
  else:
   for dep in deps:
    row=rs.get(dep)
    if row is None:missing.append('MISSING_REQUIREMENT:'+dep);continue
    evidence.append({'requirement':dep,'row_digest':digest(row),'status':row['status'],'source_method':row.get('method')})
    if row['status']!='PASS_LIMITED':missing.append('SOURCE_SUBCONDITION_UNPROVEN:'+dep)
   if rid=='SPACE_ACCOUNTING':
    try:
     metrics['unit_ownership_overlap']=ownership_overlap(model)
     if any(F(r['intersection_area_m2'])>0 for r in metrics['unit_ownership_overlap']):codes.append('POSITIVE_EXACT_UNIT_OWNERSHIP_OVERLAP')
     metrics['residual_function_extent']=residual_function_extent(model)
    except (ValueError,KeyError,TypeError,ZeroDivisionError):missing.append('EXACT_SPATIAL_GEOMETRY_REQUIRED')
  out[rid]={'verdict':'FAIL'if codes else'UNKNOWN','codes':codes or['SEMANTIC_OBLIGATIONS_NOT_COMPLETE'],'missing':missing,'evidence':evidence,'metrics':metrics,'model_hash':digest(model),'parent_complete':False,'reconstruction_version':357}
 return out
