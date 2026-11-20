"""P17 n1 full physical adapter, explicit source derivatives, never a pair bypass.
Base a38b7e53a7ef574709b270c26231450ba70cd6a1.
checker114._evaluate_impl: only n1/domain/contract, reference-root and adapter tail
differ. Q11 uses same-source P15 replay, not construction_replay118 fallback.
Circulation grammar inventories one P15 shell. Comparative necessity stays UNKNOWN.
Original historical report must be retained separately by the caller. No delivery.
"""
import copy,hashlib,inspect,json
from copy import deepcopy
from collections import Counter
from pathlib import Path
import single_model_p15 as p
from single_model_p15 import ENGINE,ROOT
import checker114 as legacy
from checker114 import F,BODY,rect,intersects,encloses,covered,sweeps,digest,check_module_placements,check_whole_privacy117
from q11_boundary118 import _BASE_EXAMINE,examine_closet_boundary,current_metrics,PENDING
from scope117 import EXCLUDED
from rule_contract118 import evaluate_rule_contract
from core_wall_audit118 import q,sweep,hit,core_concept,opening_hosts,output
from core_circulation_scope118 import subtract,SOURCE
from circulation_named_audit118 import area,long_corridor_facts
from circulation_integrity119 import remainder,safe_frame
VERSION='SINGLE_P17_FULL_PHYSICAL_V1'
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
PINS={
 'circulation_integrity119.py':'f1999e835c4e7541c8d4549f9591d6b632a61715',
 'core_circulation_scope118.py':'53fdb23b59ae600586df9d23c2b22cd16602f7e6',
 'final_route_ledger120.py':'0c32fc5fd201005ce0c6b4b5f91a211c09b2d0c6',
 'core_wall_audit118.py':'e2873b155a777e40df866c353db62e47130eee90',
 'checker114.py':'4f25ae5b9444c077159af90e872a84f4fcb25f42',
 'scope117.py':'f5386729b1f8b2fbd5229a340b73673bcdf122f4',
 'q11_boundary118.py':'34935e1d8b378118ea22f63281f90dfb55d73004',
 'rule_contract118.py':'97bf97b3fe90d14314f0633357e6e66856597f8b',
 'named_checks118.py':'bb8a4da75fa1059699618ae20486019deeae682a'}
