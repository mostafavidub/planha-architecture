"""Reconstructed357 structure measurements. No historical verdict is inherited.
Rendered233 recovered separately; required semantic joins remain unimplemented.
"""
from fractions import Fraction
from applicability import digest,number,rliv_applicability
RULES=('OPENINGS_REAL','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING')

def rectangle(v):
 if type(v) not in (list,tuple) or len(v)!=4:raise ValueError('RECT_SHAPE')
 if any(type(x) not in (str,int) for x in v):raise ValueError('RECT_EXACT_TYPE')
 a,b,c,d=map(Fraction,v)
 if c<=a or d<=b:raise ValueError('RECT_POSITIVE_EXTENT')
 return a,b,c,d

def unique(items,key='id'):
 if type(items) is not list:raise ValueError('INVENTORY_LIST')
 ids=[]
 for x in items:
  if type(x) is not dict or type(x.get(key)) is not str or not x[key].strip():raise ValueError('INVENTORY_ID')
  ids.append(x[key])
 if len(ids)!=len(set(ids)):raise ValueError('DUPLICATE_ID')
 return ids

def inspect(model):
 units=model['units'];unique(units)
 program=model['program'];n=number(model['inputs'][2])
 if n.denominator!=1 or type(program.get('units')) is not int or program['units']!=n or len(units)!=n:raise ValueError('UNIT_COUNT_MISMATCH')
 beds=program.get('bedrooms_per_unit');roles=program.get('sleep_roles')
 if type(beds) is not int or beds<1 or type(roles) is not list or len(roles)!=beds or any(type(x) is not str or not x.strip() for x in roles):raise ValueError('PROGRAM_STRUCTURE')
 measured={}
 for u in units:
  rooms=u['rooms']
  if type(rooms) is not dict or any(type(k) is not str or not k.strip() for k in rooms):raise ValueError('ROOM_ID')
  bedrooms={k:v for k,v in rooms.items() if k.startswith('bed')}
  if len(bedrooms)!=beds:raise ValueError('BEDROOM_COUNT_MISMATCH')
  area={}
  for name,parts in rooms.items():
   if type(parts) is not list or not parts:raise ValueError('ROOM_GEOMETRY_MISSING')
   rects=[rectangle(p) for p in parts]
   # Sum is explicitly NOT union area, usable area or capacity proof.
   area[name]=str(sum((c-a)*(d-b) for a,b,c,d in rects))
  measured[u['id']]={'bedroom_ids':sorted(bedrooms),'rectangle_area_sum_not_union':area}
 opening_ids=unique(model['openings'])
 for o in model['openings']:
  rectangle(o['rect'])
  if type(o.get('connects')) is not list or len(o['connects'])!=2 or any(type(x) is not str or not x for x in o['connects']):raise ValueError('OPENING_CONNECTION_IDS')
 return {'units':measured,'opening_ids':opening_ids,'program':program,'rliv':rliv_applicability(model)}

def evaluate(model,raw_report):
 out={k:{'verdict':'UNKNOWN','codes':['RECONSTRUCTED_CONTRACT_CLOSURE_UNPROVEN'],'evidence':{},'missing':['COMPLETE_EXECUTED_RENDERED233_SOURCE_OBLIGATIONS'],'reconstruction':357} for k in RULES}
 try:
  from common import rows
  rs=rows(model,raw_report)
 except (ValueError,TypeError,KeyError,ImportError) as e:
  for v in out.values():v['codes']=['SOURCE_BINDING_UNVERIFIED',str(e)]
  return out
 try:measured=inspect(model)
 except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError) as e:
  for v in out.values():v['codes']=['MODEL_DATA_INCOMPLETE_OR_INVALID',str(e)]
  return out
 for v in out.values():v['evidence']={'model_digest':digest(model),'raw_digest':digest(raw_report),'bound_requirement_ids':sorted(rs),'measurement':measured}
 out['OPENINGS_REAL']['missing']+=['BOUND_HOST_ADJACENCY_OPERATION_WINDOW_COVERAGE']
 out['ROOM_PROGRAM_CAPACITY']['missing']+=['BOUND_ACTUAL_INSTANCE_CAPACITY_AND_USABILITY','R_LIV_APPLICABILITY_AND_SCOPED_PROOF']
 out['BEDROOM_GROUPING']['missing']+=['IR_P13_BATH_ENTRY_PUBLIC_ROUTE_LENGTHS_AND_APPLICABLE_ALTERNATIVE_COMPARISON_UNVERIFIED']
 return out
