"""One stored-artifact rank2 intrinsic pass plus exact comparison and rank1 role join."""
import sys,json,time
from pathlib import Path
from gate384 import HERE,ROOT,D,load_inputs,validate
sys.path[:0]=[str(HERE),str(ROOT/'semantic_rules357'),str(ROOT/'staging378_finite_portals'),str(ROOT/'finite_comparison358'),str(ROOT/'staging381_role_semantics')]
def run(record,fresh):
 start=time.monotonic();binding=validate(record,fresh);before=D([record,fresh]);e={};errors={}
 from adapters384 import audit_loaded
 audit_loaded()
 import common
 common.REGISTRY_NAME='method_registry_source365.json'
 from eligibility384 import evaluate
 e['rank2_intrinsic']=evaluate(record,fresh,seconds=30)
 from gate381 import load_inputs as rank1_inputs,validate as rank1_validate
 i=rank1_inputs();r,f=i['record'],i['fresh'];b=rank1_validate(r,f)
 roles=json.loads((ROOT.parent/'review381_actual_v1/result.json').read_text());historical=json.loads((ROOT.parent/'review382_actual_v1/result.json').read_text())
 if roles['binding']!=b or historical['binding']!=b:raise ValueError('STORED_RANK1_CURRENT_BINDING')
 intrinsic=roles['evidence']['essential']['evidence']['intrinsic_eligibility']
 from cohort384 import compare_registered
 try:e['cohort']=compare_registered(r,f,intrinsic,record,fresh,e['rank2_intrinsic'],historical)
 except Exception as ex:errors['cohort']=type(ex).__name__+':'+str(ex)
 from final_join384 import join
 if 'cohort'in e:
  try:e['rank1_role_join']=join(r,f,roles,e['cohort'])
  except Exception as ex:errors['rank1_role_join']=type(ex).__name__+':'+str(ex)
 origins=audit_loaded();validate(record,fresh)
 if before!=D([record,fresh]):raise ValueError('INPUT_MUTATION')
 return {'schema':'ACTUAL383_RANK2_INTRINSIC_AND_CURRENT379_FINITE_JOIN384','binding':binding,'rank1_binding':b,'evidence':e,'errors':errors,'source_module_origins':origins,'rank2_intrinsic_recomputed':True,'rank1_roles_recomputed':False,'rank1_roles_source_digest':D(roles),'rank1_historical_cohort_source_digest':D(historical),'same_run_semantic_execution':False,'new_fresh':False,'candidate_constructed':False,'accepted':False,'delivery_allowed':False,'request_fulfilled':False,'seconds':time.monotonic()-start}
