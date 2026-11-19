"""Negatives for study-only binding; fresh diagnostic packets, never fixtures."""
import copy,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
from left_right_two_source_binding import verify,check_transport,transport,canonical_json,digest,STATUS
from guard400 import guard
from producer_provenance import snapshot,require_unchanged
FREEZE='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0'

def run():
    paths=['app/local_integration/'+n for n in ('left_right_two_source_binding.py','test_left_right_two_source_binding.py','diagnose_left_right_two.py')]+['.github/workflows/v25-left-right-two-binding.yml']
    sources=snapshot(ROOT,paths);assert guard(FREEZE)==12991
    diagnostic=json.loads((ROOT/'left-right-two-diagnostic.json').read_text())
    models=[r for r in diagnostic['cases'] if r['result']=='FRESH_MODEL_DIAGNOSTIC_RECORDED']
    assert models,'NO_FRESH_PROPOSAL_FOR_SCOPED_BINDING_TEST'
    positive=[];negatives=[];transport_negatives=[]
    for row in models:
        dims=row['input'];name='left-right-two-'+dims['W']+'x'+dims['L']+'-packet.json'
        obj=json.loads((ROOT/name).read_text());packet,ctx=obj['packet'],obj['context']
        frozen=digest(obj);r=verify(packet,ctx);positive.append({'input':dims,'report':r})
        assert r['scoped_verified'],r
        assert r['status']==STATUS and not r['accepted'] and not r['delivery_allowed'] and not r['whole_physical_verified']
        assert digest(obj)==frozen
        assert row['original_full_evaluation']['status']=='FAIL'
        assert row['original_full_evaluation']['accepted']is False
    packet,ctx=json.loads((ROOT/('left-right-two-'+models[0]['input']['W']+'x'+models[0]['input']['L']+'-packet.json')).read_text()).values()
    # dictionary insertion is not an authority: bind by explicit names below.
    obj=json.loads((ROOT/('left-right-two-'+models[0]['input']['W']+'x'+models[0]['input']['L']+'-packet.json')).read_text())
    packet,ctx=obj['packet'],obj['context']
    def negate(name,fn):
        p,c=copy.deepcopy(packet),copy.deepcopy(ctx);fn(p,c)
        r=verify(p,c);assert not r['scoped_verified'],name
        negatives.append({'name':name,'errors':r['errors']})
    negate('missing_local_operations',lambda p,c:p['local_model'].pop('operations'))
    negate('extra_local_numeric_field',lambda p,c:p['local_model'].update(unregistered_coordinates=['1','2']))
    negate('bed3_injected',lambda p,c:p['local_model']['units'][0]['fixtures'].update({'bed3.bed':['1','1','2','2']}))
    negate('fixture_world_tamper',lambda p,c:p['world_model']['units'][0]['fixtures'][next(iter(p['world_model']['units'][0]['fixtures']))].__setitem__(0,'999'))
    negate('operation_world_removed',lambda p,c:p['world_model']['operations'].pop(next(iter(p['world_model']['operations']))))
    negate('module_transform',lambda p,c:p['world_model']['module_placements'][0]['transform'].__setitem__('matrix',[[1,0],[0,1]]))
    negate('raw_outside25',lambda p,c:c['construction_trace']['raw'].__setitem__('W','26'))
    negate('raw_type_int',lambda p,c:c['construction_trace']['raw'].__setitem__('W',25))
    negate('raw_n_bool',lambda p,c:c['construction_trace']['raw'].__setitem__('n',True))
    negate('raw_extra',lambda p,c:c['construction_trace']['raw'].__setitem__('additional','x'))
    negate('core_tamper',lambda p,c:p['core'].__setitem__('physical_core_hash','0'*64))
    negate('unit_swap',lambda p,c:p['local_model']['units'].reverse())
    negate('proposal_extra',lambda p,c:c['construction_trace']['proposals']['A'].__setitem__('extra',1))
    negate('proposal_bedrooms_bool',lambda p,c:c['construction_trace']['proposals']['A'].__setitem__('bedrooms',True))
    negate('proposal_sleep_program',lambda p,c:c['construction_trace']['proposals']['A'].__setitem__('sleep_roles',['double','double']))
    negate('geometry_numeric_type',lambda p,c:p['world_model']['units'][0]['fixtures'][next(iter(p['world_model']['units'][0]['fixtures']))].__setitem__(0,1.0))
    negate('context_source_extra',lambda p,c:c['source_files'].__setitem__('not_a_source.py','0'*64))
    negate('admission_true',lambda p,c:p.__setitem__('admission_claim',True))
    # Direct independent transport tests cannot be rejected merely by origin replay.
    for name,mutate in [
        ('world_missing_operations',lambda m:m.pop('operations')),
        ('world_extra_numeric',lambda m:m.update(unregistered_coordinates=['1','2'])),
        ('world_swapped_units',lambda m:m['units'].reverse()),
        ('world_fixture_coordinate',lambda m:m['units'][0]['fixtures'][next(iter(m['units'][0]['fixtures']))].__setitem__(0,'999')),
        ('world_fixture_type',lambda m:m['units'][0]['fixtures'][next(iter(m['units'][0]['fixtures']))].__setitem__(0,1.0)),
        ('world_placement_transform',lambda m:m['module_placements'][0]['transform'].__setitem__('matrix',[[1,0],[0,1]])),
        ('world_operation_removed',lambda m:m['operations'].pop(next(iter(m['operations'])))),
    ]:
        world=copy.deepcopy(packet['world_model']);mutate(world)
        r=check_transport(packet['local_model'],world,packet['core']);assert not r['verified'],name
        transport_negatives.append({'name':name,'errors':r['errors']})
    try:transport({'unregistered_numeric':['1','2']},path='negative')
    except ValueError as ex:
        assert 'UNKNOWN_NUMERIC_FIELD'in str(ex);transport_negatives.append({'name':'unknown_numeric_role','errors':[str(ex)]})
    else:raise AssertionError('UNKNOWN_NUMERIC_NOT_REJECTED')
    require_unchanged(ROOT,sources);assert guard(FREEZE)==12991
    report={'schema':'V25_LEFT_RIGHT_TWO_SOURCE_BINDING_TEST_V1','positive':positive,'negative':negatives,'independent_transport_negative':transport_negatives,'passed':True,'source_snapshot':sources,'guard_before':12991,'guard_after':12991,'status':STATUS,'accepted':False,'delivery_allowed':False,'historical_schema_errors_preserved':True,'scope':'Study-only source-derived shape and independent D4. Fresh packets from same workflow. Original full evaluator FAIL report remains separate and unchanged; no production family support or qualification.'}
    (ROOT/'left-right-two-binding-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('LEFT_RIGHT_BINDING '+json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':run()
