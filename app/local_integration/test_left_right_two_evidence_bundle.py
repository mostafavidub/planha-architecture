"""Fresh integration regression, no admission or historical-error suppression."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend'),str(ROOT/'app/reconstruction357/planha_general150_runtime_work')]
from left_right_two_evidence_bundle import evaluate,CURRENT_UNKNOWN,require_reports_unchanged
from left_right_two_source_binding import digest
from producer_provenance import snapshot,require_unchanged
from guard400 import guard
FREEZE='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0'
def run():
    paths=['app/local_integration/'+n for n in ('left_right_two_evidence_bundle.py','test_left_right_two_evidence_bundle.py')]+['.github/workflows/v25-left-right-two-evidence.yml']
    sources=snapshot(ROOT,paths);assert guard(FREEZE)==12991
    diag=json.loads((ROOT/'left-right-two-diagnostic.json').read_text())
    fresh=[r for r in diag['cases'] if r['result']=='FRESH_MODEL_DIAGNOSTIC_RECORDED']
    assert fresh,'NO_FRESH_PROPOSAL_FOR_BUNDLE'
    positives=[];negative=[];synthetic_report_mutations=[]
    # Synthetic branch test only: same production ledger, no imported callable
    # replacement, fake geometry, or origin claim. Downstream mutates a report.
    for section in ('source_derived_shape_d4','historical_full_report','named_requirement_inventory','current_functional_report'):
        holder={section:{'errors':[],'pending':['UNKNOWN']}}
        frozen={section:digest(holder[section])}
        require_reports_unchanged(holder,frozen)
        def downstream(report):
            report['pending'].clear()
        downstream(holder[section])
        try:
            require_reports_unchanged(holder,frozen)
        except ValueError as ex:
            assert str(ex)=='COMPLETED_REPORT_MUTATION:'+section
            synthetic_report_mutations.append({'section':section,'error':str(ex),'scope':'SYNTHETIC_LEDGER_BRANCH_NOT_GEOMETRY'})
        else:raise AssertionError('REPORT_MUTATION_NOT_DETECTED')

    for row in fresh:
        w,l=row['input']['W'],row['input']['L'];obj=json.loads((ROOT/('left-right-two-'+w+'x'+l+'-packet.json')).read_text())
        before=digest(obj);result=evaluate(obj['packet'],obj['context'])
        (ROOT/('left-right-two-bundle-'+w+'x'+l+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2))
        assert result['completed'],result['errors']
        require_reports_unchanged(result,result['completed_report_digests'])
        assert result['status']=='FAIL' and result['historical_compatibility']=='BLOCKED'
        assert result['historical_report_digest_before_current']==result['historical_report_digest_after_current']
        assert result['current_functional_report']['physical_review_digest']==result['historical_report_digest_before_current']
        assert result['historical_full_report']['errors']==row['original_full_evaluation']['errors']
        assert result['historical_full_report']['pending']==row['original_full_evaluation']['pending']
        assert result['historical_full_report']['status']=='FAIL'
        assert all(result[k]is False for k in ('accepted','qualified','display_allowed','delivery_allowed','whole_physical_verified','whole_functional_verified','production_supported'))
        assert result['input_bundle_digest']==result['input_bundle_digest_after'] and digest(obj)==before
        raw='VARIABLE_ROOM_PROGRAM_CAPACITY_AND_SPATIAL_QUALITY_NOT_EVALUATED'
        physical=result['historical_full_report']
        assert raw in physical['original_pending'] and raw in physical['not_evaluated']
        assert any(r.get('code')==raw for r in physical['out_of_scope'])
        assert any(r['value']==raw for r in result['pending_obligations'])
        rows=result['current_functional_report']['requirements']
        assert {r['id'] for r in rows if r['state']=='UNKNOWN'}>=CURRENT_UNKNOWN
        positives.append({'input':row['input'],'model_hash':result['model_hash'],'binding':result['source_derived_shape_d4']['status'],'historical_errors':len(result['historical_full_report']['errors']),'historical_pending':result['historical_full_report']['pending'],'checker_errors':physical['errors'],'checker_pending':physical['pending'],'raw_pending_preserved':raw,'named_count':result['named_requirement_inventory']['count'],'current_requirements':rows,'stages':result['stages'],'status':result['status']})
    for name,mutate in [
        ('raw_outside25',lambda p,c:c['construction_trace']['raw'].__setitem__('W','26')),
        ('world_unknown_field',lambda p,c:p['world_model'].__setitem__('unknown',[1,2])),
        ('wrong_family',lambda p,c:p.__setitem__('family','FRONT_REAR')),
        ('context_trace_model_hash',lambda p,c:c['construction_trace'].__setitem__('model_hash','0'*64))
    ]:
        p,c=copy.deepcopy(obj['packet']),copy.deepcopy(obj['context']);mutate(p,c);r=evaluate(p,c)
        assert not r['completed'] and r['status']=='EVIDENCE_BUNDLE_FAILED_CLOSED'
        assert 'original_evaluate_pair127_with_original_physical_named'not in r['stages']
        negative.append({'name':name,'errors':r['errors'],'binding_errors':r['source_derived_shape_d4']['errors'],'stages':r['stages']})
    require_unchanged(ROOT,sources);assert guard(FREEZE)==12991
    report={'schema':'V25_LEFT_RIGHT_TWO_EVIDENCE_BUNDLE_TEST_V1','passed':True,'positive':positives,'negative':negative,'synthetic_report_mutations':synthetic_report_mutations,'source_snapshot':sources,'guard_before':12991,'guard_after':12991,'accepted':False,'delivery_allowed':False,'scope':'Integration evidence only; every original report and current UNKNOWN retained. No production support or historical schema replacement.'}
    (ROOT/'left-right-two-evidence-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('LEFT_RIGHT_EVIDENCE '+json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':run()
