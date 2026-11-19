"""Preregistered nonsquare FRAME125 source-family study; no admission."""
import copy,inspect,json,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend'),str(ENGINE)]
from diagnose_left_right_two import prepare,frame,build,context,verify,examine,evaluate_pair,propose,FREEZE,SCHEMA_PIN
from left_right_two_source_binding import digest,source_state,exact,check_transport,canonical_json,ENGINE_PIN
from frame125_two_source_binding import verify as source_binding
from left_right_two_evidence_bundle import require_reports_unchanged,CURRENT_UNKNOWN,LOCAL_FILES
from producer_provenance import snapshot,require_unchanged
from functional_review import assess
from guard400 import guard
CASES=[(w,l,'FRAME125_SERVICE_SIDE') for w,l in [('18','20'),('20','18'),('20','25'),('25','20')]]
SETTINGS={'bedrooms':2,'sleep_roles':['double','twin'],'time_limit':3,'variant':0,'ordered_macro':False,'organization_profile':'UNRESTRICTED'}
def transport_boundary(packet,ctx):
    findings=[]
    def walk(v,path):
        if type(v)not in(dict,list,str,int,float,bool,type(None)):
            findings.append({'path':path,'type':type(v).__name__})
        if type(v)is dict:
            for k,z in v.items():walk(z,path+'.'+k)
        elif type(v)in(list,tuple):
            for i,z in enumerate(v):walk(z,path+'['+str(i)+']')
    walk(packet,'packet');walk(ctx,'context')
    assert all(r['type']=='tuple' for r in findings),'UNEXPECTED_LIVE_NONJSON_TYPE:'+str(findings)
    before=digest([packet,ctx]);p,c=canonical_json([packet,ctx]);after=digest([p,c])
    assert before==after,'JSON_TRANSPORT_VALUE_CHANGE'
    return p,c,{'scope':'Explicit same JSON serialization boundary as prior artifact-fed FRAME tests; tuples become arrays only, no numeric/string coercion. Not origin or geometry repair.','live_non_json_paths':findings,'digest_before':before,'digest_after':after}
