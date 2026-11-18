"""Scoped dead-end counterexample candidate, pending independent audit.
No geometry edits, global infeasibility or invented source-purpose claim.
"""
import ast,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from common import digest
from modules_spatial import rect,intersection,difference,union_area
from circulation_role358 import evaluate as circulation,ROOT

def operation_bounds(model):
 path=ROOT/'planha_general150_runtime_work/world_transform125.py';data=path.read_bytes()
 if hashlib.sha256(data).hexdigest()!='fa301aadbf7cf006bc030464cf6ad8ed34d13f7347a20ccad69a7838e6f40b55':raise ValueError('SOURCE_GEOMETRY_KEYS_PIN')
 ns={};tree=ast.parse(data)
 for n in tree.body:
  if isinstance(n,ast.Assign)and all(isinstance(t,ast.Name)and t.id.endswith('_KEYS')for t in n.targets):exec(compile(ast.Module(body=[n],type_ignores=[]),str(path),'exec'),ns)
 out=[];body=F(model['profile']['body_m'])
 for kind,ops in model['operations'].items():
  for idx,op in enumerate(ops):
   points=[];radii=[body/2]
   def walk(x,key=''):
    if key in('module','source_contract','canonical_isometry','canonical_transform'):return
    if isinstance(x,dict):
     for k,v in x.items():
      if k in('leaf_radius_m','leaf_half_thickness_m','object_half_size_m'):
       try:radii.append(F(v))
       except(ValueError,TypeError):raise ValueError('OPERATION_RADIUS')
      walk(v,k)
    elif isinstance(x,list):
     if key in ns['RECT_KEYS']and len(x)==4 and not isinstance(x[0],(list,dict)):
      a,b,c,d=rect(x);points.extend([(a,b),(c,d)])
     elif key in ns['POINT_KEYS']and len(x)==2 and not isinstance(x[0],(list,dict)):points.append(tuple(map(F,x)))
     elif key in ns['RECT_LIST_KEYS']:
      for r in x:
       a,b,c,d=rect(r);points.extend([(a,b),(c,d)])
     elif key in ns['PATH_KEYS']:
      points.extend(tuple(map(F,p))for p in x)
     else:
      for v in x:walk(v)
   walk(op)
   if not points:raise ValueError('OPERATION_WITHOUT_GEOMETRY')
   pad=sum(radii);q=(min(x for x,y in points)-pad,min(y for x,y in points)-pad,max(x for x,y in points)+pad,max(y for x,y in points)+pad)
   out.append({'kind':kind,'index':idx,'source_operation_digest':digest(op),'conservative_bounds':list(map(str,q)),'scope':'All source geometry fields plus body/radius padding. May overexclude but never grants function from empty bbox.'})
 return out

def evaluate(record,review):
 intrinsic=circulation(record,review);m=record['candidate']['model'];ops=operation_bounds(m);out={'schema':'Q04_DEAD_END_CANDIDATE358_PENDING_AUDIT','model_hash':digest(m),'record_digest':digest(record),'review_digest':digest(review),'circulation_digest':digest(intrinsic),'rows':[],'verdict':'UNKNOWN_NO_CURRENT_SOURCE_PURPOSE_WITNESS','admission_allowed':False,'geometry_mutated':False}
 body=F(m['profile']['body_m'])
 for u in intrinsic['units']:
  for branch in u['untargeted_terminal_extensions']:
   q=rect(branch['geometry']);connections=branch['only_floor_connection'];axis=connections[0]['axis'];at=F(connections[0]['coordinate'])
   if any(c['axis']!=axis or F(c['coordinate'])!=at for c in connections):raise ValueError('SINGLE_MOUTH_REQUIRED')
   reserve=list(q)
   if at==q[axis]:reserve[axis+2]=min(q[axis+2],at+body)
   elif at==q[axis+2]:reserve[axis]=max(q[axis],at-body)
   else:raise ValueError('MOUTH_NOT_AT_END')
   reserve=tuple(reserve);proposed_distal=difference([q],[reserve]);op_hits=[{**o,'intersection':[list(map(str,z))for a in proposed_distal if(z:=intersection(a,rect(o['conservative_bounds'])))]}for o in ops];op_hits=[o for o in op_hits if o['intersection']];distal=difference(proposed_distal,[rect(o['conservative_bounds'])for o in op_hits])
   out['rows'].append({'unit':u['unit'],'branch':branch,'conservative_turning_reserve':list(map(str,reserve)),'turning_depth_source_body_m':str(body),'operation_envelopes_excluded':op_hits,'distal_no_current_witness_regions':[list(map(str,q))for q in distal],'distal_no_current_witness_area_m2':str(union_area(distal)),'predicate_status':'CANDIDATE_NO_PURPOSE_AFTER_CONSERVATIVE_RESERVE_PENDING_AUDIT'if distal else'UNKNOWN_NO_POSITIVE_COUNTEREXAMPLE','source_profile_closed_inventory':'Same fresh actual required activities, targets, all portals, checked body/scenario routes and fixed operation inventory; hypothetical standing is not a required destination.','assumption':'One full source-body depth at branch mouth is retained conservatively for planar maneuver, plus every conservative operation envelope. Must be audited against Q04 source before FAIL authority.'})
 out['independent_audit_limit']='Source body size is not an authoritative maximum maneuver/staging depth. Positive distal witness is absence of current required-path/activity evidence, not universal uselessness. A source-supported shortened alternative must preserve all applicable function before necessity rejection; no FAIL authority granted.'
 out['operator_plan']={'operator':'CLAMP_SOURCE_HALL_TERMINAL_EXTENTS_TO_REQUIRED_PORTAL_OPERATION_ENVELOPE','parameters':'Derive interval from full actual source portal/body/operation inventory and conservative turning reserve; no coordinate tuning or fixture shrinking.','preserved':['raw dimensions and occupants','all private room modules and source fixtures','all required ports and operational envelopes','connected source-body circulation','source wall profile and source opening operation','previous candidate and proof history'],'rebuild':'Regenerate hallway solids/domains/private paths, then rebuild all dependent model roles and provenance through a new producer version. Never relabel old tail useful or patch accepted model.','mandatory_rechecks':'Actual source replay, H08 all targets, source door/closet operations, partition/wall continuity, privacy, whole role extent, all parent rules with new hashes.','execution_state':'PLAN_ONLY_NO_OPERATOR_EXECUTED_NO_NEW_FRESH'}
 return out
if __name__=='__main__':
 r=json.loads((ROOT/'staging358_comparative/row_candidate358.json').read_text());v=json.loads((ROOT/'review358_source_validation/result.json').read_text());o=evaluate(r,v);Path(__file__).with_name('dead_end_predicate_actual358.json').write_text(json.dumps(o,indent=2));print([(r['unit'],r['distal_no_current_witness_area_m2'],len(r['operation_envelopes_excluded']))for r in o['rows']])
