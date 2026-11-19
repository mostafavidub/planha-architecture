"""Task 1.2: source-cited programme registry, not a planner or readiness approval."""
import copy,hashlib,inspect,json,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
DOC='https://docs.google.com/document/d/17X8Q5nsiFBmJqAodCQpIfewsDIUeP5eosc3D72ALi3s/edit'
APPROVAL={'url':DOC+'?tab=t.jgj9urck6sd','section':'A9','range':'41570-42072',
 'bundle_range':'43973-44545','meaning':'Design capacity, never actual population.'}
def _record(beds):
    approved=beds in (1,2)
    return {'id':'PROGRAM_'+str(beds)+'BED_V1','version':1,'bedrooms_per_unit':beds,
      'sleep_roles':['double']+['twin']*(beds-1),'design_persons_per_unit':2*beds,
      'capacity_means_actual_population':False,
      'approval':{'status':'APPROVED_DESIGN_PROGRAM' if approved else 'UNAPPROVED_CAPACITY_PROFILE','source':APPROVAL if approved else None,'unapproved_reason':None if approved else 'A9 approval cited here applies only to one-bed/two-person and two-bed/four-person programmes; no approval for three-bed/six-person is claimed.'},
      'source_inventory':{'status':'SOURCE_MODULES_IDENTIFIED_NOT_WHOLE_BUNDLE_VALIDATED',
        'bedroom_module':'bedroom_module116.py','twin_module':'twin_module118.py' if beds>1 else None,
        'assembly_source':'assemble114.py','capacity_source':'public_witness118.py:bind_capacity',
        'double_fixture':{'id':'bed1.bed','size_m':['2','1.6'],'design_places':2},
        'twin_fixtures':[{'source_id':'bed1.'+k,'size_m':['1.9','.9'],'design_places':1} for k in ('bedA','bedB')] if beds>1 else [],
        'closet_per_bedroom':{'size_m':['.6','2.05'],'capacity_for_clothes':'NOT_VERIFIED'},
        'dining_source':'dining_module118.py' if approved else 'UNAPPROVED_SIX_PLACE_PROFILE',
        'dining_distinct_instances':4 if approved else None,
        'dining_table_size_m':['.8','1.2'] if approved else None,
        'dining_chair_size_m':['.5','.5'] if approved else None,
        'living_source':'assemble114.py:117-123;public_witness118.py:bind_capacity',
        'living_distinct_furniture_items':4 if approved else None,
        'living_items':['sofa1','sofa2','armchair1','armchair2'] if approved else [],
        'living_design_body_studies_per_item':1 if approved else None,
        'excess_four_place_bundle_for_one_bedroom':'SOURCE_PRESENT_NOT_AUTOMATICALLY_OPTIMAL' if beds==1 else None},
      'execution_readiness':{
        'status':'EXPERIMENTAL_TWO_BED_ADAPTER_AVAILABLE_NOT_QUALIFIED' if beds==2 else 'ONE_BED_ADAPTER_NOT_AUDITED' if beds==1 else 'BLOCKED_UNAPPROVED_PROFILE',
        'public_execution_supported':False,'constructible_source_branch_exists':approved,
        'source_branch_existence_is_readiness':False,
        'quality_status':'PROFILE_NOT_READY',
        'missing':['SOURCE_BOUND_NET_CAPACITY_PREFILTER','CALIBRATED_ROOM_AND_UNIT_QUALITY_FLOORS','PARETO_ANCHORS','WHOLE_BUNDLE_FUNCTIONAL_CLOSURE']},
      'required_bundle':['sleep','living_seating','dining','clothes_storage','activities','access'],
      'relations':['qualified_adequacy_for_same_design_group','programme_locked_after_geometry','no_silent_bedroom_reduction'],
      'relation_semantics':{'qualified_adequacy_for_same_design_group':'Requirement, not verified fact: every service must adequately serve the same design-person group. Counts of chairs and beds need not be equal. Four source dining places do not change a one-bedroom sleep design capacity of two, do not alone reject it, and do not establish adequacy or optimality.','verification_status':'NOT_VERIFIED'},
      'search_policy':{'source':DOC+'?tab=t.jgj9urck6sd','sections':['AP05','AP06','AP07','AP08','AP09'],
        'range':'38709-40105','budget_is_infeasibility':False,'maximize_bedrooms':False,
        'automatic_fallback':False,'approved_search_eligible':approved,
        'eligible_is_not_execution_ready':True},
      'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
# Stored as immutable serialized data; every lookup parses a fresh independent object.
_REGISTRY_JSON=json.dumps({r['id']:r for r in [_record(1),_record(2),_record(3)]},sort_keys=True,separators=(',',':'))
def lookup(identifier):
    if type(identifier) is not str:raise ValueError('PROGRAM_ID_STRING_REQUIRED')
    data=json.loads(_REGISTRY_JSON)
    if identifier not in data:raise ValueError('UNKNOWN_PROGRAM_PROFILE_NO_FALLBACK')
    return data[identifier]
def list_profiles():
    return [lookup(k) for k in json.loads(_REGISTRY_JSON)]
def approved_profiles():
    return [p for p in list_profiles() if p['approval']['status']=='APPROVED_DESIGN_PROGRAM']
def _digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def audit_sources():
    """Read-only module construction in CI; no whole-plan proposal or planner."""
    sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
    from left_right_two_source_binding import source_state,ENGINE_PIN
    from engine114 import revision
    from guard400 import guard
    import bedroom_module116,twin_module118,dining_module118
    from producer_provenance import snapshot,require_unchanged
    freeze='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0'
    assert guard(freeze)==12991 and revision()==ENGINE_PIN
    before=source_state()
    names=['bedroom_module116.py','twin_module118.py','dining_module118.py','assemble114.py','public_witness118.py','place_module116.py','constructor127.py','search114.py']
    paths=['app/reconstruction357/planha_general150_runtime_work/'+n for n in names]
    paths+=['app/local_integration/program_profile_registry.py']
    snap=snapshot(ROOT,paths)
    for mod in (bedroom_module116,twin_module118,dining_module118):
        assert Path(inspect.getsourcefile(mod.build)).resolve()==(ENGINE/(mod.__name__+'.py')).resolve()
    double=bedroom_module116.build('5.45','3.6')
    twin=twin_module118.build('5.45','4.5')
    dining=dining_module118.build()
    def size(q):return [F(q[2])-F(q[0]),F(q[3])-F(q[1])]
    assert set(double['unit']['fixtures'])=={'bed1.bed','bed1.closet'}
    assert size(double['unit']['fixtures']['bed1.bed'])==[F(2),F('1.6')]
    assert size(double['unit']['fixtures']['bed1.closet'])==[F('.6'),F('2.05')]
    assert set(twin['unit']['fixtures'])=={'bed1.bedA','bed1.bedB','bed1.closet'}
    for k in ('bed1.bedA','bed1.bedB'):
        assert size(twin['unit']['fixtures'][k])==[F('1.9'),F('.9')]
        assert twin['unit']['fixture_metadata'][k]['design_person_places']==1
    assert set(double['unit']['activities'])=={'bed1.bed_front','bed1.bed_back','bed1.closet_front','bed1.changing'}
    assert set(twin['unit']['activities'])=={'bed1.closet_front','bed1.changing','bed1.bedA_front','bed1.bedA_back','bed1.bedB_front','bed1.bedB_back'}
    assert set(dining['fixtures'])=={'table','chair_west','chair_east','chair_front','chair_back'}
    assert {s['id'] for s in dining['seating']['instances']}=={'seat_west','seat_east','seat_front','seat_back'}
    assert len({s['fixture_id'] for s in dining['seating']['instances']})==4
    assert size(dining['fixtures']['table'])==[F('.8'),F('1.2')]
    assert dining['seating']['requested_places']==4 and len(dining['seating']['instances'])==4
    for seat in dining['seating']['instances']:
        assert size(dining['fixtures'][seat['fixture_id']])==[F('.5'),F('.5')]
        assert seat['rise_transfer']['human_transfer_and_support_profile_validated'] is False
    require_unchanged(ROOT,snap);assert source_state()==before and guard(freeze)==12991
    return {'schema':'PROGRAM_REGISTRY_SOURCE_AUDIT_V1','status':'MODULE_INVENTORY_OBSERVED_ONLY',
      'source_snapshot':snap,'engine_revision':ENGINE_PIN,'registry_digest':_digest(json.loads(_REGISTRY_JSON)),
      'modules':{'double':{'hash':_digest(double),'fixtures':double['unit']['fixtures'],'activities':double['unit']['activities']},
         'twin':{'hash':_digest(twin),'fixtures':twin['unit']['fixtures'],'activities':twin['unit']['activities']},
         'dining':{'hash':_digest(dining),'fixtures':dining['fixtures'],'pending':dining['pending']}},
      'single_bedroom_readiness':'SOURCE_BRANCH_EXISTS_NOT_WHOLE_PLAN_OR_ADAPTER_AUDITED',
      'bundle_functional_approval':False,'guard_before':12991,'guard_after':12991,
      'accepted':False,'qualified':False,'delivery_allowed':False,
      'scope':'Literal source fixture/activity inventory only. Module dimensions are source search bounds, not regulations. No whole-model or automatic selection execution.'}
