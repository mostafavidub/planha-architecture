"""Reconstruction357, not recovery of historical353. Exact scoped applicability only."""
from fractions import Fraction
import hashlib,json

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def number(x):
 if type(x) not in (str,int):raise ValueError('EXACT_STRING_OR_INTEGER_REQUIRED')
 q=Fraction(x)
 if q<=0:raise ValueError('POSITIVE_REQUIRED')
 return q

def rliv_applicability(model,brief=None):
 out={'state':'UNKNOWN','reconstruction':357,'evidence':{'model_digest':digest(model)},'missing':[]}
 try:
  inputs=model['inputs'];w,l=number(inputs[0]),number(inputs[1])
  out['evidence']['dimensions']=[str(w),str(l)]
 except (KeyError,IndexError,TypeError,ValueError,ZeroDivisionError):
  out['missing']=['VALID_EXACT_INPUT_DIMENSIONS'];return out
 matched=sorted([w,l])==[Fraction('12.5'),Fraction(20)]
 if brief is None:
  out['state']='UNKNOWN' if matched else 'NOT_APPLICABLE'
  out['missing']=['BOUND_SIX_OPTION_BRIEF'] if matched else []
  out['evidence']['basis']='DIMENSION_SCOPE_ONLY_NOT_CONTRACT_ACCEPTANCE';return out
 if (type(brief) is not dict or set(brief)!={'model_hash','source_ref','requested_count'} or brief.get('model_hash')!=digest(model) or type(brief.get('requested_count')) is not int or brief['requested_count']!=6 or brief.get('source_ref') not in ['PRD'+str(i) for i in range(111,119)]):
  out['missing']=['VALID_BOUND_SOURCE_BRIEF'];return out
 out['state']='APPLIES' if matched else 'UNKNOWN'
 out['missing']=[] if matched else ['BRIEF_DIMENSION_CONFLICT']
 out['evidence']['brief']=brief.copy();return out
