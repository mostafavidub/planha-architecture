"""Deterministic isolated world origin; never constructor127 provenance or admission."""
from pathlib import Path
import inspect
from fractions import Fraction as F
from copy import deepcopy
from contract114 import parse,core_first,digest
from open_front_kitchen_study import ROOT,ENGINE
FILES=['open_front_world_origin.py','open_front_world_assembly.py','open_front_kitchen_study.py','open_front_kitchen_check.py','open_front_kitchen_place.py']
def bindings():
    from producer_provenance import snapshot
    import open_front_world_assembly as assembly,open_front_kitchen_study as producer,open_front_kitchen_place as placer,open_front_kitchen_check as checker
    for fn,name in [(assembly.assemble,'open_front_world_assembly.py'),(producer.build,'open_front_kitchen_study.py'),(placer.install,'open_front_kitchen_place.py'),(checker.assess,'open_front_kitchen_check.py'),(parse,'contract114.py'),(core_first,'contract114.py')]:
        expected=(ENGINE/name) if name=='contract114.py' else Path(__file__).with_name(name)
        if Path(inspect.getsourcefile(fn)).resolve()!=expected.resolve():raise ValueError('NEW_WORLD_IMPORT_PATH')
    return snapshot(ROOT,['app/local_integration/'+n for n in FILES])
def construct(raw,proposals):
    from open_front_world_assembly import assemble
    if set(proposals)!= {'A','B'}:raise ValueError('EXPLICIT_PAIR_REQUIRED')
    for p in proposals.values():
        if p.get('bedrooms')!=2 or p.get('sleep_roles')!=['double','twin']:raise ValueError('STUDY_PROGRAM_SCOPE')
    w,l,n=parse(raw)
    if not(5<=w<=25 and 5<=l<=25)or n!=2:raise ValueError('STUDY_INPUT_DOMAIN')
    core=core_first(w,l)
    if core is None:raise ValueError('STUDY_CORE_UNAVAILABLE')
    m=assemble(w,l,core,proposals['A'],unit_proposals=proposals)
    return {'raw_input_digest':digest(raw),'family':'FRONT_REAR','world_model':m,'core':core,'admission_claim':False}
def build(raw,proposals):
    from engine114 import revision
    from producer_provenance import require_unchanged
    sources=bindings();rev=revision();packet=construct(raw,deepcopy(proposals))
    trace={'schema':'OPEN_FRONT_WORLD_ORIGIN_V1','raw':raw,'family':'FRONT_REAR','proposals':deepcopy(proposals),'proposal_hashes':{u:digest(p)for u,p in proposals.items()},'model_digest':digest(packet['world_model']),'core_digest':digest(packet['core']),'sources':sources,'frozen_revision':rev,'qualified':False,'delivery_allowed':False}
    require_unchanged(ROOT,sources)
    if revision()!=rev:raise ValueError('FROZEN_SOURCE_CHANGED')
    return packet,trace
def verify(packet,trace):
    from engine114 import revision
    from producer_provenance import require_unchanged
    sources=bindings()
    if trace.get('schema')!='OPEN_FRONT_WORLD_ORIGIN_V1' or trace.get('family')!='FRONT_REAR':raise ValueError('NEW_ORIGIN_SCHEMA')
    if trace.get('sources')!=sources or trace.get('frozen_revision')!=revision():raise ValueError('NEW_ORIGIN_SOURCES')
    if trace.get('qualified')is not False or trace.get('delivery_allowed')is not False:raise ValueError('NO_STUDY_ADMISSION')
    rebuilt=construct(trace['raw'],deepcopy(trace['proposals']))
    if packet!=rebuilt:raise ValueError('NEW_ORIGIN_REPLAY_MISMATCH')
    if trace['model_digest']!=digest(rebuilt['world_model']) or trace['core_digest']!=digest(rebuilt['core']) or trace['proposal_hashes']!={u:digest(p)for u,p in trace['proposals'].items()}:raise ValueError('NEW_ORIGIN_DIGEST')
    require_unchanged(ROOT,sources)
    if trace['frozen_revision']!=revision():raise ValueError('FROZEN_SOURCE_CHANGED')
    return {'origin_verified':True,'scope':'Deterministic new study source replay only, not physical/function acceptance','whole_model_pass':False,'accepted':False,'delivery_allowed':False}
