"""Own-source finite measurement, not Q04 closure or comparison eligibility."""
import json,hashlib
from pathlib import Path
from q04_closure365_v7 import objective,compare,ROOT,digest
from group_readsets_service365 import build

def evaluate(record,review):
 view=build(record,review,source_profile='SOURCE_SERVICE365');m=record['candidate']['model'];values,bindings=objective(m);pairs=[]
 for name,path in [('baseline351','actual_run/actual_response.json'),('translated357','staging357_comparative/attached_service_final357.json'),('row358','staging358_comparative/row_candidate358.json'),('clamped359','staging359_hall_clamp/actual359.json'),('notched362','staging362_core_notch/actual362.json'),('balanced365','staging365_balanced_portals/actual365.json')]:
  p=ROOT/path;r=json.loads(p.read_text());c=r['selected'][0]if name=='baseline351'else r['candidate']
  if c['request']!=record['candidate']['request']or c['model']['program']!=m['program']or c['model']['profile']!=m['profile']:raise ValueError('SAME_BRIEF_PROGRAM_PROFILE')
  pairs.append({'id':name,'path':path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'model_digest':digest(c['model']),'comparison':compare(m,c['model']),'protected_eligibility':'NOT_REASSESSED_BY_THIS_MEASUREMENT'})
 return {'schema':'SERVICE_CANDIDATE365_FINITE_OBJECTIVE_MEASUREMENT','source_profile':'SOURCE_SERVICE365','record_digest':digest(record),'fresh_result_digest':digest(review),'model_digest':digest(m),'group_digest':digest(view['groups']),'objectives':{k:str(v)for k,v in values.items()},'common_bindings':bindings,'pairs':pairs,'verdict':'UNKNOWN','remaining':['OWN_PRIVATE_BRANCH_TAIL_NECESSITY','OWN_WHOLE_COMMON_ROLE','OWN_FINITE_COMPARATIVE_PROTECTION_AND_BRANCH_CLOSURE'],'accepted':False,'new_fresh_execution':False,'note':'Known worse alternative dimensions refute dominance only; no positive eligibility or complete purpose inferred. V365 post-observation engineering objectives, not continuous global optimum.'}
if __name__=='__main__':
 r,f=[json.loads((ROOT/p).read_text())for p in ['staging365_service_grammar/candidate365.json','review365_service_source_validation/result.json']];out=evaluate(r,f);p=Path(__file__).with_name('service_candidate_objectives_actual365.json');assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2));print(out['verdict'])
