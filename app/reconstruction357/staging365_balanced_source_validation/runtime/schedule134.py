"""Finite same-program search schedule; neither proposals nor pairs imply diversity."""
from itertools import combinations_with_replacement
BUDGET={'max_solver_calls':8,'solver_seconds_per_call':3,'search_checkpoint_seconds':26,'max_full_gates':8,'validation_checkpoint_seconds':100,'total_checkpoint_seconds':135,'scope':'Start checkpoints, not hard interruption; count actual propose invocations, including early bound rejection.'}
def schedule():
 # Preserve existing profiles and relative order; place the reviewed alternative
 # immediately after baseline one-bedroom LEFT_RIGHT, before objective variant2.
 rows=[]
 for b,v,org in [(2,1,'COMPACT_FUNCTIONAL_CLUSTER'),(2,1,'UNRESTRICTED'),(1,1,'UNRESTRICTED'),(1,2,'UNRESTRICTED')]:
  for family in ('FRONT_REAR','LEFT_RIGHT'):
   rows.append({'family':family,'bedrooms':b,'variant':v,'organization_profile':org,'topology':'FRAME125_SERVICE_SIDE'if family=='LEFT_RIGHT'else'KITCHEN_BATH_SHARED_SIDE'})
   if b==1 and v==1 and family=='LEFT_RIGHT':
    rows.append({'family':family,'bedrooms':1,'variant':1,'organization_profile':'PRIVATE_CORE_SIDE','topology':'FRAME125_SERVICE_SIDE'})
 return rows

def pairs(labels):return list(combinations_with_replacement(labels,2))
