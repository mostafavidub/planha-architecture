"""Claim-boundary declarations only. Never proves any technical property."""
import hashlib,json
EXPECTED={'kind':'CONCEPT_DRAFT_ONLY','technical_approval':False,'legal_approval':False,'daylight_ventilation_scope':'EXCLUDED_FROM_MVP_NOT_EVALUATED','vertical_core_certified':False,'opening_rights':'UNVERIFIED','execution_ready':False}
def claim_boundary(model):
 d=model.get('scope_declaration');errors=[];pending=[]
 if d is None:pending.append('CANONICAL_SCOPE_DECLARATION_MISSING')
 elif not isinstance(d,dict):errors.append('SCOPE_DECLARATION_SCHEMA')
 else:
  for k,v in EXPECTED.items():
   if k not in d:pending.append('SCOPE_DECLARATION_MISSING:'+k)
   elif type(d[k])is not type(v)or d[k]!=v:errors.append('UNSUPPORTED_APPROVAL_CLAIM:'+k)
  # Reject contradictory approval assertions, not physical light/ventilation.
  for k in ('daylight_sufficiency','ventilation_sufficiency'):
   if k in d and d[k] is not False:errors.append('CONTRADICTORY_EXCLUDED_SCOPE_CLAIM:'+k)
 if model.get('accepted')is not False or model.get('release_allowed')is not False:errors.append('CANONICAL_ACCEPTANCE_CLAIM')
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_LIMITED','witness':{'declaration':d,'errors':errors,'pending':pending,'model_sha256':hashlib.sha256(json.dumps(model,sort_keys=True,separators=(',',':')).encode()).hexdigest()},'scope':'Checks only explicit pre-render absence of technical/legal/vertical-core/execution approval claims and owner-excluded MVP scope declaration. Does not verify those properties or visible warnings in files/UI; post-export display audit remains required.'}