def run():
    paths=['app/local_integration/'+n for n in set(LOCAL_FILES+['diagnose_left_right_two.py','study_frame125_two_nonsquare.py','parametric_worker.py','dimension_contract.py','frame125_two_source_binding.py'])]
    paths+=['.github/workflows/v25-frame125-two-nonsquare.yml']
    sources=snapshot(ROOT,paths);engine=source_state();assert guard(FREEZE)==12991
    for fn,path in [(propose,ENGINE/'search114.py'),(build,ENGINE/'constructor127.py'),(verify,ENGINE/'construction_replay127.py'),(evaluate_pair,ENGINE/'evaluate_pair127.py'),(assess,ROOT/'app/local_integration/functional_review.py')]:
        assert Path(inspect.getsourcefile(fn)).resolve()==path.resolve()
    report={'schema':'V25_FRAME125_TWO_NONSQUARE_V1','operation_deadline_utc':'2026-11-19T04:49:30Z','preregistered_cases':CASES,'settings':SETTINGS,'source_snapshot':sources,'engine_revision':ENGINE_PIN,'schema_pin':SCHEMA_PIN,'guard_before':12991,'cases':[],'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'production_supported':False,'global_infeasibility_proven':False,'scope':'Original unfiltered constructor/replay/inventory/pair/current. Separate FRAME125 source-derived shape/D4 contract. Exact nonsquare local/world axes, no retries or candidate selection.'}
    def save(): (ROOT/'frame125-two-nonsquare.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    save()
    for W,L,topology in CASES:
        row={'input':{'W':W,'L':L,'n':2,'requested_count':1,'program':{'bedrooms_per_unit':2}},'topology':topology,'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'stage':'prepare'}
        report['cases'].append(row);started=time.monotonic();frozen={};bundle=None
        def check():
            require_reports_unchanged(row,frozen)
            if bundle is not None:assert digest(bundle)==row['input_bundle_digest'],'INPUT_MUTATION'
            require_unchanged(ROOT,sources);assert source_state()==engine and guard(FREEZE)==12991
        def capture(name,value):
            row[name]=value;frozen[name]=digest(value);check()
        try:
            envelope,raw=prepare(json.dumps(row['input'],separators=(',',':')).encode())
            row.update(raw=raw,request_digest=envelope['canonical_request_digest'])
            core,axes=frame(raw,'LEFT_RIGHT');row['core_digest']=digest(core)
            assert list(map(str,axes))==[L,W]
            assert exact(core['solver_inputs'],[L,W,2]) and exact(core['physical_core_model']['inputs'],[W,L,2])
            row['axis_evidence']={'raw':[W,L,2],'local_solver':core['solver_inputs'],'world_core':core['physical_core_model']['inputs'],'matrix':core['world_from_local']}
            assert exact(core['world_from_local'],{'matrix':[[0,1],[1,0]],'translation':['0','0']})
            row['stage']='proposal';proposal=propose(core,topology=topology,**SETTINGS)
            capture('proposal',proposal);row['proposal_status']=proposal.get('status')
            if proposal.get('status')!='PROPOSAL_ONLY':
                row['result']='NO_FRESH_MODEL'
            else:
                row['stage']='constructor';packet=build(raw,'LEFT_RIGHT',proposal,proposal);ctx=context(raw,packet,{'A':proposal,'B':proposal})
                packet,ctx,boundary=transport_boundary(packet,ctx);row['json_transport_boundary']=boundary
                bundle=[raw,proposal,packet,ctx];row['input_bundle_digest']=digest(bundle)
                row.update(local_model_digest=digest(packet['local_model']),world_model_digest=digest(packet['world_model']),context_digest=digest(ctx))
                assert exact(packet['local_model']['inputs'],[L,W,2]) and exact(packet['world_model']['inputs'],[W,L,2])
                capture('packet',packet);capture('context',ctx)
                row['stage']='replay';capture('replay',verify(packet['world_model'],ctx))
                row['stage']='inventory';capture('world_inventory',examine(packet['local_model'],packet['world_model'],packet['core']))
                row['stage']='binding'
                capture('source_binding',source_binding(packet,ctx))
                assert row['source_binding']['scoped_verified'],row['source_binding']['errors']
                negative=[]
                p,c=copy.deepcopy(packet),copy.deepcopy(ctx)
                rr=c['construction_trace']['raw'];rr['W'],rr['L']=rr['L'],rr['W']
                rejected=source_binding(p,c);assert not rejected['scoped_verified'];negative.append({'name':'swapped_raw','errors':rejected['errors']})
                p,c=copy.deepcopy(packet),copy.deepcopy(ctx);p['core']['solver_inputs']=[W,W,2]
                rejected=source_binding(p,c);assert not rejected['scoped_verified'];negative.append({'name':'square_core_assumption','errors':rejected['errors']})
                world=copy.deepcopy(packet['world_model']);world['inputs']=[W,W,2]
                rejected=check_transport(packet['local_model'],world,packet['core']);assert not rejected['verified']
                assert 'INDEPENDENT_D4_TYPED_WORLD_MISMATCH'in rejected['errors']
                negative.append({'name':'direct_square_world_input','errors':rejected['errors'],'scope':'DIRECT_D4_NOT_REPLAY'})
                capture('axis_negative',negative)
                row['stage']='original_pair'
                try:capture('historical_report',evaluate_pair(packet,ctx))
                except Exception as ex:
                    row['historical_exception']={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()};check()
                if 'historical_report'in row:
                    historical=row['historical_report'];assert historical['model_hash']==row['world_model_digest']
                    row['stage']='current'
                    try:
                        current=assess(packet['world_model'],historical,ENGINE_PIN)
                        capture('current_report',current)
                        row['current_validation']='PENDING';check()
                        assert current['physical_review_digest']==frozen['historical_report']
                        assert current['model_digest']==row['world_model_digest'] and current['source_revision']==ENGINE_PIN
                        assert all(current[k]is False for k in ('accepted','qualified','display_allowed','delivery_allowed'))
                        assert {r['id'] for r in current['requirements'] if r['state']=='UNKNOWN'}>=CURRENT_UNKNOWN
                        row['current_validation']='BOUND_AND_FAIL_CLOSED'
                    except Exception as ex:
                        row['current_validation']='FAILED_CLOSED'
                        row['current_exception']={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()};check()
                row['result']='FRESH_EVIDENCE_RECORDED_NO_ADMISSION'
        except Exception as ex:
            row.update(result='DIAGNOSTIC_STAGE_EXCEPTION',exception={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()})
        finally:
            checkpoint_failure=None
            try:check()
            except Exception as ex:
                checkpoint_failure=ex
                row.update(result='CHECKPOINT_INTEGRITY_FAILED_CLOSED',checkpoint_exception={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()})
            row['completed_report_digests']=copy.deepcopy(frozen);row['elapsed_seconds']=time.monotonic()-started
            if bundle is not None:row['input_bundle_digest_after']=digest(bundle)
            save()
            if checkpoint_failure is not None:raise checkpoint_failure
    report.update(completed=True,guard_after=12991,source_unchanged=True);save()
    summaries=[]
    for row in report['cases']:
        h=row.get('historical_report',{});freq={}
        for e in h.get('errors',[]):
            k=e.split(':')[0] if isinstance(e,str) else e.get('code','UNKNOWN');freq[k]=freq.get(k,0)+1
        summaries.append({'input':row['input'],'topology':row['topology'],'result':row['result'],'proposal_status':row.get('proposal_status'),'model_digest':row.get('world_model_digest'),'replay':row.get('replay',{}).get('verified'),'binding':row.get('source_binding',{}).get('status'),'historical_status':h.get('status'),'error_count':len(h.get('errors',[])),'error_codes':freq,'pending':h.get('pending',[]),'current_requirements':row.get('current_report',{}).get('requirements',[]),'exception':row.get('exception'),'historical_exception':row.get('historical_exception'),'current_exception':row.get('current_exception'),'axis_evidence':row.get('axis_evidence'),'axis_negative':row.get('axis_negative'),'json_transport_boundary':row.get('json_transport_boundary')})
    print('FRAME125_NONSQUARE '+json.dumps({'cases':summaries,'guard_before':12991,'guard_after':12991,'accepted':False,'delivery_allowed':False,'completed':True},ensure_ascii=False),flush=True)
if __name__=='__main__':run()
