"""Mandatory source-backed Q11 completeness gate, not a new quality metric.
No positive functional-boundary evaluator has yet been implemented. Hence no
producer flag, room label, privacy certificate or absent screen ID can admit Q11.
This is NOT a claim that all walls are forbidden or all plots infeasible.
"""
import json,hashlib
from pathlib import Path
SOURCE_SHA='b467c36e2b458e7d677cbe6d9d77dfd02349e333115dedc03739e0cb3aa30ea8'
PENDING='Q11_FUNCTIONAL_BOUNDARY_NOT_EVALUATED'
def examine(model):
 path=Path(__file__).parent/'references/BLUEPRINT_Q11_SOURCE.json'
 errors=[]
 if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=SOURCE_SHA:errors.append({'code':'Q11_SOURCE_BINDING_FAILURE'})
 suspects=[{'wall_id':k,'rect':v}for k,v in model.get('walls',{}).items()if 'privacy_screen'in k]
 return {'errors':errors,'pending':[PENDING], 'evidence':{'rule':'Q11 RESIDUAL_WASTE','source_file':'references/BLUEPRINT_Q11_SOURCE.json','source_sha256':SOURCE_SHA,'source_line':600,'status':'NOT_EVALUATED_MANDATORY','identified_privacy_screen_walls':suspects,'inventory_is_exhaustive':False,'functional_boundary_proof_implemented':False,'required_evidence':['Actual useful room/bath/usable closet boundary, not a renamed screen or fictitious space','Actual activity and access of that space independently established','Before/after area, free route widths/lengths, activity and assumed-light impacts','Privacy independently retained without an otherwise prohibited sight-only baffle'],'not_a_global_infeasibility_claim':True}}

def bound_closet_shells(module):
 """Exact source-sized useful cabinet construction; no gross-envelope opacity.
 Shell thickness .02 and rail recess .12 retain the existing study construction.
 Operations, actor access and privacy are separate fresh mandatory gates.
 """
 from checker114 import rect,F,intersects
 u=module.get('unit',{});result={};errors=[]
 for op in module.get('operations',{}).get('closets',[]):
  fid=op.get('fixture_id');f=u.get('fixtures',{}).get(fid)
  try:
   f=rect(f)
   if u.get('fixture_metadata',{}).get(fid,{}).get('kind')!='closet':raise ValueError('not closet')
   axis=0 if op.get('front_axis')=='x' else 1 if op.get('front_axis')=='y' else -1
   side=op.get('front_side')
   if axis<0 or side not in ('min','max'):raise ValueError('front')
   other=1-axis
   if f[axis+2]-f[axis]!=F('.6')or f[other+2]-f[other]!=F('2.05'):raise ValueError('immutable size')
   # Local coordinates n=depth away from opening; t=longitudinal along face.
   def world(r):
    n0,t0,n1,t1=map(F,r)
    ns=(f[axis]+n0,f[axis]+n1)if side=='min'else(f[axis+2]-n1,f[axis+2]-n0)
    ts=(f[other]+t0,f[other]+t1)
    return (ns[0],ts[0],ns[1],ts[1])if axis==0 else(ts[0],ns[0],ts[1],ns[1])
   expected=[world(('.12','0','.6','.02')),world(('.12','2.03','.6','2.05')),world(('.58','.02','.6','2.03'))]
   actual=[rect(r)for r in op.get('shell_rects',[])]
   if sorted(actual)!=sorted(expected):raise ValueError('actual shell/source construction mismatch')
   cavity=world(('.12','.02','.58','2.03'))
   if any(intersects(cavity,r)for r in actual):raise ValueError('no usable cavity')
   for otherid,q in u.get('fixtures',{}).items():
    if otherid!=fid and intersects(cavity,rect(q)):raise ValueError('cavity occupied by other fixture')
   if any(intersects(cavity,rect(q))for q in module.get('walls',{}).values()):raise ValueError('cavity obstructed by wall')
   for i,r in enumerate(actual):result[f'{u.get("id")}.{fid}.actual_skin{i}']=list(map(str,r))
  except (ValueError,TypeError,KeyError)as exc:errors.append({'code':'Q11_CLOSET_SHELL_NOT_BOUND','fixture':fid,'detail':str(exc)})
 return {'errors':errors,'opaque_materials':result}

def examine_closet_boundary(module):
 from checker114 import check_module,check_twin_module,digest
 binding=bound_closet_shells(module);errors=list(binding['errors']);pending=[]
 intent=module.get('q11_functional_boundary',module.get('privacy_construction',{}))
 if intent.get('kind')!='ACTUAL_USABLE_CLOSET_SHELL':pending.append('Q11_USEFUL_CLOSET_BOUNDARY_MISSING')
 if any('privacy_screen'in k for k in module.get('walls',{})):errors.append({'code':'Q11_SEPARATE_SIGHT_SCREEN_REMAINS'})
 if not binding['opaque_materials']:pending.append('Q11_ACTUAL_CLOSET_SKINS_MISSING')
 result=check_twin_module(module)if module.get('schema')=='PRIVATE_TWIN_ROOM_MODULE118'else check_module(module)
 errors.extend(result['errors']);pending.extend(result['pending'])
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_USEFUL_CLOSET_BOUNDARY_ONLY','errors':errors,'pending':pending,'module_hash':digest(module),'actual_opaque_materials':binding['opaque_materials'],'fresh_module_report':result,'whole_Q11_pass':False,'remaining':['Before/after actual area/route/light-impact ledger','Full-model transformed bindings and neighboring operation/circulation','Residual waste and useful-space review beyond this local cabinet boundary']}

