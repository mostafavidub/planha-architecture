"""V25-11 LEFT_RIGHT explicit-two diagnostic. No producer or schema patch."""
import ast,hashlib,inspect,json,sys,time,traceback
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'manifests/WORKTREE_STATE.json').is_file())
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ROOT/'app/local_integration'),str(ROOT/'frontend'),str(ENGINE)]
from guard400 import guard
from producer_provenance import snapshot,require_unchanged
from parametric_worker import prepare
from engine114 import revision
from contract114 import digest
from constructor127 import frame,build,context
from construction_replay127 import verify
from world_inventory125 import examine
from search114 import propose
FREEZE='530cc37c1fa0d2a8be10c3ec09a3b6c3c4a8526245e3d0a2e2e719459dab11e0'
SCHEMA_PIN='59aac9a1e8b17caa40d16aca71a59c4281507b55abf56bb7efc48c5dea0d11ea'
CASES=[('25','25'),('20','20'),('18','20')]
SETTINGS={'bedrooms':2,'sleep_roles':['double','twin'],'time_limit':3,'variant':0,'ordered_macro':False,'topology':'SIDE_ROOTED_SERVICES'}

def run():
    out=ROOT/'left-right-two-diagnostic.json'
    paths=['app/local_integration/'+n for n in ('diagnose_left_right_two.py','explicit_two_bedroom_worker.py','parametric_worker.py','producer_provenance.py','dimension_contract.py')]+['.github/workflows/v25-left-right-two.yml']
    paths+=['app/reconstruction357/planha_general150_runtime_work/'+n for n in ('search114.py','constructor127.py','construction_replay127.py','world_inventory125.py','world_transform125.py','frame_contract125.py','common_core125.py','assemble114.py','world_record_schema129.json')]
    sources=snapshot(ROOT,paths);rev=revision();assert guard(FREEZE)==12991
    for fn,name in ((propose,'search114.py'),(build,'constructor127.py'),(verify,'construction_replay127.py'),(examine,'world_inventory125.py')):
        assert Path(inspect.getsourcefile(fn)).resolve()==(ENGINE/name).resolve()
    schema_bytes=(ENGINE/'world_record_schema129.json').read_bytes()
    assert hashlib.sha256(schema_bytes).hexdigest()==SCHEMA_PIN
    schema=json.loads(schema_bytes)
    worker=(ROOT/'app/local_integration/explicit_two_bedroom_worker.py').read_text()
    tree=ast.parse(worker);constant_attempts=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='append':
            for arg in node.args:
                try:value=ast.literal_eval(arg)
                except (ValueError,TypeError):continue
                if isinstance(value,dict) and value.get('family')=='LEFT_RIGHT':constant_attempts.append({'line':node.lineno,'value':value})
    assert len(constant_attempts)==1 and constant_attempts[0]['value']['state']=='UNSUPPORTED_CURRENT_SOURCE_RECORD_SCHEMA'
    # Explicitly synthetic shape witness, never an assembled model/proposal.
    shape=sorted(['A.bed1','A.bed2','A.dining','A.living','B.bed1','B.bed2','B.dining','B.living'])
    assert shape not in schema['records']['root.room_metadata']
    report={'schema':'V25_LEFT_RIGHT_EXPLICIT_TWO_DIAGNOSTIC_V1','preregistered_inputs':CASES,'settings':SETTINGS,'source_snapshot':sources,'engine_revision_before':rev,'schema_pin':SCHEMA_PIN,'schema_scope':schema['scope'],'worker_constant_policy':constant_attempts,
        'synthetic_shape_probe':{'scope':'Hand-enumerated two-bedroom room_metadata keyset only, not generation or geometry evidence','path':'root.room_metadata','keys':shape,'permitted_keysets':schema['records']['root.room_metadata'],'listed':False},
        'cases':[],'accepted':False,'delivery_allowed':False,'qualified':False,'global_infeasibility_proven':False,'guard_before':12991,
        'scope':'Independent fresh LEFT_RIGHT proposals, original construction/replay and inventory only. Original production worker remains unchanged and unsupported. No whole physical/functional checker, qualification, repair, or schema extension.'}
    def save():out.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    save()
    for W,L in CASES:
        row={'input':{'W':W,'L':L,'n':2,'requested_count':1,'program':{'bedrooms_per_unit':2}},'stage':'prepare','accepted':False}
        report['cases'].append(row);started=time.monotonic()
        try:
            envelope,raw=prepare(json.dumps(row['input'],separators=(',',':')).encode())
            row.update(raw=raw,request_digest=envelope['canonical_request_digest'],stage='frame')
            core,_=frame(raw,'LEFT_RIGHT');row['core_digest']=digest(core);row['stage']='proposal'
            proposal=propose(core,**SETTINGS);row.update(proposal=proposal,proposal_digest=digest(proposal),proposal_status=proposal.get('status'))
            if proposal.get('status')!='PROPOSAL_ONLY':
                row['result']='NO_FRESH_MODEL';row['schema_failure_observed_on_fresh_model']=False
            else:
                row['stage']='constructor'
                packet=build(raw,'LEFT_RIGHT',proposal,proposal)
                ctx=context(raw,packet,{'A':proposal,'B':proposal})
                immutable=digest([raw,proposal,packet,ctx])
                row.update(local_model_digest=digest(packet['local_model']),world_model_digest=digest(packet['world_model']),context_digest=digest(ctx),construction_trace=ctx['construction_trace'],stage='replay')
                replay=verify(packet['world_model'],ctx);row['replay']=replay
                assert immutable==digest([raw,proposal,packet,ctx])
                row['stage']='world_inventory';inventory=examine(packet['local_model'],packet['world_model'],packet['core']);row['world_inventory']=inventory
                assert immutable==digest([raw,proposal,packet,ctx])
                mismatch_paths=sorted(set(e.split(':',1)[1] for e in inventory['errors'] if e.startswith('UNKNOWN_RECORD_FIELDS:')))
                evidence=[]
                def walk(v,path='root',key='',frame_name=''):
                    if key in ('module','source_contract','rotation_source133'):return
                    if isinstance(v,dict):
                        keys=sorted(k for k in v if not(path=='root' and k=='frame_binding125'))
                        if path in mismatch_paths and keys not in schema['records'].get(path,[]):
                            evidence.append({'frame':frame_name,'path':path,'actual_keys':keys,'allowed_keysets':schema['records'].get(path,[])})
                        for k,z in v.items():
                            if path=='root' and k=='frame_binding125':continue
                            walk(z,path+'.'+k,k,frame_name)
                    elif isinstance(v,list):
                        for z in v:walk(z,path+'[]','',frame_name)
                walk(packet['local_model'],frame_name='local');walk(packet['world_model'],frame_name='world')
                row.update(mismatch_paths=mismatch_paths,mismatch_evidence=evidence,schema_failure_observed_on_fresh_model=bool(mismatch_paths),result='FRESH_MODEL_DIAGNOSTIC_RECORDED')
                # Preserve full fresh evidence separately, not as production history.
                (ROOT/('left-right-two-'+W+'x'+L+'-packet.json')).write_text(json.dumps({'packet':packet,'context':ctx},ensure_ascii=False))
        except Exception as ex:
            row.update(result='DIAGNOSTIC_STAGE_EXCEPTION',exception_type=type(ex).__name__,exception=str(ex),traceback=traceback.format_exc())
        finally:
            row['elapsed_seconds']=time.monotonic()-started;save()
            require_unchanged(ROOT,sources);assert revision()==rev and guard(FREEZE)==12991
    report.update(completed=True,guard_after=12991,engine_revision_after=revision(),fresh_models=sum(r['result']=='FRESH_MODEL_DIAGNOSTIC_RECORDED' for r in report['cases']))
    save()
    concise={**report,'cases':[{k:v for k,v in r.items() if k not in ('proposal','construction_trace','mismatch_evidence')} for r in report['cases']]}
    print('LEFT_RIGHT_TWO '+json.dumps(concise,ensure_ascii=False),flush=True)
    return report
if __name__=='__main__':run()
