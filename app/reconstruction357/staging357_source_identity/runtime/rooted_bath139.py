"""Exact right-root source placement study; no wall fabrication or gate override."""
from fractions import Fraction as F
from contract114 import S
from pathlib import Path
import json,hashlib
PINS={'bathroom_module117.py': '15bf1f24281af54d68f2b0ce0e92c366dff2600b014c606e7fa7b2bc44077be8', 'bathroom_source117.json': 'a31df1090677e03577f359b147052ca2cdf454863da00bdf663eafcc143e9428'}


def source_right(module):
 root=Path(__file__).parent
 for name,hsh in PINS.items():
  if hashlib.sha256((root/name).read_bytes()).hexdigest()!=hsh:raise ValueError('BATH_SOURCE_CHANGED')
 binding=module['source_binding']
 if binding['source_snapshot_sha256']!=PINS['bathroom_source117.json']or binding['producer_sha256']!=PINS['bathroom_module117.py']:raise ValueError('BATH_SOURCE_BINDING')
 hosts=[(k,tuple(map(F,q)))for k,q in module['wall_hosts'].items()if k.endswith('service_right')]
 if len(hosts)!=1:raise ValueError('UNIQUE_SOURCE_SERVICE_RIGHT_REQUIRED')
 name,q=hosts[0];w=F(module['input_program']['width']);h=F(module['input_program']['depth'])
 if not(q[0]==w<q[2]and q[1]<q[3]and q[1]<=0 and q[3]>=h):raise ValueError('SOURCE_RIGHT_HOST_CONTRACT')
 # Independently reconstruct the actual clipped/expanded service_right host
 # from immutable source coordinates and the unchanged producer transform.
 raw=json.loads((root/'bathroom_source117.json').read_text())
 base=tuple(F(str(v))-(F('.25')if i%2==0 else F('6.725'))for i,v in enumerate(raw['walls']['A.service_right']))
 expected=tuple(v+(w-F('3.15')if i%2==0 else h-F('2.25'))if v>=(F('3.15')if i%2==0 else F('2.25'))else v for i,v in enumerate(base))
 if q!=expected:raise ValueError('SOURCE_HOST_GEOMETRY_MISMATCH')
 return name,q

def anchor(module,box):
 name,q=source_right(module);x0,y0,x1,y1=map(F,box);w=F(module['input_program']['width']);h=F(module['input_program']['depth'])
 x=x1-q[2];lo=max(y0,y0-q[1]);hi=min(y1-h,y1-q[3])
 if x<x0 or x+w>x1 or lo>hi:raise ValueError('ROOTED_SOURCE_DOES_NOT_FIT')
 return {'source_host':name,'source_host_rect':list(map(S,q)),'bath_x':S(x),'bath_y_min':S(lo),'bath_y_max':S(hi),'source_skin_m':S(q[2]-w),'root_face_x':S(x1),'scope':'Right shell contact study, not full host-network acceptance.'}

def validate(module,box,bath):
 try:
  r=anchor(module,box);a,b,c,d=map(F,bath);w=F(module['input_program']['width']);h=F(module['input_program']['depth']);_,q=source_right(module);x0,y0,x1,y1=map(F,box)
  if(c-a,d-b)!=(w,h):raise ValueError('BATH_SOURCE_SIZE_CHANGED')
  if a!=F(r['bath_x'])or not(F(r['bath_y_min'])<=b<=F(r['bath_y_max'])):raise ValueError('ROOT_PLACEMENT_DRIFT')
  world=(a+q[0],b+q[1],a+q[2],b+q[3]);overlap=min(world[3],y1)-max(world[1],y0)
  if world[2]!=x1 or overlap<=0:raise ValueError('NO_POSITIVE_RIGHT_SHELL_CONTACT')
  return {'status':'EXACT_RIGHT_SOURCE_CONTACT','source_host':r['source_host'],'host_rect':list(map(S,world)),'contact_length_m':S(overlap),'root_face_x':S(x1)}
 except(KeyError,ValueError,TypeError)as exc:return {'status':'ROOT_CONTACT_REJECTED','reason':str(exc)}
