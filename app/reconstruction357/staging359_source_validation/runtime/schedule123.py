"""Bounded source-program exploration, not architectural diversity proof."""
from fractions import Fraction as F
from contract114 import TRANS

def requested_count(raw):
 n=F(str(raw.get('requested_count',6)).translate(TRANS))
 if n.denominator!=1 or not 1<=n<=12:raise ValueError('REQUESTED_COUNT_INTEGER_1_TO_12_STUDY_LIMIT')
 return int(n)

def schedule(program):
 supported=[b for b in program['bedroom_choices'] if b in (1,2)]
 ordered=supported # preserve higher supported program before fallback
 # Opposite furnishing orientation before another same-orientation objective.
 return [{'bedrooms':b,'variant':v,'topology':top,'orientation':'horizontal'if v%2==0 else'vertical'}for top,v in [('KITCHEN_BATH_SHARED_SIDE',1),('SIDE_ROOTED_SERVICES',2),('SIDE_ROOTED_SERVICES',1),('KITCHEN_BATH_SHARED_SIDE',2),('SIDE_ROOTED_SERVICES',0),('KITCHEN_BATH_SHARED_SIDE',0)]for b in ordered]

def bind_runtime(program,attempts):
 p=dict(program)
 p['program_order_basis']='HIGHER_SUPPORTED_SOURCE_PROGRAM_FIRST; fallback is an alternative, not capacity adequacy proof'
 p['runtime_supported_bedroom_counts']=sorted({a['bedrooms']for a in attempts})
 p['scheduled_program_variants']=attempts
 p['unscheduled_programs']=[{'bedrooms':b,'reason':'NO_COMPLETE_RUNTIME_TOPOLOGY_FOR_THIS_PROGRAM','not_infeasible':True}for b in p['bedroom_choices']if b not in p['runtime_supported_bedroom_counts']]
 p['limits']=['Actual scheduled program/variant pairs are listed; enumeration is a finite engineering budget, not domain coverage.', 'Only independently gated complete sleep/living/dining/clothing/daily-use programs may be admitted. Three-bedroom runtime topology is not integrated.', 'Requested count is a target, not a promised admission count. Geometry inequality is not independently verified architectural diversity.', 'Remaining floor is not proven useful living area; no overall quality or optimality claim.']
 return p
