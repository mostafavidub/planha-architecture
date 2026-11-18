"""Immutable artifact inventory + measured geometry, no receipt acceptance."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'semantic_rules357'))
from comparison_metrics import digest,measure_model

def build():
 out={'schema':'FINITE358_ARTIFACT_LEDGER_PENDING_MINIMA','rule_acceptance':False,'global_optimum':False,'closed_applicable_comparison':False,'members':[]}
 for ident,path,selector in [('baseline351','actual_run/actual_response.json','selected0'),('translated357','staging357_comparative/attached_service_final357.json','candidate'),('row358','staging358_comparative/row_candidate358.json','candidate')]:
  p=ROOT/path;x=json.loads(p.read_text());c=x['selected'][0] if selector=='selected0'else x['candidate'];m=c['model'] if 'model'in c else c['packet']['world_model']
  out['members'].append({'id':ident,'artifact':path,'artifact_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'candidate_digest':digest(c),'model_digest':digest(m),'request':c.get('request'), 'metrics':measure_model(m),'terminal_state':'UNKNOWN_EVIDENCE','reason':'INTRINSIC_PLANAR_FUNCTIONAL_MINIMA_NOT_YET_BOUND_TO_LEDGER','not_excluded':True})
 out['unconstructed_branches']=[{'id':'source114_full_band_core','terminal_state':'UNKNOWN_EVIDENCE','reason':'SOURCE_PRIMITIVE_OWNERSHIP_COUNTEREXAMPLE_NOT_YET_RECOMPUTED','not_excluded':True}]
 out['missing']=['FIXED_INTRINSIC_MINIMA_REGISTRY','PER_UNIT_SCENARIO_PROTECTED_FUNCTIONAL_METRICS','EXCLUSIVE_CIRCULATION_COMPONENT_DESTINATION_INVENTORY','PRIVATE_GROUP_TARGET_ROUTE_METRICS','SERVICE_EXCLUSIVE_CIRCULATION_ROLES','SOURCE114_FULL_BAND_BRANCH_PROOF']
 return out
if __name__=='__main__':
 p=Path(__file__).with_name('ledger_actual358.json');p.write_text(json.dumps(build(),ensure_ascii=False,indent=2));print(p)
