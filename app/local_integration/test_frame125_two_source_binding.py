"""Fresh FRAME contract tests; original matrix reports remain separate."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
from frame125_two_source_binding import verify,topology_check,proposal_check,STATUS,TOPOLOGY
from left_right_two_source_binding import digest,check_transport,transport
from producer_provenance import snapshot,require_unchanged
from guard400 import guard
from diagnose_left_right_two import FREEZE
def run():
    paths=['app/local_integration/'+n for n in ('frame125_two_source_binding.py','test_frame125_two_source_binding.py','left_right_two_source_binding.py','compare_left_right_two_topologies.py')]+['.github/workflows/v25-frame125-two-binding.yml']
    snap=snapshot(ROOT,paths);assert guard(FREEZE)==12991
    matrix=json.loads((ROOT/'topology-comparison.json').read_text());frozen=digest(matrix)
    models=[r for r in matrix['cases'] if r['topology']==TOPOLOGY and 'packet'in r]
    assert len(models)==2,'BOTH_PREREGISTERED_FRAME_WITNESSES_REQUIRED'
    positives=[];negative=[];direct=[]
    for row in models:
        r=verify(row['packet'],row['context']);assert r['scoped_verified'],r
        assert r['status']==STATUS and all(r[k]is False for k in ('accepted','qualified','display_allowed','delivery_allowed','whole_physical_verified','whole_functional_verified','historical_schema_replaced','production_supported'))
        assert row['historical_report']['status']=='FAIL' and row['historical_report']['errors']
        positives.append({'input':row['input'],'binding':r,'historical_report_digest':row['completed_report_digests']['historical_report'],'historical_error_count':len(row['historical_report']['errors']),'historical_pending':row['historical_report']['pending'],'current_report_digest':row['completed_report_digests']['current_report'],'current_requirements':row['current_report']['requirements']})
    packet,ctx=models[0]['packet'],models[0]['context']
    def neg(name,fn):
        p,c=copy.deepcopy(packet),copy.deepcopy(ctx);fn(p,c);r=verify(p,c);assert not r['scoped_verified'],name;negative.append({'name':name,'errors':r['errors']})
    neg('wrong_topology',lambda p,c:c['construction_trace']['proposals']['A'].__setitem__('organization_topology','SIDE_ROOTED_SERVICES'))
    neg('proposal_extra',lambda p,c:c['construction_trace']['proposals']['A'].__setitem__('extra',1))
    neg('bed3',lambda p,c:c['construction_trace']['proposals']['A'].__setitem__('bedrooms',3))
    neg('program_bool',lambda p,c:c['construction_trace']['proposals']['A'].__setitem__('bedrooms',True))
    neg('roles_changed',lambda p,c:c['construction_trace']['proposals']['A'].__setitem__('sleep_roles',['double','double']))
    neg('raw26',lambda p,c:c['construction_trace']['raw'].__setitem__('W','26'))
    neg('raw_int',lambda p,c:c['construction_trace']['raw'].__setitem__('W',20))
    neg('core',lambda p,c:p['core'].__setitem__('physical_core_hash','0'*64))
    neg('missing_ops',lambda p,c:p['local_model'].pop('operations'))
    neg('extra_numeric',lambda p,c:p['local_model'].__setitem__('unknown',['1','2']))
    neg('fixture',lambda p,c:p['world_model']['units'][0]['fixtures'][next(iter(p['world_model']['units'][0]['fixtures']))].__setitem__(0,'999'))
    neg('unit_swap',lambda p,c:p['local_model']['units'].reverse())
    neg('wall_alias',lambda p,c:p['local_model']['physical_wall_network']['source_aliases'].pop(next(iter(p['local_model']['physical_wall_network']['source_aliases']))))
    neg('authority',lambda p,c:p.__setitem__('admission_claim',True))
    for name,field,index in [('bath_source_side','bath',2),('shared_wall','kitchen',2),('top_alignment','kitchen',3)]:
        p=copy.deepcopy(ctx['construction_trace']['proposals']['A']);p['rectangles'][field][index]+=.05
        try:topology_check(p,packet['core'])
        except ValueError as ex:
            assert str(ex).startswith('FRAME_');direct.append({'name':name,'errors':[str(ex)],'scope':'DIRECT_TOPOLOGY_NOT_REPLAY'})
        else:raise AssertionError(name)
    sides=[r for r in matrix['cases'] if r['topology']=='SIDE_ROOTED_SERVICES' and 'packet'in r]
    assert sides,'ACTUAL_SIDE_PROPOSAL_REQUIRED_FOR_LABEL_NEGATIVE'
    for row in sides:
        p=copy.deepcopy(row['context']['construction_trace']['proposals']['A']);p['organization_topology']=TOPOLOGY
        try:topology_check(p,row['packet']['core'])
        except ValueError as ex:direct.append({'name':'actual_side_relabel_'+row['input']['W'],'errors':[str(ex)],'scope':'DIRECT_TOPOLOGY_NOT_REPLAY','original_proposal_digest':digest(row['context']['construction_trace']['proposals']['A'])})
        else:raise AssertionError('ACTUAL_SIDE_RELABEL_SATISFIED_FRAME_RELATIONS')
    def target(v,key,change):
        if isinstance(v,dict):
            if key in v:change(v[key]);return True
            return any(target(z,key,change) for z in v.values())
        if isinstance(v,list):return any(target(z,key,change) for z in v)
        return False
    def canonical(m):assert target(m['operations'],'canonical_isometry',lambda q:q['translation'].__setitem__(0,'999'))
    def point(m):assert target(m['operations'],'hand_point',lambda q:q.__setitem__(0,'999'))
    def route(m):
        u=m['units'][0];u['routes'][next(iter(u['routes']))][0][0]='999'
    def rotation(m):
        u=m['units'][0];v=u['fixture_metadata'][next(iter(u['fixture_metadata']))];v['rotation_deg']=(v['rotation_deg']+90)%180
    for name,fn in [('canonical',canonical),('operation_point',point),('route_point',route),('rotation',rotation),('module_source',lambda m:m['module_placements'][0]['module']['bounds'][0].__setitem__(0,'999')),('placement',lambda m:m['module_placements'][0]['transform'].__setitem__('matrix',[[1,0],[0,1]])),('numeric_type',lambda m:m['units'][0]['fixtures'][next(iter(m['units'][0]['fixtures']))].__setitem__(0,1.0))]:
        world=copy.deepcopy(packet['world_model']);fn(world);r=check_transport(packet['local_model'],world,packet['core'])
        assert not r['verified'] and 'INDEPENDENT_D4_TYPED_WORLD_MISMATCH'in r['errors'],(name,r)
        direct.append({'name':name,'errors':r['errors'],'scope':'DIRECT_D4_NOT_REPLAY'})
    try:transport({'unknown':['1','2']},path='test')
    except ValueError as ex:assert 'UNKNOWN_NUMERIC_FIELD'in str(ex);direct.append({'name':'unknown_numeric_role','errors':[str(ex)]})
    else:raise AssertionError('UNKNOWN_NUMERIC_ACCEPTED')
    assert digest(matrix)==frozen;require_unchanged(ROOT,snap);assert guard(FREEZE)==12991
    report={'schema':'FRAME125_TWO_BINDING_TEST_V1','passed':True,'operation_deadline_utc':'2026-11-19T04:49:30Z','positive':positives,'negative':negative,'direct_negative':direct,'source_snapshot':snap,'matrix_digest':frozen,'guard_before':12991,'guard_after':12991,'accepted':False,'delivery_allowed':False,'scope':'Source-derived shape plus shared independent explicit-field D4 only; alias/ledger rebuild depends on pinned sources. Not independent semantic inventory or physical admission; original matrix reports remain unfiltered.'}
    (ROOT/'frame125-two-binding-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('FRAME125_BINDING '+json.dumps({'passed':True,'positive':positives,'negative_count':len(negative),'direct_negative':direct,'guard_before':12991,'guard_after':12991,'accepted':False,'delivery_allowed':False},ensure_ascii=False),flush=True)
if __name__=='__main__':run()
