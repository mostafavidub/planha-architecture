"""Reconstructed357 current-measurement adapter; no copied historical verdicts."""
from comparison_metrics import measure_model,digest
RULES={'CIRCULATION_NECESSITY':['VALIDATED_FINITE_ALTERNATIVES','CIRCULATION_COMPONENT_PURPOSES','MATCHED_FUNCTIONAL_SCENARIOS'],'SERVICE_COMPACTNESS':['EXCLUSIVE_SERVICE_CIRCULATION_ROLE','VALIDATED_SAME_PROGRAM_FUNCTIONAL_BASELINE'],'COMMON_CORE_COMPACTNESS':['CORE_STAGING_FUNCTION','VALIDATED_COMPACT_CORE_ALTERNATIVE'],'KITCHEN_PROXIMITY':['SOURCE_OPERATION_AND_GUEST_PRIVATE_RELATION_CLOSURE'],'DISTINCTNESS_AND_FAIRNESS':['PER_UNIT_FUNCTIONAL_FAIRNESS','SOURCE_SELECTION_SET_APPLICABILITY']}
def evaluate(model,report):
 from common import rows
 out={k:{'verdict':'UNKNOWN','codes':['SEMANTIC_COMPARATIVE_OBLIGATIONS_UNPROVEN'],'missing':list(v),'evidence':{},'model_digest':digest(model)}for k,v in RULES.items()}
 try:rs=rows(model,report);m=measure_model(model)
 except(ValueError,TypeError,KeyError)as e:
  for v in out.values():v['codes']=['BOUND_MEASUREMENT_FAILED',str(e)]
  return out
 for k,v in out.items():
  v['measured']=m['common']if k=='COMMON_CORE_COMPACTNESS'else m['units'];v['measurement_scope']=m['scope']
  v['evidence']={'bound_source_requirement_ids':sorted(rs),'raw_digest':digest(report)}
 # No selected-set receipt is available in this single-candidate API. Pairwise
 # ranking is unassessed, not an excuse to waive per-unit fairness.
 out['DISTINCTNESS_AND_FAIRNESS']['scope']='SINGLE_CANDIDATE_NOT_SELECTION_SET_PROOF'
 return out
