"""Fresh standalone check for one exact permitted source delta; not whole admission."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import hashlib,inspect
from open_front_kitchen_study import ROOT,ENGINE,SCHEMA
def assess(module):
    from contract114 import digest,S
    import kitchen_module117,checker114,operation_check114
    import open_front_kitchen_study as producer
    for fn,path in [(kitchen_module117.build,ENGINE/'kitchen_module117.py'),
                    (checker114.check_kitchen_module,ENGINE/'checker114.py'),
                    (operation_check114.check_reference_kitchen117,ENGINE/'operation_check114.py'),
                    (producer.build,Path(__file__).with_name('open_front_kitchen_study.py'))]:
        if Path(inspect.getsourcefile(fn)).resolve()!=path.resolve():raise ValueError('STUDY_IMPORT_PATH')
    before=digest(module)
    errors=[];pending=[];evidence={}
    try:
        W=F(module['input_program']['width']);H=F(module['input_program']['depth'])
        base=kitchen_module117.build(W,H)
        baseline=checker114.check_kitchen_module(base)
        if baseline['status']!='PASS_MODULE_SCOPED':raise ValueError('BASE_MODULE_NOT_VERIFIED')
        expected=deepcopy(base)
        expected['schema']=SCHEMA;expected['contract_version']='OPEN_FRONT_CONTROLLED_DELTA_V1'
        del expected['walls']['front.right']
        expected['openings'][0]['rect']=[S(F('.6')),S(F('-.15')),S(W),'0']
        from geometry114 import cells
        apron=cells(base['reserved_approach_gross']+[expected['openings'][0]['rect']],list(expected['walls'].values()))
        expected['unit']['rooms']['public_access']=apron
        expected['unit']['ownership']=deepcopy(expected['unit']['rooms']['kitchen'])+apron
        expected['source_binding']={'producer_sha256':hashlib.sha256(Path(inspect.getsourcefile(producer.build)).read_bytes()).hexdigest(),
            'base_module_digest':digest(base),'base_producer_sha256':base['source_binding']['producer_sha256'],
            'fixture_source_sha256':base['source_binding']['fixture_source_sha256'],
            'delta_contract':'remove front.right; expand existing permanent arch to W and exact threshold floor; retain every other value'}
        if digest(module)!=digest(expected):errors.append('NOT_EXACT_ALLOWED_SOURCE_DELTA')
        walls=[checker114.rect(q) for q in module['walls'].values()]
        host=checker114.rect(module['wall_hosts']['front'])
        openings=module['openings']
        if len(openings)!=1:raise ValueError('ARCH_INVENTORY')
        ap=checker114.rect(openings[0]['rect'])
        if not checker114.covered(host,[q for q in walls if checker114.encloses(host,q)]+[ap]):errors.append('ARCH_HOST_PARTITION')
        if not checker114.encloses(host,ap) or any(checker114.intersects(ap,q) for q in walls):errors.append('ARCH_ACTUAL_CUT')
        u=module['unit'];owner=[checker114.rect(q) for q in u['ownership']]
        if not checker114.covered(ap,owner):errors.append('ARCH_THRESHOLD_FLOOR')
        for role,parts in u['rooms'].items():
            for q in map(checker114.rect,parts):
                if not checker114.covered(q,owner) or any(checker114.intersects(q,w) for w in walls):errors.append('ACTUAL_ROLE_FLOOR:'+role)
        fixtures=[checker114.rect(q) for q in u['fixtures'].values()]
        centers={tuple(map(F,p['center'])) for p in module['external_ports']}
        for k,path in u['routes'].items():
            if tuple(map(F,path[0])) not in centers or tuple(map(F,path[-1]))!=tuple(map(F,u['route_targets'][k])):errors.append('ROUTE_ENDPOINT')
            for q in checker114.sweeps(path):
                if not checker114.covered(q,owner) or any(checker114.intersects(q,r) for r in walls+fixtures):errors.append('ACTUAL_ROUTE_COLLISION')
        fragment=deepcopy(module);fragment['units']=[deepcopy(u)]
        ops=module['operations']['kitchen']
        if len(ops)!=1:raise ValueError('OPERATION_INVENTORY')
        operational=operation_check114.check_reference_kitchen117(fragment,ops[0])
        errors.extend(operational['errors']);pending.extend(operational['pending'])
        evidence={'baseline_digest':digest(base),'baseline_check':baseline,'operations':operational,
            'retained_port_width':module['external_ports'][0]['body_width'],
            'scope':'Exact allowed source delta and fresh local operations/routes. Port/apron not widened. No whole-plan privacy, public routing, functional necessity, source127 or delivery approval.'}
    except (KeyError,ValueError,TypeError,IndexError,ZeroDivisionError) as e:
        errors.append({'code':'STUDY_SCHEMA_OR_GEOMETRY','detail':str(e)})
    if digest(module)!=before:raise ValueError('CHECK_MUTATED_MODULE')
    return {'schema':'OPEN_FRONT_KITCHEN_STUDY_CHECK_V1','module_digest':before,'errors':errors,'pending':pending,
        'status':'FAIL_STUDY' if errors else 'UNKNOWN_STUDY' if pending else 'PASS_MODULE_STUDY_ONLY',
        'evidence':evidence,'whole_model_pass':False,'accepted':False,'display_allowed':False,'delivery_allowed':False}