_BASE_EXAMINE=examine

def examine_whole_boundary(model, *, workflow_context=None):
 from checker114 import check_module_placements,check_whole_privacy117,digest,F
 base=_BASE_EXAMINE(model);errors=list(base['errors']);pending=[];modules=[]
 beds={(u['id'],k)for u in model.get('units',[])for k in u['rooms']if k.startswith('bed')}
 placements=[p for p in model.get('module_placements',[])if p.get('module',{}).get('schema')in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118')]
 if {(p['unit_id'],p['room_id'])for p in placements}!=beds or not beds:pending.append('Q11_EVERY_BEDROOM_BOUNDARY_NOT_PROVEN')
 for p in placements:
  result=examine_closet_boundary(p['module']);modules.append({'unit':p['unit_id'],'room':p['room_id'],'result':result})
  errors.extend(result['errors']);pending.extend(result['pending'])
 if any('privacy_screen'in k for k in model.get('walls',{})):errors.append({'code':'Q11_SEPARATE_SIGHT_SCREEN_REMAINS'})
 placement=check_module_placements(model);errors.extend(placement['errors']);pending.extend(placement['pending'])
 privacy=check_whole_privacy117(model);errors.extend(privacy['errors']);pending.extend(privacy['pending'])
 path=Path(__file__).parent/'references/Q11_IMPACT_BASELINES118.json';impact=None
 if not path.exists()or hashlib.sha256(path.read_bytes()).hexdigest()!='f42e211189e1263a25f61763e5d11e7ea332cc60135c6d70e2b42005def04f31':pending.append('Q11_IMPACT_SOURCE_NOT_BOUND')
 else:
  row=next((r for r in json.loads(path.read_text())if r['after_hash']==digest(model)),None)
  if row is None:
   provenance=verify_new_workflow(model,workflow_context)
   if provenance['errors']:errors.extend(provenance['errors'])
   if provenance['verified']:
    impact={'kind':'NEW_CONSTRUCTION_CURRENT_STATE_ONLY','workflow':provenance,'current':current_metrics(model),'before_comparison_applicable':False,'improvement_claim':False,'limits':['Current actual geometry/activity/routes/window opportunities only','No invented predecessor or before-after improvement','Overall residual usefulness/quality has separate named gates']}
   else:pending.append('Q11_BEFORE_AFTER_OR_TRUSTED_NEW_WORKFLOW_NOT_EVALUATED')
  else:
   before=row['before_model']
   if digest(before)!=row['before_hash']or before['inputs']!=model['inputs']or before['program']!=model['program']:errors.append({'code':'Q11_IMPACT_MODEL_PROGRAM_BINDING'})
   def union_area(rs):
    rs=[tuple(map(F,r))for r in rs];xs=sorted({x for r in rs for x in(r[0],r[2])});ys=sorted({x for r in rs for x in(r[1],r[3])})
    return sum((b-a)*(d-c)for a,b in zip(xs,xs[1:])for c,d in zip(ys,ys[1:])if any(r[0]<=a<b<=r[2]and r[1]<=c<d<=r[3]for r in rs))
   def metrics(m):
    return {u['id']:{'room_areas':{k:str(union_area(rs))for k,rs in u['rooms'].items()},'routes':{k:{'length':str(sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1]))for a,b in zip(p,p[1:]))),'body_m':'.7'}for k,p in u['routes'].items()},'activities':u['activities'],'fixtures':u['fixtures']}for u in m['units']}
   for a,b in zip(before['units'],model['units']):
    if a['id']!=b['id']or set(a['activities'])!=set(b['activities'])or set(a['routes'])!=set(b['routes']):errors.append({'code':'Q11_REQUIRED_ACTIVITY_REMOVED'})
   impact={'before_model_hash':row['before_hash'],'after_model_hash':digest(model),'before':metrics(before),'after':metrics(model),'before_windows':before.get('concept_windows',[]),'after_windows':model.get('concept_windows',[]),'limits':['No daylight sufficiency claim','Longer paths are disclosed, not called improvements','Freed floor is not automatically useful','This exact saved comparison does not certify other dimensions']}
 if errors or pending:pending.append(PENDING)
 return {'errors':errors,'pending':sorted(set(pending)),'evidence':{**base['evidence'],'status':'FAIL'if errors else'NOT_EVALUATED_MANDATORY'if pending else'PASS_USEFUL_CLOSET_BOUNDARY_SCOPED','functional_boundary_proof_implemented':True,'modules':modules,'placement':placement,'privacy':privacy,'impact':impact,'scope':'Sight-only-screen replacement by actually usable source-sized cabinet; not all residual-space or spatial-quality rules'}}