def source_guard():
 baseline=p.snapshot()
 for name,pin in PINS.items():
  path=ENGINE/name;raw=path.read_bytes()
  p.require(not path.is_symlink() and hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()==pin,'PHYSICAL_SOURCE_CHANGED:'+name)
 for fn,path in ((legacy._evaluate_impl,ENGINE/'checker114.py'),(p.replay,ROOT/'app/local_integration/single_model_p15.py'),(examine_closet_boundary,ENGINE/'q11_boundary118.py'),(evaluate_rule_contract,ENGINE/'rule_contract118.py'),(core_concept,ENGINE/'core_wall_audit118.py')):
  p.require(Path(inspect.getsourcefile(fn)).resolve()==path.resolve(),'ACTUAL_PHYSICAL_SOURCE_PATH')
 return {'producer':baseline,'physical_adapter':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
def validate_identity(model,raw,proposal):
 p.require(p.digest(raw)==p.digest(p.RAW),'SINGLE_RAW_BINDING')
 p.require(model.get('schema')==p.FAMILY and model.get('contract_version')=='p15-single-v1','SINGLE_MODEL_SCHEMA')
 p.require(p.digest(model.get('inputs'))==p.digest(['18','20',1]),'SINGLE_TYPED_INPUT')
 p.require(type(model.get('units'))is list and [u.get('id')for u in model['units']]==['A'],'SINGLE_UNIT_INVENTORY')
 p.require(type(model.get('program',{}).get('units'))is int and model['program']['units']==1,'SINGLE_PROGRAM_UNIT_COUNT')
 p.require(type(proposal.get('bedrooms'))is int and proposal['bedrooms']==2 and proposal.get('sleep_roles')==['double','twin'],'SINGLE_PROGRAMME')
 c=p.core(raw)
 expected={'family':p.FAMILY,'raw_digest':p.digest(raw),'core_digest':p.digest(c),'proposal_digest':p.digest(proposal),'programme_digest':p.digest(p.lookup('PROGRAM_2BED_V1')),'unit_assignment':{'A':p.digest(proposal)},'pair_built_then_filtered':False}
 p.require(p.digest(model.get('construction_identity'))==p.digest(expected),'SINGLE_CONSTRUCTION_IDENTITY')
 p.require(p.digest(model.get('common_spaces'))==p.digest({k:c[k]for k in ('stair','lift','lobby')}),'SINGLE_CORE_BINDING')
 p.require(p.digest(model['units'][0].get('ownership'))==p.digest(c['unit_ownership']['A']),'SINGLE_OWNERSHIP')
 p.require(all(model.get(k)is False for k in AUTH),'SINGLE_NO_AUTHORITY')
def verify_context(model,context):
 p.require(type(context)is dict and set(context)=={'schema','raw','proposal'} and context['schema']=='SINGLE_P17_PHYSICAL_CONTEXT_V1','SINGLE_CONTEXT_SCHEMA')
 validate_identity(model,context['raw'],context['proposal'])
 replay=p.replay(model,context['raw'],context['proposal'])
 p.require(replay.get('verified')is True and replay.get('model_digest')==p.digest(model),'SINGLE_REPLAY')
 return {'verified':True,'errors':[],'pending':[],'constructor_replay':replay,'operation':'generate_from_dimensions','scope':'P15 exact same-source replay, not independent physics or producer authentication'}

def single_applicability(model):
 return {'status':'PASS_LIMITED','witness':{'applies':True,'family':p.FAMILY},'scope':'Record unresolved same-program circulation necessity; no arbitrary length threshold.'}
def single_necessity(model):
 return output('Q04',[],['SINGLE_SAME_PROGRAM_CIRCULATION_COMPARISON_NOT_EVALUATED'],{'actual_route_cost_facts':long_corridor_facts(model)['witness'],'historical_pair_component_executed':False,'necessity_verified':False})
def adapters_for_single_workflow(context):
 from named_checks118 import ADAPTERS,response
 from final_route_ledger120 import evaluate as final_ledger
 callbacks=dict(ADAPTERS)
 def q11_single(model):
  r=examine_q11(model,workflow_context=context)
  return response(r['errors'],r['pending'],r['evidence'],'Same physical Q11 component/placement/privacy checks with P15 source replay; no pair provenance substitution.')
 def circulation_single(model):
  a=single_circulation_integrity(model);b=final_ledger(model)
  return response(list(a['witness'].get('errors',[]))+b['witness']['errors'],list(a['witness'].get('pending',[])),{'actual_functional_integrity':a,'final_route_classification':b},'Same circulation physical checks and final-route floor ledger, P15 one-unit shell grammar; necessity remains separate.')
 callbacks.update(q11_functional_boundary=q11_single,circulation_functional_integrity=circulation_single,long_corridor_necessity=single_necessity)
 return callbacks

def evaluate(model,raw,proposal):
 before=source_guard();original=p.digest(model)
 context={'schema':'SINGLE_P17_PHYSICAL_CONTEXT_V1','raw':copy.deepcopy(raw),'proposal':copy.deepcopy(proposal)}
 replay=verify_context(model,context)
 report=_evaluate_impl(model,workflow_context=context)
 p.require(p.digest(model)==original,'PHYSICAL_INPUT_MUTATION')
 p.require(source_guard()==before,'PHYSICAL_SOURCE_MUTATION')
 report.update(schema='SINGLE_PHYSICAL_P17_V1',family=p.FAMILY,replay=copy.deepcopy(replay),source_snapshot=before,integrity_verified=True,
               original_historical_report_replaced=False,**{k:False for k in AUTH})
 report.update(eligible_for_draft_export=False,draft_review_allowed=False,release=False,public_release=False,technical_accepted=False)
 return report

def grammar(m, *, frame_core=None,frame_local=None):
 """P15 one-unit module-composed two-bedroom grammar only, never arbitrary labels.
 Unknown enclosing-wall sources/rooms remain pending, including renamed halls.
 Separate mandatory module-placement tests prove every mapped wall geometry.
 """
 from private_binding121 import examine as bind_private
 binding=bind_private(m) if m.get('private_domains') else None
 missing=[];mapped=set();supported={'PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118','BATHROOM_MODULE117','KITCHEN_MODULE117'}
 for placement in m.get('module_placements',[]):
  module=placement['module']
  if module.get('schema')not in supported:missing.append('UNSUPPORTED_CIRCULATION_MODULE_GRAMMAR')
  mapped|={placement['id_map'][k]for k in module['walls']}
 expected={'left','right','front','back'}
 expected|={uid+'.unit_boundary.solid'+str(i)for uid in('A',)for i in(0,1)}
 expected|={'core.stair.'+k for k in('left','bottom','top','right.solid0','right.solid1')}
 expected|={'core.lift.'+k for k in('right','bottom','top','left.solid0','left.solid1')}
 if binding is not None:
  missing.extend(binding['errors']+binding['pending']);expected.update(binding['boundary_wall_ids'])
 if m.get('frame_binding125'):
  from frame_circulation125 import grammar as frame_grammar
  missing.extend(frame_grammar(m,frame_core,frame_local))
 elif set(m['walls'])-mapped!=expected:missing.append('UNCLASSIFIED_ENCLOSING_WALL_OR_CORRIDOR_SOURCE')
 for u in m['units']:
  beds={k for k in u['rooms']if k.startswith('bed')}
  allowed_extra={'private_circulation'} if len(beds)==3 and binding is not None else set()
  if beds not in ({'bed1'},{'bed1','bed2'},{'bed1','bed2','bed3'}) or set(u['rooms']) != beds|{'bath','kitchen','dining','living','entry_circulation'}|allowed_extra:missing.append(u['id']+':UNSUPPORTED_OR_RENAMED_ROOM_CIRCULATION_GRAMMAR')
 from paired_private_zone118 import examine
 pairs=examine(m)
 for u in m['units']:
  beds={k for k in u['rooms']if k.startswith('bed')}
  if len(beds)==3 and binding is not None and not binding['errors'] and not binding['pending']:
   continue
  if len(beds)==1:
   # Source-bound placement and actual access are checked independently; a
   # two-bedroom paired zone is inapplicable, not waived for multi-bedroom.
   placed=[p for p in m.get('module_placements',[]) if p.get('module',{}).get('schema') in {'PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118'} and any(v.startswith(u['id']+'.bed1.') for v in p.get('id_map',{}).values())]
   if len(placed)!=1:missing.append(u['id']+':SINGLE_BEDROOM_SOURCE_PLACEMENT_MISSING')
   continue
  if not any(z['unit']==u['id']and z['status']=='PASS_TWO_BEDROOM_PRIVATE_APPROACH_TOPOLOGY'and set(z['bedrooms'])=={u['id']+'.bed1',u['id']+'.bed2'}for z in pairs['zones']):missing.append(u['id']+':NO_INDEPENDENT_REAL_PAIRED_PRIVATE_ZONE')
 return sorted(set(missing))



@safe_frame
def single_circulation_integrity(m, *, frame_core=None,frame_local=None):
 # These independent validators evaluate current geometry, never stored PASS.
 from named_checks118 import body_route_sweeps,public_named_scenarios
 from access_accounting118 import bath_nonprivate_access
 from checker114 import check_module_placements
 placement=check_module_placements(m)
 checks={'core':core_concept(m),'hosts':opening_hosts(m),'body':body_route_sweeps(m),'public_scenarios':public_named_scenarios(m),'bath_nonprivate':bath_nonprivate_access(m)}
 errors=[];pending=grammar(m,frame_core=frame_core,frame_local=frame_local);rows=[]
 if placement['errors']:errors.append('ACTUAL_SOURCE_MODULE_PLACEMENT_FAILED')
 pending.extend(placement['pending'])
 for k,r in checks.items():
  if r['status']=='FAIL':errors.append(k+':ACTUAL_FUNCTIONAL_CIRCULATION_FAILED')
  elif r['status']!='PASS_LIMITED':pending.append(k+':ACTUAL_FUNCTIONAL_CIRCULATION_NOT_EVALUATED')
 body=F(str(m['profile']['body_m']))
 for u in m['units']:
  paths=list(u['routes'].values())+list(u.get('scenario_routes',{}).values())
  sw=[r for p in paths for r in sweep(p,body)]
  dedicated=[q(r)for r in u['rooms'].get('entry_circulation',[])]
  # Room labels are not evidence of function. Classify uncovered material
  # explicitly rather than counting it as circulation/usable seating.
  residual=remainder(dedicated,sw)
  for r in dedicated:
   if not any(hit(r,s)for s in sw):errors.append(u['id']+':DECLARED_CIRCULATION_COMPONENT_WITHOUT_ACTUAL_ROUTE_USE')
  rows.append({'unit':u['id'],'route_body_union_m2':str(area(sw)),'declared_entry_union_m2':str(area(dedicated)), 'not_route_proven_floor_m2':str(area(residual)), 'not_route_proven_parts':[list(map(str,r))for r in residual], 'classification':'NOT_ROUTE_PROVEN; not automatically useful seating or necessary corridor. Door/other operation floor is assessed by separate mandatory operation gates.'})
 common=[q(r)for r in m['common_spaces']['lobby']];sw=[r for p in m['common_routes'].values()for r in sweep(p,body)]
 unused=[r for r in common if not any(hit(r,s)for s in sw)]
 return output('Q04',errors,pending,{'source':SOURCE,'module_placement':placement,'checks':checks,'units':rows,'common_unprogrammed_components':[{'rect':list(map(str,r)),'area_m2':str(area([r])),'classification':'COMMON_UNPROGRAMMED_NOT_PROVEN_FUNCTIONAL'}for r in unused], 'common_not_route_proven_area_m2':str(area(remainder(common,sw))), 'functional_claim_boundary':'Only actual required body-route swept union counted as route use. Unused floor is preserved and disclosed, never labelled necessary circulation or useful public area by this audit.', 'review_separation':'Layout alternative, preference tradeoffs and absolute necessity are REVIEW, not excused collisions or fake functional floor.', 'route_cost_facts':long_corridor_facts(m)['witness']})


def examine_q11(model, *, workflow_context=None):
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
 path=ENGINE/'references/Q11_IMPACT_BASELINES118.json';impact=None
 if not path.exists()or hashlib.sha256(path.read_bytes()).hexdigest()!='f42e211189e1263a25f61763e5d11e7ea332cc60135c6d70e2b42005def04f31':pending.append('Q11_IMPACT_SOURCE_NOT_BOUND')
 else:
  row=next((r for r in json.loads(path.read_text())if r['after_hash']==digest(model)),None)
  if row is None:
   provenance=verify_context(model,workflow_context)
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



def reduce_scope117(report):
 if not isinstance(report,dict) or report.get('checker_version')!=VERSION:
  raise ValueError('SINGLE_P17_REQUIRES_OWN_CHECKER_REPORT')
 if not isinstance(report.get('errors'),list)or not isinstance(report.get('pending'),list)or any(not isinstance(p,str)for p in report['pending']):
  raise ValueError('CONCEPT117_REPORT_SCHEMA')
 out=deepcopy(report);original=list(report['pending']);moved=sorted(set(original)&set(EXCLUDED));remaining=sorted(set(original)-set(EXCLUDED))
 out['physics_status_before_scope']=report.get('status');out['original_pending']=original
 out['pending']=remaining;out['gate_scope']='SINGLE_P17_CONCEPT_SCOPE_V1';out['pending_scope']='Mandatory limited-Concept controls only; other unknowns are retained separately, never marked PASS.'
 out['not_evaluated']=sorted(set(report.get('not_evaluated',[]))|set(moved))
 out['out_of_scope']=list(report.get('out_of_scope',[]))+[dict(code=k,status='NOT_EVALUATED',**EXCLUDED[k])for k in moved]
 ready=not out['errors']and not remaining
 out['status']='FAIL'if out['errors']else'NOT_EVALUATED'if remaining else'PASS_CONCEPT_SCOPED_REVIEW'
 out['eligible_for_draft_export']=ready;out['draft_review_allowed']=ready
 out.update(accepted=False,release=False,technical_accepted=False,public_release=False)
 out['limitations']=['پیش‌نویس برای بررسی کانسپت است، نه نقشه اجرایی، تأیید فنی یا پذیرش نهایی مالک.','هیچ تضمین پوشش همه ابعاد، شش گزینه، بهترین چیدمان یا کیفیت کلی از این نتیجه استنباط نمی‌شود.']+[EXCLUDED[k]['label_fa']for k in moved]
 return out


def attach_rule_contract(model,existing_report,*,trusted_evaluators=None,context=None,applicability_evaluators=None):
 """Internal checker connector. An existing PASS supplies zero named-rule proofs.
Call directly after fresh independent physical evaluation, not from HTTP receipt.
Only propagates existing errors and named missing tests; cannot launder producer
claims. Consumers still perform their own source/report reconstruction on reopen.
"""
 out=copy.deepcopy(existing_report);audit=evaluate_rule_contract(model,trusted_evaluators=trusted_evaluators,context=context,applicability_evaluators=applicability_evaluators)
 errors=list(out.get('errors',[]));pending=list(out.get('pending',[]))
 if out.get('model_hash')!=digest(model)or out.get('checker_version')!=VERSION:errors.append({'code':'PHYSICAL_REPORT_BINDING_OR_ORIGIN'})
 errors.extend(audit['errors']);pending.extend(audit['pending']);out['errors']=errors;out['pending']=sorted(set(pending));out['rule_contract_evidence']=audit
 ready=not errors and not pending and audit['status']=='PASS_NAMED_REQUIRED_SCOPED'and existing_report.get('status')in ('PASS_CONCEPT_SCOPED_REVIEW','PASS_LIMITED')
 out['status']='FAIL'if errors else'NOT_EVALUATED'if not ready else'PASS_CONCEPT_SCOPED_REVIEW'
 out['eligible_for_draft_export']=ready;out['draft_review_allowed']=ready;out.update(accepted=False,release=False,technical_accepted=False,public_release=False,all_rules_approved=False)
 return out


def _evaluate_impl(model, *, workflow_context=None, comparison_only=False):
 errors=[];pending=[];counts={}
 def err(code,**data):errors.append(dict(code=code,**data))
 try:
  W,L,n=map(F,model['inputs']);frame=rect([0,0,W,L])
  if not 5<=W<=25 or not 5<=L<=25 or n!=1:err('INPUT_PROGRAM_DOMAIN')
  if model.get('contract_version')!='p15-single-v1':err('UNSUPPORTED_CONSTRAINT_CONTRACT_VERSION')
  if F(model.get('profile',{}).get('body_m',0))!=BODY:err('MODEL_BODY_CONTRACT_BINDING')
  catalog=json.loads((ENGINE/'fixture_catalog114.json').read_text());catalog_hash=digest(catalog)
  source_path=ENGINE/catalog['source_file'];source_bytes=source_path.read_bytes();source=json.loads(source_bytes)
  if hashlib.sha256(source_bytes).hexdigest()!='2def7c7b7237eec7665f6a410096c9902166ef0fb6c3a880cd2f58b1b1c783e4' or catalog['source_file_sha256']!=hashlib.sha256(source_bytes).hexdigest():err('IMMUTABLE_REFERENCE_FILE_CHANGED')
  for kind,spec in catalog['types'].items():
   source_q=rect(source['units'][0]['fixtures'][spec['source_fixture_key']])
   if (F(spec['width_m']),F(spec['depth_m']))!=(source_q[2]-source_q[0],source_q[3]-source_q[1]) or spec['scale_allowed']is not False:err('CATALOG_REFERENCE_SIZE_MISMATCH',kind=kind)
  if model.get('fixture_catalog_hash')!=catalog_hash:err('FIXTURE_CATALOG_BINDING')
  units=model['units'];walls={k:rect(v)for k,v in model['walls'].items()};owners={};fixtures=[]
  if len(units)!=1:err('UNIT_COUNT')
  for k,w in walls.items():
   if not encloses(frame,w):err('WALL_OUTSIDE_FRAME',wall=k)
  for u in units:
   uid=u['id'];owner=[rect(v)for v in u['ownership']];owners[uid]=owner
   for q in owner:
    if not encloses(frame,q):err('OWNERSHIP_OUTSIDE_FRAME',unit=uid)
   rooms={k:[rect(q)for q in v]for k,v in u['rooms'].items()}
   for k,rs in rooms.items():
    for r in rs:
     if not covered(r,owner):err('ROOM_OUTSIDE_OWNERSHIP',room=k)
   names=list(rooms)
   for i,a in enumerate(names):
    for b in names[i+1:]:
     if any(intersects(q,r)for q in rooms[a]for r in rooms[b]):err('ROOM_OVERLAP',rooms=[a,b])
   local={k:rect(v)for k,v in u['fixtures'].items()}
   for k,q in local.items():
    fixtures.append((uid,k,q))
    if not covered(q,owner):err('FIXTURE_OUTSIDE_OWNERSHIP',fixture=k)
    for wk,w in walls.items():
     if intersects(q,w):err('FIXTURE_WALL_COLLISION',fixture=k,wall=wk)
   routes=dict(u.get('routes',{}));routes.update(u.get('scenario_routes',{}))
   if not routes:pending.append('MISSING_BODY_ROUTES:'+uid)
   for rk,path in routes.items():
    for q in sweeps(path):
     if not covered(q,owner):err('BODY_OUTSIDE_OWNERSHIP',route=rk)
     for wk,w in walls.items():
      if intersects(q,w):err('BODY_WALL_COLLISION',route=rk,wall=wk)
     for fk,f in local.items():
      kind=u.get('fixture_metadata',{}).get(fk,{}).get('kind')
      source_task_exception=(kind=='shower_floor'and rk in('shower','shower_use'))or(kind=='WC_iranian'and rk=='WC_use')
      if not source_task_exception and intersects(q,f):err('BODY_FIXTURE_COLLISION',route=rk,fixture=fk)
   beds=[k for k in rooms if k.split('.')[-1].startswith('bed')]
   if not 1<=len(beds)<=4:err('BEDROOM_PROGRAM_COUNT',unit=uid)
   if F(model.get('program',{}).get('bedrooms_per_unit',0))!=len(beds):err('DECLARED_BEDROOM_PROGRAM_BINDING',unit=uid)
   metadata=u.get('fixture_metadata',{});inventory=Counter()
   for fk,q in local.items():
    md=metadata.get(fk,{});kind=md.get('kind');spec=catalog['types'].get(kind);inventory[kind]+=1
    if kind=='dining_table6':
     spec={'width_m':'2.2','depth_m':'1','allowed_plan_rotations_deg':[0,90,180,270]}
    if kind=='single_bed':
     spec={'width_m':'1.9','depth_m':'.9','allowed_plan_rotations_deg':[0,90,180,270]}
     source_path=ENGINE/'references/CAPACITY_PROGRAM118_SOURCE.json'
     if hashlib.sha256(source_path.read_bytes()).hexdigest()!='427cde4c55e57ea7c26ff52bb2651859750b93913cc86ecdf2751fad37566e8f':err('TWIN_SOURCE_CHANGED')
    if spec is None:err('UNKNOWN_FIXTURE_TYPE',fixture=fk);continue
    rotation=md.get('rotation_deg')
    if rotation not in spec['allowed_plan_rotations_deg']:err('FIXTURE_ROTATION',fixture=fk);continue
    expected=(F(spec['width_m']),F(spec['depth_m']))
    if rotation%180:expected=expected[::-1]
    if (q[2]-q[0],q[3]-q[1])!=expected:err('IMMUTABLE_FIXTURE_SIZE_CHANGED',fixture=fk)
   twin_rooms={p['room_id']for p in model.get('module_placements',[])if p.get('unit_id')==uid and p.get('module',{}).get('schema')=='PRIVATE_TWIN_ROOM_MODULE118'}
   expected=Counter({k:1 for k in catalog['types']});expected['bed']=len(beds)-len(twin_rooms);expected['closet']=len(beds)
   if twin_rooms:expected['single_bed']=2*len(twin_rooms)
   roles=model.get('program',{}).get('sleep_roles')
   if roles is not None:
    actual_roles=['twin'if br in twin_rooms else'double'for br in sorted(beds)]
    if roles!=actual_roles:err('SLEEP_ROLE_MODULE_BINDING',unit=uid)
    if sorted(roles)==['double','twin','twin']:
     expected['armchair1']=2;expected['armchair2']=2
     if model['program'].get('design_occupants_per_unit')!=6:err('SIX_PERSON_PROGRAM_OCCUPANCY_BINDING',unit=uid)
   # Installed source dining inventory is independent of sleep occupancy.
   # No module means the legacy catalog inventory remains required.
   if u.get('dining_module_placement') is not None:
    try:
     from dining_inventory119 import counts as source_dining_counts
     dining_counts=source_dining_counts(u)
     if 'dining_table6'in dining_counts:expected.pop('dining_table',None)
     for kind,count in dining_counts.items():expected[kind]=count
    except (KeyError,ValueError,TypeError,IndexError)as ex:err('DINING_SOURCE_INVENTORY_BINDING',unit=uid,detail=str(ex))
   if inventory!=expected:err('FIXTURE_INVENTORY',unit=uid,expected=dict(expected),actual=dict(inventory))
   for br in beds:
    for kind in (('single_bed','closet')if br in twin_rooms else('bed','closet')):
     members=[fk for fk,q in local.items()if metadata.get(fk,{}).get('kind')==kind and covered(q,rooms[br])]
     if len(members)!=(2 if kind=='single_bed'else 1):err('BEDROOM_FIXTURE_MEMBERSHIP',room=br,kind=kind)
   if any(not covered(q,[r for rs in rooms.values()for r in rs]+list(walls.values())) for q in owner):err('UNACCOUNTED_OWNERSHIP_FLOOR',unit=uid)
  for i,(a,rs)in enumerate(owners.items()):
   for b,ss in list(owners.items())[i+1:]:
    if any(intersects(r,s)for r in rs for s in ss):err('UNIT_OWNERSHIP_OVERLAP',units=[a,b])
  for i,(u,k,q)in enumerate(fixtures):
   for v,j,r in fixtures[i+1:]:
    if intersects(q,r):err('FIXTURE_COLLISION',fixtures=[k,j])
  for op in model.get('openings',[]):
   q=rect(op['rect']);host_record=model.get('wall_hosts',{}).get(op.get('host_wall_id'));host=rect(host_record)if host_record is not None else walls.get(op.get('host_wall_id'))
   pocket_type=op.get('kind',op.get('operation_kind'))=='pocket_source113'
   if pocket_type:
    from operation_check114 import pocket_host_geometry117
    for code in pocket_host_geometry117(model,op,walls):err(code,opening=op['id'])
   elif host is None:pending.append('OPENING_UNCUT_HOST_BINDING_REQUIRED:'+op['id'])
   elif not encloses(host,q):err('OPENING_OUTSIDE_HOST',opening=op['id'])
   if host is not None and not pocket_type:
    pieces=[r for r in walls.values()if encloses(host,r)]+[rect(z['rect'])for z in model.get('openings',[])if z.get('host_wall_id')==op.get('host_wall_id')]
    if not covered(host,pieces):err('HOST_WALL_UNACCOUNTED_GAP',opening=op['id'])
    if any(intersects(q,w)for w in walls.values()):err('OPENING_NOT_ACTUALLY_CUT',opening=op['id'])
   vertical=(q[3]-q[1])>(q[2]-q[0]);axis=1 if vertical else 0
   low=q[axis]+BODY/2;high=q[axis+2]-BODY/2
   obstacles=list(walls.values())+[r for _,_,r in fixtures]
   values={low,high}
   for r in obstacles:
    values.update(v for v in (r[axis]-BODY/2,r[axis+2]+BODY/2)if low<=v<=high)
   ordered=sorted(values);values.update((a+b)/2 for a,b in zip(ordered,ordered[1:]))
   witness=False
   for t in values:
    if low>high or not low<=t<=high:continue
    crossing=(q[0]-BODY/2,t-BODY/2,q[2]+BODY/2,t+BODY/2)if vertical else(t-BODY/2,q[1]-BODY/2,t+BODY/2,q[3]+BODY/2)
    if encloses(frame,crossing)and not any(intersects(crossing,r)for r in obstacles):witness=True;break
   if not witness:err('NO_BODY_CROSSING_AT_ACTUAL_APERTURE',opening=op['id'])
  # Owner scope121: do not evaluate light, ventilation or required window inventory.
  # Preserve only geometry of window objects that actually exist in this model.
  for win in model.get('concept_windows',[]):
   q=rect(win['plan_rect']);host=walls.get(win.get('host_wall_id'))
   if host is None or not encloses(host,q):err('WINDOW_HOST_MISSING_OR_OUTSIDE',window=win['id'])
   if win.get('floor_portal')is not False or not 0<=F(win['sill_m'])<F(win['head_m']):err('WINDOW_HEIGHT_OR_FLOOR_PORTAL',window=win['id'])
  from operation_check114 import check_operations
  operation_owners=dict(owners)
  lobby=model.get('common_spaces',{}).get('lobby',[])
  if lobby:operation_owners['COMMON']=[rect(q)for q in lobby]
  oe,op=check_operations(model,operation_owners,walls,fixtures);errors.extend(oe);pending.extend(op)
  if model.get('module_placements')is not None:
   placement=check_module_placements(model);errors.extend(placement['errors']);pending.extend(placement['pending'])
  common=model.get('common_spaces',{});cr=model.get('common_routes',{})
  required={src+'_'+u['id']for src in ('stair','lift')for u in units}
  if set(cr)!=required:err('COMMON_ROUTE_INVENTORY')
  for name,path in cr.items():
   uid=name.rsplit('_',1)[-1];source=name.rsplit('_',1)[0]
   if source not in ('stair','lift')or uid not in owners:err('COMMON_ROUTE_UNKNOWN_ENDPOINT',route=name);continue
   core=rect(common[source]);start=tuple(F(v)for v in path[0])
   if not(core[0]<=start[0]<=core[2]and core[1]<=start[1]<=core[3]):err('COMMON_ROUTE_NOT_FROM_CORE',route=name)
   ownunit=next(u for u in units if u['id']==uid)
   entryparts=[rect(r)for r in ownunit['rooms'].get('entry_circulation',[])]
   end=tuple(F(v)for v in path[-1]);endbody=(end[0]-BODY/2,end[1]-BODY/2,end[0]+BODY/2,end[1]+BODY/2)
   if not covered(endbody,entryparts):err('COMMON_ROUTE_NOT_TO_REAL_ENTRY_FLOOR',route=name)
   for q in sweeps(path):
    if not encloses(frame,q):err('COMMON_BODY_OUTSIDE_FRAME',route=name)
    for wid,w in walls.items():
     if intersects(q,w):err('COMMON_BODY_WALL_COLLISION',route=name,wall=wid)
    for fu,fk,f in fixtures:
     if intersects(q,f):err('COMMON_BODY_FIXTURE_COLLISION',route=name,fixture=fk)
    for other,rs in owners.items():
     if other!=uid and any(intersects(q,r)for r in rs):err('COMMON_BODY_OTHER_UNIT',route=name,unit=other)
    for rkey,rs in ownunit['rooms'].items():
     if rkey not in ('entry_circulation','living') and any(intersects(q,rect(r))for r in rs):err('COMMON_BODY_PRIVATE_ROOM',route=name,room=rkey)
    othercore=rect(common['lift'if source=='stair'else'stair'])
    if intersects(q,othercore):err('COMMON_BODY_OTHER_CORE',route=name)
  if not cr:pending.append('COMMON_ROUTES_MISSING')
  if model.get('route_failures'):err('MISSING_REQUIRED_ACTIVITY_ROUTES',failures=model['route_failures'])
  for u in units:
   for target,point in u.get('route_targets',{}).items():
    path=u.get('routes',{}).get(target)
    if not path or tuple(map(F,path[-1]))!=tuple(map(F,point)):err('ROUTE_TARGET_BINDING',unit=u['id'],target=target)
   if set(u.get('activities',{}))!=set(u.get('route_targets',{})):err('ACTIVITY_ROUTE_INVENTORY',unit=u['id'])
  privacy=check_whole_privacy117(model);errors.extend(privacy['errors']);pending.extend(privacy['pending'])
  pending.extend(['VARIABLE_ROOM_PROGRAM_CAPACITY_AND_SPATIAL_QUALITY_NOT_EVALUATED'])
  counts={'units':len(units),'fixtures':len(fixtures),'walls':len(walls),'windows':len(model.get('concept_windows',[]))}
 except (KeyError,ValueError,TypeError,IndexError,StopIteration,ZeroDivisionError)as e:err('MODEL_SCHEMA_OR_GEOMETRY_ERROR',detail=str(e))
 report={'checker_version':VERSION,'model_hash':digest(model),'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_LIMITED','errors':errors,'pending':sorted(set(pending)),'counts':counts,'privacy_evidence':locals().get('privacy',{}).get('evidence'),'placement_evidence':locals().get('placement'),'accepted':False,'release':False,'eligible_for_draft_export':not errors and not pending}
 
 scope_doc=ENGINE/'references/CONCEPT_GATE_FA.md'
 if not scope_doc.is_file() or hashlib.sha256(scope_doc.read_bytes()).hexdigest()!='8804bca0ecb774c5186969f85c0d03b73766e23e20d30304b84f580c41a1d05e':
  report['errors'].append({'code':'CONCEPT_SCOPE_SOURCE_CHANGED'})
 report['scope_source']={'path':'references/CONCEPT_GATE_FA.md','sha256':'8804bca0ecb774c5186969f85c0d03b73766e23e20d30304b84f580c41a1d05e','source':'Pinned limited Concept contract from reference113, not technical approval'}
 report['nonleaf_interfaces']=[{'opening_id':o['id'],'kind':o.get('kind'),'hardware_status':'NOT_EVALUATED' if o.get('kind')=='core_access_interface' else 'NO_LEAF_SOURCE_ARCH'} for o in model.get('openings',[]) if o.get('kind') in ('core_access_interface','permanent_open_arch')]
 
 q11=examine_q11(model,workflow_context=workflow_context);report['errors'].extend(q11['errors']);report['pending'].extend(q11['pending']);report['q11_evidence']=q11['evidence']
 report['contract_addendum']='BLUEPRINT_Q11_MANDATORY_SOURCE_COMPLETENESS118_V1'
 
 
 adapters=adapters_for_single_workflow(workflow_context)
 if comparison_only:
  adapters['long_corridor_necessity']=lambda m:{'status':'NOT_EVALUATED','witness':{'code':'EXCLUDED_FOR_NONCIRCULAR_COMPARISON','model_hash':digest(m)},'scope':'Internal comparison prerequisite only; Q04 not accepted or waived.'}
 return attach_rule_contract(model,reduce_scope117(report),trusted_evaluators=adapters,context={'stage':'concept_internal','batch_models':[model]},applicability_evaluators={'long_corridor_necessity':single_applicability})

