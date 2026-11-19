"""Exact input and JSON boundary study, not an active public generator.
Binary64 equality is separate from decimal geometry and solver approximation.
"""
import copy,json,math
from fractions import Fraction as F
from public_wln_contract import parse_public,verify_public,engine_raw
from same_version_front_rear_contract import digest
from front_rear_runtime_adapter import transport,proposal_transport
from core_choice_pair_study import selected_core
def need(ok,code):
 if not ok:raise ValueError(code)
def prepare(body):
 e=parse_public(body);verify_public(body,e);raw=engine_raw(e)
 ratios={}
 for axis in ('W','L'):
  r=e['canonical_request']['dimensions_m'][axis]
  q=F(int(r['numerator']),int(r['denominator']))
  need(F(raw[axis])==q,'EXACT_INPUT_RATIO')
  ratios[axis]=[str(q.numerator),str(q.denominator)]
 return {'raw':raw,'envelope':e,'ratios':ratios,'raw_digest':digest(raw),'envelope_digest':digest(e)}
def gated_propose(body,producer,seconds=30):
 # The exact wrapper used by the study. Invalid inputs cannot reach producer.
 # This is NOT public preflight readiness or production permission.
 p=prepare(body)
 try:core,_=selected_core(p['raw'],'FRONT_REAR_COMPACT118')
 except ValueError as ex:
  if str(ex)!='CURRENT_CORE_METHOD_NO_FIT_NOT_INFEASIBLE':raise
  return p,None,{'status':'STUDY_CORE_NO_FIT_NOT_INFEASIBLE'}
 result=producer(core,2,time_limit=seconds,variant=0,sleep_roles=['double','twin'],ordered_macro=False,topology='SIDE_ROOTED_SERVICES')
 return p,core,result
def roundtrip(value):
 normalized,receipt=transport(value);pin=digest(normalized)
 encoded=json.dumps(normalized,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()
 reread=json.loads(encoded)
 records=[]
 def compare(a,b,path):
  need(type(a)is type(b),'ROUNDTRIP_EXACT_TYPE')
  if type(a)is dict:
   need(set(a)==set(b),'ROUNDTRIP_KEYS')
   for k in a:compare(a[k],b[k],path+[k])
  elif type(a)is list:
   need(len(a)==len(b),'ROUNDTRIP_LENGTH')
   for i,(x,y)in enumerate(zip(a,b)):compare(x,y,path+[i])
  elif type(a)is float:
   need(math.isfinite(a)and a.hex()==b.hex()and a.as_integer_ratio()==b.as_integer_ratio(),'ROUNDTRIP_BINARY64')
   records.append({'path':path,'hex':a.hex(),'ratio':[str(x)for x in a.as_integer_ratio()]})
  else:need(a==b,'ROUNDTRIP_SCALAR')
 compare(normalized,reread,[])
 need(digest(reread)==pin,'ROUNDTRIP_DIGEST')
 return reread,{'schema':'EXACT_JSON_ROUNDTRIP208_V1','before_digest':pin,'after_digest':digest(reread),
  'binary64_records':records,'binary64_count':len(records),'binary64_record_digest':digest(records),
  'tuple_conversion_count':len(receipt['tuple_paths']),'byte_count':len(encoded),
  'scope':'Finite binary64 and exact typed JSON equality, not exact MILP arithmetic or equality of binary ratio to decimal geometry',
  'accepted':False,'qualified':False}
def coordinate_receipt(original,normalized,receipt):
 need(digest(original)==digest(normalized),'COORDINATE_DIGEST')
 import numpy as np
 expected=[]
 for name,values in original.get('rectangles',{}).items():
  for i,x in enumerate(values):
   if type(x)is np.float64:expected.append(['rectangles',name,i])
 for name,points in original.get('network_paths',{}).items():
  for i,point in enumerate(points):
   for j,x in enumerate(point):
    if type(x)is np.float64:expected.append(['network_paths',name,i,j])
 supplied=[r['path']for r in receipt['coordinate_conversions']]
 need(len(supplied)==len(expected)and len({digest(p)for p in supplied})==len(supplied)and {digest(p)for p in supplied}=={digest(p)for p in expected},'COORDINATE_RECEIPT_COVERAGE')
 rows=[]
 for r in receipt['coordinate_conversions']:
  path=r['path'];need(path[0]in ('rectangles','network_paths'),'COORDINATE_ROLE')
  x,y=original,normalized
  for k in path:x,y=x[k],y[k]
  need(type(y)is float and math.isfinite(y),'NORMALIZED_COORDINATE')
  binary=y.as_integer_ratio();decimal=F(str(y))
  need(x.as_integer_ratio()==binary and r['binary_ratio']==[str(v)for v in binary]and r['hex']==y.hex(),'COORDINATE_BINARY_RATIO')
  rows.append({'path':path,'binary_ratio':[str(v)for v in binary],'decimal_ratio':[str(decimal.numerator),str(decimal.denominator)],'hex':y.hex()})
 return {'schema':'ROLE_COORDINATE_PRECISION208_V1','proposal_digest':digest(normalized),'conversion_count':len(rows),
  'records':rows,'record_digest':digest(rows),'binary_ratio_and_decimal_ratio_are_distinct':True,'accepted':False,'qualified':False}
