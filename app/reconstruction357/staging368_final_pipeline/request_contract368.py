"""Typed fixed-scope request. Validation is not feasibility or admission."""
import json,hashlib,copy,re
from decimal import Decimal
FIELDS=('W','L','n','requested_count')
FIXED={'W':'26','L':'28','n':2,'requested_count':2}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def parse_json(body):
 if type(body)is not str or len(body.encode())>16384:raise ValueError('REQUEST_BODY_LIMIT')
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('DUPLICATE_FIELD:'+k)
   d[k]=v
  return d
 def no_float(s):raise ValueError('JSON_FLOAT_NOT_SUPPORTED_USE_DECIMAL_TEXT')
 raw=json.loads(body,object_pairs_hook=pairs,parse_float=no_float,parse_constant=no_float)
 e=normalize(raw);e['transport_body_sha256']=hashlib.sha256(body.encode()).hexdigest();return e
def normalize(raw):
 if type(raw)is not dict or set(raw)!=set(FIELDS):raise ValueError('EXACT_FIELD_INVENTORY_REQUIRED')
 norm={};types={}
 for k in FIELDS:
  v=raw[k]
  if type(v)not in(str,int):raise ValueError('INVALID_FIELD_TYPE:'+k)
  types[k]=type(v).__name__;s=str(v).strip().translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩٫','01234567890123456789.'))
  if len(s)>64 or not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?',s):raise ValueError('EXACT_DECIMAL_REQUIRED:'+k)
  d=Decimal(s)
  if k in('n','requested_count'):
   if type(v)is str and (str(v)!=str(v).strip() or not re.fullmatch(r'[1-9][0-9]*',s)):raise ValueError('COUNT_CANONICAL_DIGITS_REQUIRED:'+k)
   if d!=d.to_integral_value():raise ValueError('INTEGER_REQUIRED:'+k)
   norm[k]=int(d)
  else:
   if d!=Decimal(FIXED[k]):raise ValueError('UNSUPPORTED_EXACT_FIXED_DIMENSION:'+k)
   norm[k]=FIXED[k]
 if norm!=FIXED:raise ValueError('UNSUPPORTED_FIXED_SCOPE_26_28_TWO_UNITS_TWO_PLANS')
 canonical={'schema':'PLANHA_FIXED_REQUEST368','dimensions_m':{'W':{'numerator':26,'denominator':1},'L':{'numerator':28,'denominator':1}},'unit_count':2,'requested_count':2,'program_policy':'FIXED_SOURCE_THREE_BEDROOM_DOUBLE_TWIN_TWIN_NOT_OWNER_CUSTOM_PROGRAM'}
 return {'schema':'REQUEST_ENVELOPE368','received_input':copy.deepcopy(raw),'received_types':types,'received_digest':digest(raw),'normalized_raw':norm,'raw_digest':digest(norm),'canonical_request':canonical,'canonical_request_digest':digest(canonical),'scope':'FIXED_REQUEST_ONLY_NOT_5_TO_45_COVERAGE','accepted':False,'delivery_allowed':False}
def verify(e):
 if type(e)is not dict:raise ValueError('ENVELOPE_REQUIRED')
 base=normalize(e.get('received_input'))
 if set(e)-set(base)-{'transport_body_sha256'}:raise ValueError('ENVELOPE_EXTRA_FIELDS')
 if any(k not in e or digest(e[k])!=digest(v)for k,v in base.items()):raise ValueError('ENVELOPE_BINDING_CHANGED')
 if 'transport_body_sha256'in e and (type(e['transport_body_sha256'])is not str or not re.fullmatch('[0-9a-f]{64}',e['transport_body_sha256'])):raise ValueError('TRANSPORT_HASH_TYPE')
 return copy.deepcopy(base)
