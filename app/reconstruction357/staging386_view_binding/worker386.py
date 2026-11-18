import json,sys,time
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;W=R.parent;P=Path(sys.argv[1]);start=time.monotonic()
sys.path.insert(0,str(R/'staging381_role_semantics'))
from gate381 import load_inputs,validate,views,D
from final_join386 import join
try:
 i=load_inputs();r,f=i['record'],i['fresh'];binding=validate(r,f);v=views(r,f)
 roles=json.loads((W/'review381_actual_v1/result.json').read_text());prior=json.loads((W/'review384_actual_v1/result.json').read_text());cohort=prior['evidence']['cohort']
 if roles['binding']!=binding or prior['rank1_binding']!=binding:raise ValueError('STORED_ACTUAL_BINDING')
 if cohort['binding']['record_digest']!=D(r)or cohort['binding']['fresh_digest']!=D(f):raise ValueError('STORED_COHORT_BINDING')
 result=join(r,f,roles,cohort,v)
 out={'schema':'PURE_VIEW_BINDING_JOIN386','binding':binding,'join':result,'roles_source_digest':D(roles),'cohort_source_digest':D(cohort),'prior384_result_digest':D(prior),'new_intrinsic':False,'new_comparison':False,'new_fresh':False,'new_candidate':False,'same_run_semantic_execution':False,'accepted':False,'delivery_allowed':False,'request_fulfilled':False,'seconds':time.monotonic()-start}
 (P/'result.json').write_text(json.dumps(out,indent=2))
except Exception as e:
 (P/'error.json').write_text(json.dumps({'error':type(e).__name__+':'+str(e),'seconds':time.monotonic()-start}));raise
