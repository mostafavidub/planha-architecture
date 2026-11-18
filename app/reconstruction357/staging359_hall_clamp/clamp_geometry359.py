"""New source121 hall-bound operationalization. No whole-plan acceptance.
Exact typed inputs only; full-width connector strips preserved independently of
route centerline sweeps. No case coordinates, area cutoff or 0.7 constant.
"""
from fractions import Fraction as F

def rect(r):
 if type(r)not in(list,tuple)or len(r)!=4 or any(type(x)not in(str,int,F)for x in r):raise ValueError('EXACT_RECT')
 a,b,c,d=map(F,r)
 if not a<c or not b<d:raise ValueError('POSITIVE_RECT')
 return a,b,c,d

def clamp(hall,connector_regions,interface,required_paths,operation_envelopes,body):
 left,rear,right,back=rect(hall);body=F(body)
 if body<=0 or not required_paths or not connector_regions:raise ValueError('REQUIRED_SOURCE_INVENTORY')
 reservations=[]
 def add(r,origin):
  a,b,c,d=rect(r)
  # Closed contact at hall front matters for connector continuity.
  if d>=rear and b<=back and c>left and a<right:
   reservations.append({'interval':[str(max(left,a)),str(min(right,c))],'source':origin})
 for i,r in enumerate(connector_regions):add(r,'SOURCE_FULL_WIDTH_CONNECTOR:'+str(i))
 add(interface,'SOURCE_PUBLIC_INTERFACE')
 for k,path in sorted(required_paths.items()):
  if len(path)<2:raise ValueError('SOURCE_PATH_REQUIRED')
  for i,(a,b)in enumerate(zip(path,path[1:])):
   ax,ay=map(F,a);bx,by=map(F,b)
   if (ax==bx)==(ay==by):raise ValueError('NONZERO_ORTHOGONAL_PATH')
   h=body/2;add([min(ax,bx)-h,min(ay,by)-h,max(ax,bx)+h,max(ay,by)+h],'SOURCE_BODY_ROUTE:'+k+':'+str(i))
 for k,r in sorted(operation_envelopes.items()):add(r,'SOURCE_OPERATION_OR_ACTIVITY:'+k)
 if not reservations:raise ValueError('UNPROVED_EMPTY_REQUIRED_REGION')
 lo=min(F(q['interval'][0])for q in reservations);hi=max(F(q['interval'][1])for q in reservations)
 if not left<=lo<hi<=right:raise ValueError('BAD_CLAMP')
 return {'hall':[str(lo),str(rear),str(hi),str(back)],'before':list(map(str,(left,rear,right,back))),'reservations':reservations,'released_area_m2':str(((lo-left)+(right-hi))*(back-rear)),'accepted':False,'released_floor_function':'NOT_ESTABLISHED','wall_attachment':'REQUIRES_RECONSTRUCTION_AND_INDEPENDENT_CHECK'}
