"""Budgeted profiles, not guaranteed organizations or six admitted layouts."""
from itertools import combinations_with_replacement
BUDGET={'max_solver_calls':8,'solver_seconds_per_call':3,'search_checkpoint_seconds':26,'max_full_gates':8,'validation_checkpoint_seconds':100,'total_checkpoint_seconds':135,'scope':'Start checkpoints; complete each independent gate before admission. Not a hard interruptible time guarantee.'}
def schedule():
 return [{'family':f,'bedrooms':b,'variant':v,'organization_profile':org,'topology':'FRAME125_SERVICE_SIDE'if f=='LEFT_RIGHT'else'KITCHEN_BATH_SHARED_SIDE'} for b,v,org in [(2,1,'UNRESTRICTED'),(1,1,'UNRESTRICTED'),(1,2,'UNRESTRICTED'),(1,1,'PRIVATE_CORE_SIDE')] for f in ('FRONT_REAR','LEFT_RIGHT')]
def pairs(labels):return list(combinations_with_replacement(labels,2))
