"""Fresh source-bound before/after cabinet-boundary study, not current Q11 closure."""
from pathlib import Path
from copy import deepcopy
import inspect
from contract114 import digest
from open_front_kitchen_study import ENGINE
def assess(packet,trace,baseline_packet,baseline_context):
    from open_front_world_origin import verify
    from evaluate_pair127 import evaluate as baseline_evaluate
    from open_front_placement_check import check_module_placements
    from open_front_operation_check import check_operations
    from checker114 import check_whole_privacy117,rect
    from q11_boundary118 import examine_closet_boundary,current_metrics
    for fn,path in [(baseline_evaluate,ENGINE/'evaluate_pair127.py'),(check_whole_privacy117,ENGINE/'checker114.py'),(examine_closet_boundary,ENGINE/'q11_boundary118.py'),
                    (verify,Path(__file__).with_name('open_front_world_origin.py')),(check_module_placements,Path(__file__).with_name('open_front_placement_check.py')),(check_operations,Path(__file__).with_name('open_front_operation_check.py'))]:
        if Path(inspect.getsourcefile(fn)).resolve()!=path.resolve():raise ValueError('Q11_STUDY_IMPORT_PATH')
    origin=verify(packet,trace);m=packet['world_model'];old=baseline_packet['world_model']
    bt=baseline_context['construction_trace']
    if bt.get('schema')!='CONSTRUCTION_TRACE127_PAIR_V1' or digest(bt['raw'])!=digest(trace['raw']) or digest(bt['proposals'])!=digest(trace['proposals']):raise ValueError('ACTUAL_PREDECESSOR_INPUT_PROPOSAL_BINDING')
    if digest(m['inputs'])!=digest(old['inputs']) or digest(m['program'])!=digest(old['program']) or digest(m['profile'])!=digest(old['profile']):raise ValueError('BEFORE_AFTER_PROGRAM_BINDING')
    before=digest([packet,trace,baseline_packet,baseline_context])
    baseline=baseline_evaluate(baseline_packet,baseline_context)
    if baseline.get('status')!='PASS_CONCEPT_SCOPED_REVIEW' or baseline.get('errors') or baseline.get('pending') or not baseline.get('multiproposal_provenance127',{}).get('verified'):raise ValueError('BASELINE_NOT_FRESH_VERIFIED')
    errors=[];pending=[];modules=[]
    beds={(u['id'],k)for u in m['units']for k in u['rooms']if k.startswith('bed')}
    placed=[p for p in m['module_placements']if p['module']['schema']in('PRIVATE_ROOM_MODULE116','PRIVATE_TWIN_ROOM_MODULE118')]
    if {(p['unit_id'],p['room_id'])for p in placed}!=beds or not beds:pending.append('EVERY_BEDROOM_BOUNDARY_NOT_PROVEN')
    for p in placed:
        r=examine_closet_boundary(p['module']);errors.extend(r['errors']);pending.extend(r['pending'])
        modules.append({'unit':p['unit_id'],'room':p['room_id'],'report':r})
    if any('privacy_screen'in k for k in m['walls']):errors.append({'code':'SEPARATE_SIGHT_SCREEN_REMAINS'})
    placement=check_module_placements(m);errors.extend(placement['errors']);pending.extend(placement['pending'])
    privacy=check_whole_privacy117(m);errors.extend(privacy['errors']);pending.extend(privacy['pending'])
    owners={u['id']:[rect(q)for q in u['ownership']]for u in m['units']}
    owners['COMMON']=[rect(q)for q in m['common_spaces']['lobby']]
    walls={k:rect(q)for k,q in m['walls'].items()}
    fixtures=[(u['id'],k,rect(q))for u in m['units']for k,q in u['fixtures'].items()]
    oe,op=check_operations(m,owners,walls,fixtures);errors.extend(oe);pending.extend(op)
    for a,b in zip(old['units'],m['units']):
        if a['id']!=b['id'] or set(a['activities'])!=set(b['activities']) or set(a['routes'])!=set(b['routes']) or digest(a['fixtures'])!=digest(b['fixtures']):errors.append({'code':'REQUIRED_ACTIVITY_OR_FIXTURE_CHANGED'})
    from geometry114 import cells
    removed=cells(list(old['walls'].values()),list(m['walls'].values()))
    area=sum((rect(q)[2]-rect(q)[0])*(rect(q)[3]-rect(q)[1])for q in removed)
    if digest([packet,trace,baseline_packet,baseline_context])!=before:raise ValueError('Q11_STUDY_INPUT_MUTATED')
    return {'schema':'OPEN_FRONT_BEFORE_AFTER_BOUNDARY_STUDY_V1','model_digest':digest(m),'baseline_digest':digest(old),'origin':origin,'baseline_review_digest':digest(baseline),
        'errors':errors,'pending':sorted(set(pending)),'status':'FAIL_SCOPED'if errors else'UNKNOWN_SCOPED'if pending else'PASS_CLOSET_BOUNDARY_AND_COMPARISON_SCOPED',
        'modules':modules,'placement':placement,'privacy':privacy,'operations':{'errors':oe,'pending':op},
        'before':current_metrics(old),'after':current_metrics(m),'released_physical_material_m2':str(area),'released_material_parts':removed,
        'before_after_claim':'Actual separately verified baseline, not a new-construction waiver or hypothetical predecessor',
        'whole_physical_verified':False,'current_Q11_complete':False,'functional_wall_necessity':'UNKNOWN','accepted':False,'display_allowed':False,'delivery_allowed':False,
        'scope':'Current source-sized usable closet boundaries, fresh whole privacy/operations and real before-after metrics only. Released wall material is not useful area; kitchen wall necessity and full current residual-space quality remain unproved.'}
