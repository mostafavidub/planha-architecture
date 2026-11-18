"""Versioned finite evidence inventory; statuses come from callbacks, never flags."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'finite_comparison365'),str(ROOT/'semantic_rules357')]
from q04_closure365_v7 import compare,digest
MEMBERS=(('baseline351','actual_run/actual_response.json'),('translated357','staging357_comparative/attached_service_final357.json'),('row358','staging358_comparative/row_candidate358.json'),('clamped359','staging359_hall_clamp/actual359.json'),('notched362','staging362_core_notch/actual362.json'),('balanced365','staging365_balanced_portals/actual365.json'),('service365','staging365_service_grammar/candidate365.json'),('joint367','review367_joint_attempt2/actual367.json'))
def model_of(name,record):return record['selected'][0]if name=='baseline351'else record['candidate']
def inventory(current_record,current_id):
 current=current_record['candidate'];rows=[]
 if current_id not in {n for n,p in MEMBERS}:raise ValueError('UNREGISTERED_CURRENT_ID')
 for name,path in MEMBERS:
  p=ROOT/path;record=json.loads(p.read_text());candidate=model_of(name,record)
  if name==current_id and digest(record)!=digest(current_record):raise ValueError('CURRENT_ARTIFACT_MISMATCH')
  if candidate['request']!=current['request']or candidate['model']['program']!=current['model']['program']or candidate['model']['profile']!=current['model']['profile']:raise ValueError('COHORT_BRIEF_PROGRAM_PROFILE_CHANGED:'+name)
  row={'id':name,'path':path,'artifact_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'record_digest':digest(record),'model_digest':digest(candidate['model']),'role':'CURRENT'if name==current_id else'ALTERNATIVE','eligibility':'PENDING_OWN_CALLBACK_NOT_A_STORED_FLAG','comparison':None if name==current_id else compare(current['model'],candidate['model'])}
  rows.append(row)
 return {'members':rows,'finite_scope':'Registered current source variants only; full domain dispatcher/selector lineage still required; not all continuous parameters.','domain_closed':False,'accepted':False,'selection_set_dependency':'Any final selected pair containing balanced365 and joint367 requires balanced365 reevaluation against joint367 as well. Prior balanced365 Q04 receipt remains historical, not automatically valid for expanded cohort.'}
def evaluate_geometric_inventory():
 r=json.loads((ROOT/'review367_joint_attempt2/actual367.json').read_text());b=json.loads((ROOT/'staging365_balanced_portals/actual365.json').read_text())
 return {'schema':'FINITE_COHORT367_PRE_GATE_GEOMETRY','current367':inventory(r,'joint367'),'balanced365_recheck':inventory(b,'balanced365'),'new_fresh_execution':False,'verdict':'UNKNOWN_PENDING_OWN_GATES_ROLES_PROTECTION'}
if __name__=='__main__':
 x=evaluate_geometric_inventory();p=Path(__file__).with_name('cohort_preflight_actual367.json');assert not p.exists();p.write_text(json.dumps(x,indent=2));print(x['verdict'])
