"""357 reconstructed intrinsic sitting closure using recovered351 source kernel.
Author233 applicability has not yet been recovered: no whole-parent PASS here.
"""
from pathlib import Path
import hashlib,types,time
from common import rows,digest,registry_methods
from modules_spatial import rect,union_area,intersection,source_sweeps
ROOT=Path(__file__).resolve().parents[1];PATH=ROOT/'staging351_collision_lineage/fresh_bridge.py'
PIN='2775bf8998e6c2a4294c290e9a85073f5facb4ae24201674f559a09519ad6209'
def evaluate(envelope,result,groups,seconds=6):
 start=time.monotonic();out={'rule_id':'LIVING_USEFUL_CONTIGUITY','verdict':'UNKNOWN','parent_complete':False,'missing':[],'evidence':{}}
 def need(x,c):
  if not x:raise ValueError(c)
 try:
  need(type(seconds)in(int,float)and 0<seconds<=10,'BOUNDED_BUDGET')
  model=envelope['packet']['world_model'];rs=rows(model,result['raw_fresh_report']);mh=digest(model);before=digest([envelope,result,groups])
  need(result['candidate_digest']==digest(envelope),'CANDIDATE_BINDING');need(groups['model_hash']==mh and groups['fresh_result_digest']==digest(result),'GROUP_FRESH_BINDING')
  code=PATH.read_bytes();need(hashlib.sha256(code).hexdigest()==PIN,'RECOVERED351_SOURCE_PIN');bridge=types.ModuleType('_closure357_source351');bridge.__file__=str(PATH);exec(compile(code,str(PATH),'exec'),bridge.__dict__)
  bridge._group_sources285();methods=registry_methods();bridge._network_sources288();prereq=[]
  for rid in bridge.GROUP285_IDS:
   found=[g for g in groups['rows']if g.get('requirement_id')==rid];need(len(found)==1,'GROUP_INVENTORY');g=found[0];row=rs[rid]
   need(g['verdict']=='SCOPED_PASS'and row['status']=='PASS_LIMITED','SOURCE_SUBCONDITION:'+rid);need(g['row_hash']==digest(row)and g['witness_hash']==digest(row['evidence']['witness']),'SOURCE_ROW_BINDING');need(row['method']==methods[rid],'SOURCE_METHOD');prereq.append(g)
  from network387 import evaluate as network_evaluate
  network=network_evaluate(envelope,result,prereq,seconds-(time.monotonic()-start));need(network['verdict']=='SCOPED_PASS','SOURCE_NETWORK')
  cap=rs['fixture_inventory_use']['evidence']['witness']['capacity'];need(cap['errors']==[]and cap['pending']==[]and cap['evidence']['status']=='PASS_ACTUAL_INSTANCE_PLANAR_CAPACITY','SOURCE_CAPACITY');need(cap['evidence']['model_hash']==mh,'CAPACITY_MODEL')
  unitrows=[]
  for u in model['units']:
   role=u['spatial_role_bindings']['living_activity_group'];seats=u['public_program']['capacity']['living_seats'];ids=[s['fixture_id']for s in seats]
   need(len(ids)==len(set(ids))and set(ids)==set(role['fixture_ids']),'SOURCE_SITTING_INVENTORY');n=[r for r in network['rows']if r['unit']==u['id']];need(len(n)==1 and set(n[0]['targets'])==set(ids),'ALL_SOURCE_TARGETS')
   c=[r for r in cap['evidence']['units']if r['unit']==u['id']];need(len(c)==1 and c[0]['actual_places']['living_seats']>=c[0]['residents_study'],'SOURCE_REQUIRED_COUNT')
   need(set(role['activity_ids'])==set(role['access_route_ids']),'ACTIVITY_ACCESS_INVENTORY');sitting=[rect(u['fixtures'][k])for k in ids]+[rect(u['activities'][k])for k in role['activity_ids']]
   for a in sitting:
    for excluded in('dining','kitchen'):
     need(not any(intersection(a,rect(r))for r in u['rooms'][excluded]),'SITTING_ROLE_OVERLAP')
   access=[]
   for key in role['access_route_ids']:access+=source_sweeps(u['routes'][key],model['profile']['body_m'])
   whole=sitting+access
   # Whole union includes verified access sweeps, not bounding-box or residual.
   connected={0};pending=[0]
   while pending:
    i=pending.pop();a=whole[i]
    for j,b in enumerate(whole):
     if j not in connected and max(a[0],b[0])<=min(a[2],b[2])and max(a[1],b[1])<=min(a[3],b[3]):connected.add(j);pending.append(j)
   need(len(connected)==len(whole),'SOURCE_SITTING_ACCESS_DISCONNECTED')
   unitrows.append({'unit':u['id'],'required_residents':c[0]['residents_study'],'actual_sitting_places':c[0]['actual_places']['living_seats'],'sitting_activity_area_m2':str(union_area(sitting)),'sitting_access_union_area_m2':str(union_area(whole)),'connected':True,'source_body_m':model['profile']['body_m'],'residual_claimed':False})
  need(digest([envelope,result,groups])==before,'INPUT_MUTATION');bridge._group_sources285();bridge._network_sources288()
  out.update(verdict='PASS_SCOPED_INTRINSIC_LIVING',missing=['AUTHOR233_PARENT_SCOPE_AND_R_LIV_PROOF_PENDING_REVIEW'],evidence={'model_hash':mh,'base_fresh_digest':digest(result),'source_bridge_sha256':PIN,'network':network,'capacity':cap,'units':unitrows},scope='CURRENT_SOURCE_SITTING_PROGRAM_AND_ACCESS_ONLY_NOT_FULL_PARENT')
 except (ValueError,KeyError,TypeError,IndexError,AttributeError)as e:out['missing']=['CLOSURE_BLOCKED:'+str(e)]
 out['elapsed_seconds']=time.monotonic()-start;return out
