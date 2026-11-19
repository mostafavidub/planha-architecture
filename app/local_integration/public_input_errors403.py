"""Versioned error-set diagnostics; V3 acceptance and wire policy are unchanged."""
import json,hashlib,inspect
from pathlib import Path
import public_wln_contract as v3
import dimension_contract as dim
ROOT=Path(__file__).resolve().parents[2]
SCHEMA='PUBLIC_WLN_ERROR_SET_V1'
PINS={'public_wln_contract.py':'80fd2b2710342735dc35e484c9b0da790995d830','dimension_contract.py':'058502cd97b5131908b82fdbdba34c62d3376ea3'}
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def guard():
 out={}
 for name,pin in PINS.items():
  p=Path(__file__).with_name(name);b=p.read_bytes()
  if hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()!=pin:raise ValueError('ERROR_SET_SOURCE_CHANGED')
  mod=v3 if name.startswith('public')else dim
  if Path(mod.__file__).resolve()!=p.resolve():raise ValueError('ERROR_SET_IMPORT_PATH')
  out[name]=hashlib.sha256(b).hexdigest()
 for fn,name in [(v3.parse_public,'public_wln_contract.py'),(v3._unit_count,'public_wln_contract.py'),(dim._number,'dimension_contract.py'),(dim._bounded_tree,'dimension_contract.py')]:
  if Path(inspect.getsourcefile(fn)).resolve()!=Path(__file__).with_name(name).resolve():raise ValueError('ERROR_SET_CALLABLE_PATH')
 return out
def row(e):return {'code':e.code,'field':e.field,'status':e.status}
class ErrorSet(dim.InputError):
 def __init__(self,primary,errors,scope):
  super().__init__(primary.code,primary.field,primary.status)
  self.errors=errors;self.scope=scope
def structural(body):
 # Same structural precedence as V3, including wire decimal rejection.
 if type(body)is not bytes:raise dim.InputError('BODY_BYTES_REQUIRED')
 if len(body)>dim.MAX_BODY:raise dim.InputError('UNSUPPORTED_BODY_LIMIT',status=409)
 try:
  raw=json.loads(body.decode('utf-8'),object_pairs_hook=dim._pairs,parse_float=dim.JsonDecimal,parse_int=dim._integer,parse_constant=dim._nonfinite)
 except dim.InputError:raise
 except RecursionError:raise dim.InputError('UNSUPPORTED_NESTING_DEPTH',status=409)
 except (UnicodeError,ValueError):raise dim.InputError('JSON_SYNTAX_INVALID')
 bounded=dict(raw)if type(raw)is dict else raw
 if type(bounded)is dict and isinstance(bounded.get('n'),dim.JsonDecimal):bounded['n']=0
 dim._bounded_tree(bounded)
 if type(raw)is not dict:raise dim.InputError('OBJECT_REQUIRED')
 if set(raw)-{'W','L','n'}:raise dim.InputError('UNEXPECTED_PUBLIC_FIELD',sorted(set(raw)-{'W','L','n'})[0])
 return raw
def parse_public_errors(body):
 pin=guard()
 try:
  try:return v3.parse_public(body)
  except dim.InputError as primary:
   try:raw=structural(body)
   except dim.InputError:
    raise ErrorSet(primary,[row(primary)],'STRUCTURAL_FAIL_FAST') from None
   errors=[]
   for field in ('W','L','n'):
    try:
     if field=='n':v3._unit_count(raw.get('n'))
     elif field not in raw:raise dim.InputError('FIELD_REQUIRED',field)
     else:dim._number(raw[field],field)
    except dim.InputError as error:errors.append(row(error))
   if not errors:raise ValueError('ERROR_SET_UNCLASSIFIED_PRIMARY')
   if row(primary)not in errors:raise ValueError('ERROR_SET_PRIMARY_NOT_PRESERVED')
   raise ErrorSet(primary,errors,'INDEPENDENT_FIELD_ERRORS') from None
 finally:
  if guard()!=pin:raise ValueError('ERROR_SET_SOURCE_CHANGED')
def response(error):
 errors=getattr(error,'errors',[row(error)])
 return {'schema':SCHEMA,'acceptance_contract':v3.SCHEMA,'code':error.code,'field':error.field,
  'primary_status':error.status,'errors':errors,'error_scope':getattr(error,'scope','SINGLE_CONTRACT_ERROR'),
  'generation_started':False,**{k:False for k in AUTH}}
