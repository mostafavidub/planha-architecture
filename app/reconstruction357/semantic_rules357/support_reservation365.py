"""Exact role-ledger reconciliation; operational reserve adds no usable area.
It never grants a parent verdict. Independent reservation scope audit precedes
registry adoption. No epsilon, area threshold or label-only coverage is used.
"""
from fractions import Fraction as F
from modules_spatial import rect,intersection,difference,union_area
from common import digest

def reconcile(support,reservation):
 if support['model_hash']!=reservation['model_hash']:raise ValueError('RESERVATION_SUPPORT_MODEL_BINDING')
 out=[]
 for row in support['rows']:
  gap=list(map(rect,row['unresolved_regions']));rs=[r for r in reservation['reservations']if r['unit']==row['unit']];regions=list(map(lambda r:rect(r['region']),rs))
  if any(r['classification']!='ENGINEERING_OPERATIONAL_SEPARATION_RESERVATION_NOT_USABLE_LIVING'or r['usable_floor_capacity_increment']!=0 for r in rs):raise ValueError('NONUSABLE_RESERVATION_CLASSIFICATION_REQUIRED')
  if difference(regions,gap):raise ValueError('RESERVATION_CLAIMS_EXTRA_OR_ALREADY_ACCOUNTED_FLOOR')
  remaining=difference(gap,regions)
  out.append({'unit':row['unit'],'original_source_functional_coverage_m2':row['body_plus_source_function_coverage_m2'],'original_unresolved_area_m2':str(union_area(gap)),'nonusable_operational_reservation_area_m2':str(union_area(regions)),'remaining_unresolved_area_m2':str(union_area(remaining)),'remaining_regions':[list(map(str,r))for r in remaining],'reservation_ids':[digest(r)for r in rs],'usable_floor_capacity_increment':0,'floor_role_accounting_only':True,'scope':'Reservation is separately nonusable operational margin, not additional seating or usable living floor.'})
 return {'model_hash':support['model_hash'],'support_digest':digest(support),'reservation_digest':digest(reservation),'rows':out,'unresolved_positive_extent':any(F(r['remaining_unresolved_area_m2'])>0 for r in out),'parent_complete':False,'admission_allowed':False}
