"""Current joint9 + exact old readsets + new explicit finite-cohort derivation."""
import json,sys,copy
from pathlib import Path
from contract385 import ROOT,W,validate_member_folder,digest
RULES=('SPACE_ACCOUNTING','GUEST_ROUTE_INDEPENDENCE','LIVING_USEFUL_CONTIGUITY','CIRCULATION_NECESSITY','ROOM_PROGRAM_CAPACITY','BEDROOM_GROUPING','SERVICE_COMPACTNESS','COMMON_CORE_COMPACTNESS','PRIVACY_WITHOUT_FAKE_BAFFLE','OPENINGS_REAL','KITCHEN_PROXIMITY')
def run_member(folder,expected):
 folder=Path(folder);i=validate_member_folder(folder,expected);record,fresh,binding=i['record'],i['fresh'],i['binding'];before=digest(i)
 out={'schema':'SAME_RUN385_JOINT_SEMANTIC_DERIVATION','binding':binding,'current_nine_recomputed':False,'same_pipeline_run_semantic_execution':True,'old_role_geometry_recomputed':False,'accepted':False,'delivery_allowed':False}
 try:
  sys.path.insert(0,str(ROOT/'staging368_semantic_bridge'))
  from equivalence import compare
  from predicates import evaluate
  ref=json.loads((ROOT/'staging368_semantic_bridge/reference_registry.json').read_text());spec=ref['members']['joint']
  oldr=json.loads((ROOT/spec['paths']['record']).read_text());oldf=json.loads((ROOT/spec['paths']['fresh']).read_text())
  eq=compare(oldr,oldf,record,fresh);groups=evaluate(record,fresh,'joint',ref,seconds=8)
  out.update(current_nine_recomputed=True,current_groups=groups,exact_readset_equivalence=eq)
  b=validate_member_folder(folder.parent/'balanced',expected,require_physical_pass=True)
  bsem=json.loads((folder.parent/'balanced/semantic.json').read_text())
  rank1={**b,'semantic':bsem,'folder':str(folder.parent/'balanced')}
  from joint_composition385 import compose,load_rank2_bundle
  result=compose(record,fresh,binding,groups,eq,rank1,load_rank2_bundle())
  out.update(composition=result,qualification=result['qualification'])
 except Exception as error:
  out.update(qualification={'qualified':False,'parent_verdicts':{r:'UNKNOWN'for r in RULES},'q12_verdict':'UNKNOWN','cohort_closed':False,'missing':[type(error).__name__+':'+str(error)]})
 end=validate_member_folder(folder,expected)
 if digest(end)!=before:raise ValueError('JOINT_SEMANTIC_INPUT_CHANGED')
 return out
