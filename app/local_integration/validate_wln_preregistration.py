"""Validate preregistered expectations against input/preflight only; never calls runtime."""
import json,hashlib
from pathlib import Path
from public_wln_contract import parse_public
from live_program_scheduler import preflight
from dimension_contract import InputError
ROOT=Path(__file__).resolve().parents[2]
def validate(path):
 spec=json.loads(path.read_text());assert spec['schema']=='TASK5_1_PREREGISTERED_WLN_MATRIX_V1'
 assert spec['preregistered_before_matrix_execution'] is True and spec['execution_plan_5_2']['new_solver_calls']==0
 assert spec['public_fields']==['W','L','n']
 assert spec['owner_range']=={'min':5,'max':25,'inclusive':True,'no_clamping':True}
 required={'app/local_integration/'+x for x in ('public_wln_contract.py','dimension_contract.py','live_program_scheduler.py','same_version_front_rear_contract.py','public_wln_server.py')}
 assert set(spec['source_blob_shas'])==set(spec['source_paths'])==required
 for p,h in spec['source_blob_shas'].items():
  b=(ROOT/p).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==h
 ids=[c['id'] for c in spec['cases']];assert len(ids)==len(set(ids))==28
 rows=[]
 for c in spec['cases']:
  e=c['expected'];assert e['wire_contract_accepted'] is e['input_valid'];body=c['body'].encode();row={'id':c['id'],'body_sha256':hashlib.sha256(body).hexdigest()}
  try:
   envelope=parse_public(body);pf=preflight(body)
   assert e['input_valid'] is True and pf['state']==e['state_or_code'] and pf['execution_ready'] is e['execution_ready']
   assert all(envelope[k] is False for k in ('accepted','qualified','display_allowed','delivery_allowed'))
   row.update(input_valid=True,state=pf['state'],execution_ready=pf['execution_ready'])
   if pf['execution_ready']:assert e['http_status'] is None
  except InputError as ex:
   assert e['input_valid'] is False and ex.code==e['state_or_code'] and ex.status==e['http_status']
   row.update(input_valid=False,code=ex.code,status=ex.status)
  assert e['delivery_allowed'] is False and e['geometric_feasibility']=='NOT_INFERRED'
  rows.append(row)
 return {'schema':'TASK5_1_PREREGISTRATION_VALIDATION_V1','cases':rows,'case_count':len(rows),
  'actual_http_requests':0,'solver_calls':0,'fresh_geometry':False,'scope':'Parser/preflight expectation validation only; actual HTTP matrix is5.2',
  'spec_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),**{k:False for k in ('accepted','qualified','display_allowed','delivery_allowed')}}
if __name__=='__main__':
 out=validate(ROOT/'specs/V25_TASK_5_1_WLN_MATRIX_PREREGISTRATION.json')
 Path('preregistration-validation.json').write_text(json.dumps(out,sort_keys=True,indent=2));print(json.dumps(out,sort_keys=True))
