"""Task 2.1: selected same-version pipeline contract; NOT a generation execution."""
import copy, hashlib, importlib, inspect, json, sys
from pathlib import Path
from public_wln_contract import parse_public, verify_public, engine_raw
from program_profile_registry import lookup
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
FREEZE='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0'
ENGINE_REVISION='faada6a8a1106adfe8a24a5f18dfdf6b550f20a6ecc93d81ce07d47a20d6a279'
APIS={
 'search114.propose':['core','bedrooms','time_limit','variant','fixed_witness','diagnostic_capture','sleep_roles','ordered_macro','topology','organization_profile'],
 'constructor127.frame':['raw','family'],
 'constructor127.build':['raw','family','proposal_a','proposal_b'],
 'constructor127.context':['raw','packet','proposals'],
 'construction_replay127.verify':['model','context'],
 'evaluate_pair127.evaluate':['packet','context'],
 'functional_review.assess':['model','physical_review','source_revision']}
def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def contract():
    return {'schema':'FRONT_REAR_TWO_SAME_VERSION_CONTRACT_V1','task':'2.1',
      'status':'CONTRACT_SELECTED_NOT_EXECUTED',
      'case':{'W':'18','L':'20','n':2,'family':'FRONT_REAR'},
      'program_id':'PROGRAM_2BED_V1','bedrooms_per_unit':2,'sleep_roles':['double','twin'],
      'design_persons_per_unit':4,
      'technical_capacity_profile':'LEGACY_SOURCE_PROGRAM',
      'technical_profile_is_program_approval':False,
      'search':{'topology':'SIDE_ROOTED_SERVICES','organization_profile':'UNRESTRICTED',
        'ordered_macro':False,'variant':0,'fixed_witness':None,'diagnostic_capture':None,
        'requested_count':1,'count_meaning':'Internal bounded study budget, not product output count',
        'no_witness_is_global_infeasibility':False},
      'engine_revision':ENGINE_REVISION,'guard_count':12991,
      'api_parameters':copy.deepcopy(APIS),
      'transport':{'public_keys':['W','L','n'],'original_bytes_required':True,
        'entry_order':['parse_public','verify_public(original_bytes,envelope)','engine_raw'],
        'exact_json_types':True,'nonfinite_allowed':False,
        'live_tuple_transport':'No implicit normalization; any later JSON boundary must be explicit, recorded and digest preserving',
        'hash_is_authentication':False},
      'fields':{
        'raw':{'W':'decimal string','L':'decimal string','n':'strict int 2','requested_count':'strict int 1'},
        'envelope':'Full public contract envelope and original transport SHA256',
        'registry':'Full immutable-copy PROGRAM_2BED_V1 record plus canonical digest',
        'source_hashes':'SHA256 for pinned engine files and selected integration sources, plus actual import paths and signatures',
        'proposals':'Ordered A/B PROPOSAL_ONLY objects; strict int bedrooms=2; roles double,twin; no relabelled three-bedroom proposal',
        'packet':['family','local_model','world_model','core','unit_proposal_hashes','admission_claim'],
        'context':'constructor127.context unmodified CONSTRUCTION_TRACE127_PAIR_V1',
        'replay':'construction_replay127.verify complete result, not admission',
        'physical_report':'evaluate_pair127.evaluate complete result including every error and pending',
        'functional_report':'functional_review.assess on identical world model and identical physical report'},
      'lineage':['original bytes -> envelope -> exact raw',
        'registry digest -> explicit search arguments -> ordered proposals',
        'constructor127 packet -> context -> replay127',
        'same packet/context -> full evaluate_pair127 report',
        'same world model + frozen physical report -> functional_review',
        'freeze every completed report before downstream calls; compare at each stage and final'],
      'quality':'PROFILE_NOT_READY',
      'unresolved':['NET_CAPACITY_PREFILTER','QUALITY_FLOORS','PARETO_ANCHORS','WHOLE_BUNDLE_FUNCTIONAL_CLOSURE'],
      'prohibited':['constructor129','default_three_bedroom_program','historical_schema_replacement','error_or_unknown_filtering','silent_program_reduction'],
      'fresh_model_executed':False,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
def bind_request(body,envelope,program_id):
    verify_public(body,envelope)
    raw=engine_raw(envelope)
    if type(program_id) is not str or program_id!='PROGRAM_2BED_V1':raise ValueError('SELECTED_PROGRAM_ONLY')
    if raw!={'W':'18','L':'20','n':2,'requested_count':1}:raise ValueError('SELECTED_CASE_ONLY')
    p=lookup(program_id)
    if p['approval']['status']!='APPROVED_DESIGN_PROGRAM' or p['sleep_roles']!=['double','twin']:
        raise ValueError('PROGRAM_REGISTRY_CHANGED')
    c=contract()
    return {'schema':'FRONT_REAR_TWO_REQUEST_BINDING_V1','contract_digest':digest(c),
      'raw':raw,'envelope':copy.deepcopy(envelope),'program_registry':p,'program_registry_digest':digest(p),
      'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False}
def audit_sources():
    """Imports/signatures/enums only; never invokes solver, constructor, replay or gates."""
    sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'frontend')]
    from engine114 import revision
    from guard400 import guard
    from producer_provenance import snapshot,require_unchanged
    assert revision()==ENGINE_REVISION and guard(FREEZE)==12991
    files=sorted({k.split('.')[0]+'.py' for k in APIS if not k.startswith('functional_review.')})
    paths=['app/reconstruction357/planha_general150_runtime_work/'+f for f in files]
    paths+=['app/local_integration/'+f for f in ['same_version_front_rear_contract.py','public_wln_contract.py','program_profile_registry.py','functional_review.py','guest_four_route_diagnostic.py','kitchen_guest_review.py','living_connectivity_diagnostic.py']]
    before=snapshot(ROOT,paths);observed={}
    for name,params in APIS.items():
        modname,fn=name.split('.');mod=importlib.import_module(modname);func=getattr(mod,fn)
        base=ROOT/'app/local_integration' if modname=='functional_review' else ENGINE
        expected=(base/(modname+'.py')).resolve()
        assert Path(mod.__file__).resolve()==expected
        assert Path(inspect.getsourcefile(func)).resolve()==expected
        sig=inspect.signature(func)
        assert list(sig.parameters)==params
        observed[name]={'file':str(expected.relative_to(ROOT)),'signature':str(sig)}
    import constructor127,search114
    assert constructor127.FAMILIES==('FRONT_REAR','LEFT_RIGHT')
    defaults=inspect.signature(search114.propose).parameters
    assert defaults['topology'].default=='SIDE_ROOTED_SERVICES'
    assert defaults['organization_profile'].default=='UNRESTRICTED'
    assert defaults['ordered_macro'].default is False
    # Required explicit values and return protocol literals are source audited,
    # not a runtime feasibility or whole-model compatibility claim.
    source=(ENGINE/'search114.py').read_text()
    for token in ['LEGACY_SOURCE_PROGRAM','PROPOSAL_ONLY','SEARCH_TIMEOUT_NO_WITNESS','NO_PROPOSAL_IN_THIS_TOPOLOGY']:
        assert token in source
    require_unchanged(ROOT,before)
    assert revision()==ENGINE_REVISION and guard(FREEZE)==12991
    return {'schema':'SAME_VERSION_SOURCE_API_AUDIT_V1','status':'API_SOURCE_AUDITED_ONLY',
      'contract':contract(),'contract_digest':digest(contract()),'sources':before,'observed_apis':observed,
      'engine_revision':ENGINE_REVISION,'guard_before':12991,'guard_after':12991,
      'solver_called':False,'fresh_model_executed':False,'replay_executed':False,'evaluators_executed':False,
      'accepted':False,'qualified':False,'delivery_allowed':False}
