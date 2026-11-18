"""Actual apertures only. No daylight/ventilation/window-per-room evaluation."""
from copy import deepcopy
from core_wall_audit118 import q,inside,opening_hosts,output

def evaluate(m):
 view=deepcopy(m);view['concept_windows']=[]
 doors=opening_hosts(view);errors=[];pending=[];rows=[]
 if doors['status']=='FAIL':errors+=doors['witness'].get('errors',[])
 elif doors['status']!='PASS_LIMITED':pending+=doors['witness'].get('pending',['ACTUAL_DOOR_HOST_NOT_EVALUATED'])
 try:
  for w in m.get('concept_windows',[]):
   r=q(w['plan_rect']);host=q(m['walls'][w['host_wall_id']])
   if not inside(r,host):errors.append(w['id']+':ACTUAL_WINDOW_OUTSIDE_HOST')
   if w.get('floor_portal')is not False:errors.append(w['id']+':WINDOW_NOT_A_FLOOR_PORTAL')
   # Height order is geometry of an already modeled object, not clearance,
   # illuminance, ventilation sufficiency or a demand to create a window.
   from fractions import Fraction as F
   if not 0<=F(str(w['sill_m']))<F(str(w['head_m'])):errors.append(w['id']+':INVALID_ACTUAL_VERTICAL_EXTENT')
   rows.append({'id':w['id'],'host_wall_id':w['host_wall_id'],'actual_rect':w['plan_rect']})
 except(KeyError,ValueError,TypeError)as ex:errors.append('ACTUAL_OPENING_GEOMETRY_SCHEMA:'+str(ex))
 return output('H08/H18',errors,pending,{'door_apertures':doors,'existing_window_objects':rows,'lighting_and_ventilation':'EXCLUDED_BY_OWNER_SCOPE_NOT_EVALUATED','no_window_inventory_requirement':True,'export_parity':'SEPARATE_PRODUCT_STAGE'})
