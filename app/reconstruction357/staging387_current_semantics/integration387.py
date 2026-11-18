"""Balanced member semantic entrypoint for the supervised387 pipeline."""
from gate387 import configure,load_inputs,verify_end,views,ROOT,D
from frozen387 import module

def run_member(folder,expected):
 configure(folder,expected)
 from extended387 import run
 from qualification387 import qualify,RULES
 i=load_inputs();record,fresh=i['record'],i['fresh'];roles=run(record,fresh);joined=None;raw_join=None;errors={}
 if 'cohort'in roles['evidence']:
  try:
   raw_join=module(ROOT/'staging386_view_binding/final_join386.py','_current387_final_join386').join(record,fresh,roles,roles['evidence']['cohort'],views(record,fresh))
   sealing=module(ROOT/'staging387_current_semantics/semantic_seal387.py','_current387_semantic_seal')
   joined=sealing.seal_current(record,fresh,roles,raw_join)
  except Exception as error:errors['role_join']=type(error).__name__+':'+str(error)
 try:q=qualify(record,fresh,roles,joined)
 except Exception as error:
  errors['qualification']=type(error).__name__+':'+str(error)
  q={'qualified':False,'parent_verdicts':{k:'UNKNOWN'for k in RULES},'q12_verdict':'UNKNOWN','cohort_closed':False,'missing':['CURRENT_QUALIFICATION_BINDING_OR_PREREQUISITE_FAILURE',errors['qualification']]}
 end=verify_end()
 if end!=roles['binding']:raise ValueError('POST_SEMANTIC_BINDING_CHANGED')
 from gate387 import _load_all
 member_binding=_load_all()['binding']
 return {'schema':'SAME_RUN387_BALANCED_SEMANTIC_QUALIFICATION','binding':member_binding,'semantic_binding':end,'qualification':q,'roles':roles,'raw_role_join':raw_join,'role_join':joined,'errors':errors,
         'role_evidence_digest':D(roles),'role_join_digest':D(joined)if joined is not None else None,'same_pipeline_run_semantic_execution':True,
         'current_essential_and_role_kernels_recomputed':True,'fresh_checker_executed_by_semantic_phase':False,'accepted':False,'delivery_allowed':False}
