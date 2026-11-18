"""Add fixed-source audited SERVICE365 dependency; Q04 remains independent."""
import json,hashlib
from pathlib import Path
from common import digest
from role_registry_model365_v2 import evaluate as base_evaluate
from role_registry_model365 import DAG,ordered_dag
from service_runner365 import evaluate as service_evaluate
ROOT=Path(__file__).resolve().parents[1]
RUNNER_SHA='5bedd36276ae8b58951fb634291efd5f22941c677266d76d1b5eebf756fa5f32'
def evaluate(record,review):
 path=Path(__file__).with_name('service_runner365.py')
 if hashlib.sha256(path.read_bytes()).hexdigest()!=RUNNER_SHA:raise ValueError('SERVICE365_RUNNER_PIN')
 before=digest([record,review]);out=base_evaluate(record,review);service=service_evaluate(record,review);mh=digest(record['candidate']['model'])
 if service['verdict']!='PASS_SCOPED_FINITE_SERVICE_COMPACTNESS'or service['record_digest']!=digest(record)or service['fresh_result_digest']!=digest(review)or any(service[k]['evidence'][1]['model_digest']!=mh for k in ('against362','against359')):raise ValueError('SERVICE365_CURRENT_PROOF_BINDING')
 n=out['nodes'];n['SERVICE_CIRCULATION']={'status':'PASS_SCOPED_SOURCE117_BATH_WC_CIRCULATION_RECONCILIATION','evidence':service,'scope':'Current balanced365 source117 bath/WC only, actual reviewed comparisons359/362. Not SERVICE_ANCHOR365 eligibility or full Q04.'}
 for u in n['Q12_PER_UNIT']['evidence']:
  if 'EXCLUSIVE_SERVICE_CIRCULATION_ACCOUNTING'in u['exact_pending']:u['exact_pending'].remove('EXCLUSIVE_SERVICE_CIRCULATION_ACCOUNTING')
 for k in ordered_dag():n[k]['depends_on']=DAG[k];n[k]['blocking_dependencies']=[d for d in DAG[k]if n[d]['status'].startswith('UNKNOWN')]
 if hashlib.sha256(path.read_bytes()).hexdigest()!=RUNNER_SHA or before!=digest([record,review]):raise ValueError('INPUT_OR_SOURCE_CHANGED')
 out['schema']='ROLE_REGISTRY_BALANCED365_V3_AUDITED_SERVICE_DEPENDENCY';return out
if __name__=='__main__':
 r=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text());v=json.loads((ROOT/'review365_balanced_source_validation/result.json').read_text());o=evaluate(r,v);Path(__file__).with_name('role_registry_on365_v3.json').write_text(json.dumps(o,indent=2));print({k:v['status']for k,v in o['nodes'].items()})
