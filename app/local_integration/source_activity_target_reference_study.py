"""Activity-center target references and stored-route endpoints only.
No route generation, obstacle/width checking, provenance or architecture acceptance.
"""
from source_wall_record_contract_study import header,coordinate,rectangle,need
from declared_geometry_projection_study import digest
def point(p):
 need(type(p)is list and len(p)==2,'POINT_SHAPE');return list(map(coordinate,p))
def assess(model,expected_model_digest):
 out={'schema':'ACTIVITY_TARGET_ROUTE_REFERENCE_STUDY_V1','state':'INVALID_TARGET_REFERENCE','model_digest':expected_model_digest,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'origin_verified':False,'route_geometry_verified':False,'not_checked':['ACTIVITY_SOURCE_COMPLETENESS','BODY_CLEARANCE_OBSTACLES_AND_SCENARIOS','FAILURE_REASON_TRUTH','SCENARIO_ROUTES','ENTRY_ENDPOINT','WHOLE_EVALUATOR']}
 try:
  header(model,expected_model_digest);rows=[]
  failures=model['route_failures'];need(type(failures)is list,'FAILURE_LEDGER_TYPE')
  for u in model['units']:
   acts=u['activities'];targets=u['route_targets'];routes=u['routes']
   need(type(acts)is dict and bool(acts) and type(targets)is dict and set(acts)==set(targets),'ACTIVITY_TARGET_KEYSET')
   need(type(routes)is dict and set(routes)<=set(targets)|{'kitchen'},'ROUTE_REFERENCE_KEYSET')
   if 'kitchen'in routes:
    need('kitchen_work'in routes and digest(routes['kitchen'])==digest(routes['kitchen_work']),'KITCHEN_ROUTE_ALIAS')
   for aid,q in acts.items():
    need(type(aid)is str and bool(aid),'ACTIVITY_ID')
    a,b,c,d=rectangle(q);target=point(targets[aid])
    need(target==[(a+c)/2,(b+d)/2],'ACTIVITY_CENTER_TARGET')
    matched=[f for f in failures if type(f)is dict and f.get('unit')==u['id'] and f.get('route')==aid]
    path=routes.get(aid)
    if aid in routes:
     need(type(path)is list and bool(path),'NONEMPTY_STORED_PATH')
     pts=[point(p)for p in path];need(pts[-1]==target,'ROUTE_TARGET_ENDPOINT')
     state='STORED_PATH_REFERENCE_BOUND_NOT_GEOMETRY_CHECKED'
    else:state='MISSING_PATH_WITH_MATCHED_LEDGER_RECORD' if matched else 'MISSING_PATH_WITHOUT_FAILURE_RECORD'
    rows.append({'unit':u['id'],'activity_id':aid,'target_digest':digest(targets[aid]),'stored_path_digest':digest(path)if aid in routes else None,'evidence_state':state,'matched_failure_count':len(matched),'matched_failure_digests':[digest(f)for f in matched],'matched_reason_text_present':[type(f.get('reason'))is str and bool(f['reason'])for f in matched],'architectural_effect':'UNKNOWN_NOT_ROUTE_GEOMETRY_VERDICT'})
  need(digest(model)==expected_model_digest,'INPUT_MUTATION')
  out.update(state='ACTIVITY_TARGET_REFERENCES_BOUND_ONLY',bindings=rows,original_failure_ledger_digest=digest(failures))
 except (ValueError,TypeError,KeyError,IndexError,UnicodeError,OverflowError,RecursionError) as ex:out.update(error=str(ex),error_type=type(ex).__name__)
 return out