# Whole-model entry point. Local boundary audit remains separately callable.
examine=examine_whole_boundary

def examine(model, *, workflow_context=None):
 try:return examine_whole_boundary(model,workflow_context=workflow_context)
 except (KeyError,ValueError,TypeError,IndexError)as exc:
  r=_BASE_EXAMINE(model);r['errors'].append({'code':'Q11_MODEL_OR_WITNESS_SCHEMA','detail':str(exc)});return r


def verify_new_workflow(model,context):
 """Context is supplied by the internal entrypoint, never deserialized from model.
 Source hashes bind the dimensions-only workflow; source module/isometry checks
 remain independently mandatory. Revision contexts cannot rename themselves new.
 """
 from source_registry_service365 import CurrentContext,verify_context
 if isinstance(context,CurrentContext):return verify_context(model,context)
 from fractions import Fraction as F
 errors=[];verified=False
 if context is None:return {'verified':False,'errors':[],'reason':'TRUSTED_WORKFLOW_CONTEXT_MISSING'}
 if context.get('operation')!='generate_from_dimensions':return {'verified':False,'errors':[],'reason':'REVISION_OR_UNKNOWN_WORKFLOW_REQUIRES_REAL_BASELINE'}
 if context.get('baseline_model_hash')is not None or context.get('existing_plan_id')is not None:errors.append({'code':'Q11_REVISION_MISLABELED_NEW_CONSTRUCTION'})
 try:
  if list(map(F,context['inputs']))!=list(map(F,model['inputs'])):errors.append({'code':'Q11_WORKFLOW_INPUT_BINDING'})
  for name in (('constructor129.py','assemble114.py') if context.get('construction_trace',{}).get('schema')=='CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1'else ('constructor128.py','assemble114.py') if context.get('construction_trace',{}).get('schema')=='CONSTRUCTION_TRACE128_HIERARCHICAL_V1'else ('constructor127.py','assemble114.py') if context.get('construction_trace',{}).get('schema')=='CONSTRUCTION_TRACE127_PAIR_V1'else ('constructor126.py','assemble114.py') if context.get('construction_trace',{}).get('schema')=='CONSTRUCTION_TRACE126_PAIR_V1'else('engine114.py','assemble114.py')):
   actual=hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
   if context.get('source_files',{}).get(name)!=actual:errors.append({'code':'Q11_WORKFLOW_SOURCE_BINDING','file':name})
 except (KeyError,ValueError,TypeError):errors.append({'code':'Q11_WORKFLOW_SCHEMA'})
 if context.get('construction_trace',{}).get('schema')=='CONSTRUCTION_TRACE129_HIERARCHICAL_FRAME_V1':
  from construction_replay129 import verify
 elif context.get('construction_trace',{}).get('schema')=='CONSTRUCTION_TRACE128_HIERARCHICAL_V1':
  from construction_replay128 import verify
 elif context.get('construction_trace',{}).get('schema')=='CONSTRUCTION_TRACE127_PAIR_V1':
  from construction_replay127 import verify
 elif context.get('construction_trace',{}).get('schema')=='CONSTRUCTION_TRACE126_PAIR_V1':
  from construction_replay126 import verify
 elif context.get('construction_trace',{}).get('schema')=='CONSTRUCTION_TRACE125_WORLD_V1':
  from construction_replay125 import verify
 else:
  from construction_replay118 import verify
 replay=verify(model,context)if not errors else {'verified':False,'errors':[],'pending':[]}
 errors.extend(replay['errors'])
 return {'verified':not errors and replay['verified'],'errors':errors,'pending':replay.get('pending',[]),'constructor_replay':replay,'operation':context.get('operation'),'source_files':context.get('source_files'),'inputs':context.get('inputs'),'trust_boundary':'Internal generated-request context plus exact constructor/source replay, not a model flag or user-supplied PASS receipt'}

def current_metrics(model):
 from fractions import Fraction as F
 def area(rs):
  rs=[tuple(map(F,r))for r in rs];xs=sorted({x for r in rs for x in(r[0],r[2])});ys=sorted({y for r in rs for y in(r[1],r[3])})
  return str(sum((b-a)*(d-c)for a,b in zip(xs,xs[1:])for c,d in zip(ys,ys[1:])if any(r[0]<=a<b<=r[2]and r[1]<=c<d<=r[3]for r in rs)))
 return {'units':{u['id']:{'room_floor_areas':{k:area(v)for k,v in u['rooms'].items()},'fixture_area':area(list(u['fixtures'].values())),'activities':u['activities'],'routes':{k:{'length':str(sum(abs(F(b[0])-F(a[0]))+abs(F(b[1])-F(a[1]))for a,b in zip(p,p[1:]))),'body_width_m':'.7'}for k,p in u['routes'].items()}}for u in model['units']},'actual_windows':model.get('concept_windows',[]),'area_is_not_proof_of_usefulness':True}
