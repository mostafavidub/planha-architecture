"""Independent closed D4-extension contract. Component geometry, never admission."""
from pathlib import Path
import hashlib
from contract114 import digest
from checker114 import check_module, check_twin_module

PINS = {
 'PRIVATE_ROOM_MODULE116': ('bedroom_module116.py','21bcadf03beb91b9b78a85d2b87520b594c19dce28b932860d871744e4815789','c876cb026c2f227a10ed6a36ba6e49f0dc9c92fcf2c7ab300d42236ed2bf3fc1'),
 'PRIVATE_TWIN_ROOM_MODULE118': ('twin_module118.py','074c6f39f613977e0d7417a99f0d9682343d433713774faa7a18c85283e93260','82e66b18d79b2b5ad3eb8aebff1ac3625ee4ac11279d44cec8950b712df901f8'),
}
EXPECTED_D4 = {(a,b,c,d) for a,b,c,d in __import__('itertools').product((-1,0,1),repeat=4) if a*a+c*c==1 and b*b+d*d==1 and a*b+c*d==0}

def examine(wrapper):
 errors=[];pending=[];evidence={}
 def require(ok,code):
  if not ok:errors.append({'code':code})
 try:
  require(type(wrapper)is dict and set(wrapper)=={'schema','contract_version','base_module','base_hash','placement_contract','provenance','accepted'},'WRAPPER_CLOSED_FIELDS')
  require(wrapper.get('schema')=='ROTATABLE_PRIVATE_SOURCE133','WRAPPER_SCHEMA')
  require(wrapper.get('contract_version')=='D4_SOURCE_EXTENSION_133_V1','WRAPPER_VERSION')
  require(wrapper.get('accepted')is False,'NO_INHERITED_ADMISSION')
  m=wrapper['base_module'];pin=PINS.get(m.get('schema'))
  require(pin is not None,'UNREVIEWED_BASE_ROLE')
  if pin is None:raise ValueError('unknown base schema')
  producer,sha,basehash=pin
  require(digest(m)==wrapper['base_hash']==basehash,'IMMUTABLE_REVIEWED_BASE_HASH')
  contract=wrapper['placement_contract']
  require(type(contract)is dict and set(contract)=={'allowed_matrices','scale_allowed','revalidate_after_placement'},'CONTRACT_CLOSED_FIELDS')
  require(contract.get('scale_allowed')is False and contract.get('revalidate_after_placement')is True,'CONTRACT_NO_SCALE_RECHECK')
  mats=contract.get('allowed_matrices');valid=type(mats)is list and len(mats)==8
  if valid:
   valid=all(type(a)is list and len(a)==2 and all(type(row)is list and len(row)==2 and all(type(v)is int for v in row)for row in a)for a in mats)
  require(valid and {tuple(v for row in a for v in row)for a in mats}==EXPECTED_D4 if valid else False,'EXACT_EIGHT_D4_INTEGER_MATRICES')
  expected={'base_producer':producer,'base_producer_sha256':sha,'scope':'SOURCE_GEOMETRY_D4_EXTENSION_NOT_WHOLE_PLAN'}
  require(type(wrapper['provenance'])is dict and wrapper['provenance']==expected,'EXACT_PINNED_PROVENANCE')
  for filename,filesha,_ in PINS.values():
   require(hashlib.sha256(Path(__file__).with_name(filename).read_bytes()).hexdigest()==filesha,'BASE_PRODUCER_BYTES_'+filename)
  # No untrusted widened base is submitted to the old checker.
  if not errors:
   gate=(check_twin_module if m['schema']=='PRIVATE_TWIN_ROOM_MODULE118'else check_module)(m)
   require(gate.get('status')=='PASS_MODULE_SCOPED'and not gate.get('errors')and not gate.get('pending'),'BASE_FRESH_COMPONENT_GATE')
   evidence['base_status']=gate.get('status');evidence['base_errors']=gate.get('errors',[]);pending.extend(gate.get('pending',[]))
 except Exception as exc:errors.append({'code':'MALFORMED_EXTENSION','detail':str(exc)})
 return {'status':'PASS_SOURCE_D4_CONTRACT_SCOPED'if not errors and not pending else'FAIL_SOURCE_D4_CONTRACT','errors':errors,'pending':pending,'accepted':False,'scope':'ENGINEERING_SOURCE_GEOMETRY_ONLY_NOT_WHOLE_PLAN_OR_REGULATORY_APPROVAL','evidence':evidence}
