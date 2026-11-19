"""Preregistered original-source topology comparison; no admission or schema extension."""
import copy,inspect,json,sys,time,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend'),str(ENGINE)]
from diagnose_left_right_two import prepare,frame,build,context,verify,examine,evaluate_pair,propose,FREEZE,SCHEMA_PIN
from left_right_two_source_binding import digest,source_state,verify as source_binding,ENGINE_PIN
from left_right_two_evidence_bundle import require_reports_unchanged,CURRENT_UNKNOWN,LOCAL_FILES
from producer_provenance import snapshot,require_unchanged
from functional_review import assess
from guard400 import guard
CASES=[(w,l,t) for w,l in [('20','20'),('25','25')] for t in ('SIDE_ROOTED_SERVICES','FRAME125_SERVICE_SIDE')]
SETTINGS={'bedrooms':2,'sleep_roles':['double','twin'],'time_limit':3,'variant':0,'ordered_macro':False,'organization_profile':'UNRESTRICTED'}
def run():
    paths=['app/local_integration/'+n for n in set(LOCAL_FILES+['diagnose_left_right_two.py','compare_left_right_two_topologies.py','parametric_worker.py','dimension_contract.py'])]
    paths+=['.github/workflows/v25-left-right-two-topologies.yml']
    sources=snapshot(ROOT,paths);engine=source_state();assert guard(FREEZE)==12991
    for fn,path in [(propose,ENGINE/'search114.py'),(build,ENGINE/'constructor127.py'),(verify,ENGINE/'construction_replay127.py'),(evaluate_pair,ENGINE/'evaluate_pair127.py'),(assess,ROOT/'app/local_integration/functional_review.py')]:
        assert Path(inspect.getsourcefile(fn)).resolve()==path.resolve()
    report={'schema':'V25_EXPLICIT_TWO_TOPOLOGY_COMPARISON_V1','operation_deadline_utc':'2026-11-19T04:49:30Z','preregistered_cases':CASES,'settings':SETTINGS,'source_snapshot':sources,'engine_revision':ENGINE_PIN,'schema_pin':SCHEMA_PIN,'guard_before':12991,'cases':[],'accepted':False,'qualified':False,'display_allowed':False,'delivery_allowed':False,'production_supported':False,'global_infeasibility_proven':False,'scope':'Original unfiltered constructor/replay/inventory/pair/current. Source-derived shape/D4 only for original SIDE_ROOTED contract; FRAME125 binding NOT_APPLICABLE. No retries or candidate selection.'}
    def save(): (ROOT/'topology-comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
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
            core,_=frame(raw,'LEFT_RIGHT');row['core_digest']=digest(core)
            row['stage']='proposal';proposal=propose(core,topology=topology,**SETTINGS)
            capture('proposal',proposal);row['proposal_status']=proposal.get('status')
            if proposal.get('status')!='PROPOSAL_ONLY':
                row['result']='NO_FRESH_MODEL'
            else:
                row['stage']='constructor';packet=build(raw,'LEFT_RIGHT',proposal,proposal);ctx=context(raw,packet,{'A':proposal,'B':proposal})
                bundle=[raw,proposal,packet,ctx];row['input_bundle_digest']=digest(bundle)
                row.update(local_model_digest=digest(packet['local_model']),world_model_digest=digest(packet['world_model']),context_digest=digest(ctx))
                capture('packet',packet);capture('context',ctx)
                row['stage']='replay';capture('replay',verify(packet['world_model'],ctx))
                row['stage']='inventory';capture('world_inventory',examine(packet['local_model'],packet['world_model'],packet['core']))
                row['stage']='binding'
                capture('source_binding',source_binding(packet,ctx) if topology=='SIDE_ROOTED_SERVICES' else {'status':'NOT_APPLICABLE_CONTRACT_TOPOLOGY','scoped_verified':False,'reason':'Unmodified binding contract permits SIDE_ROOTED_SERVICES only; no schema or topology expansion.'})
                row['stage']='original_pair'
                try:capture('historical_report',evaluate_pair(packet,ctx))
                except Exception as ex:
                    row['historical_exception']={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()};check()
                if 'historical_report'in row:
                    historical=row['historical_report'];assert historical['model_hash']==row['world_model_digest']
                    row['stage']='current'
                    try:
                        current=assess(packet['world_model'],historical,ENGINE_PIN);check()
                        assert current['physical_review_digest']==frozen['historical_report']
                        assert current['model_digest']==row['world_model_digest'] and current['source_revision']==ENGINE_PIN
                        assert all(current[k]is False for k in ('accepted','qualified','display_allowed','delivery_allowed'))
                        assert {r['id'] for r in current['requirements'] if r['state']=='UNKNOWN'}>=CURRENT_UNKNOWN
                        capture('current_report',current)
                    except Exception as ex:
                        row['current_exception']={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()};check()
                row['result']='FRESH_EVIDENCE_RECORDED_NO_ADMISSION'
        except Exception as ex:
            row.update(result='DIAGNOSTIC_STAGE_EXCEPTION',exception={'type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()})
        finally:
            check();row['completed_report_digests']=copy.deepcopy(frozen);row['elapsed_seconds']=time.monotonic()-started
            if bundle is not None:row['input_bundle_digest_after']=digest(bundle)
            save()
    report.update(completed=True,guard_after=12991,source_unchanged=True);save()
    summaries=[]
    for row in report['cases']:
        h=row.get('historical_report',{});freq={}
        for e in h.get('errors',[]):
            k=e.split(':')[0] if isinstance(e,str) else e.get('code','UNKNOWN');freq[k]=freq.get(k,0)+1
        summaries.append({'input':row['input'],'topology':row['topology'],'result':row['result'],'proposal_status':row.get('proposal_status'),'model_digest':row.get('world_model_digest'),'replay':row.get('replay',{}).get('verified'),'binding':row.get('source_binding',{}).get('status'),'historical_status':h.get('status'),'error_count':len(h.get('errors',[])),'error_codes':freq,'pending':h.get('pending',[]),'current_requirements':row.get('current_report',{}).get('requirements',[]),'exception':row.get('exception'),'historical_exception':row.get('historical_exception'),'current_exception':row.get('current_exception')})
    print('TOPOLOGY_COMPARISON '+json.dumps({'cases':summaries,'guard_before':12991,'guard_after':12991,'accepted':False,'delivery_allowed':False,'completed':True},ensure_ascii=False),flush=True)
if __name__=='__main__':run()
