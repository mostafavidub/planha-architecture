"""P38 offline diagnostic crosswalk; not an assessor, gate, or export surface."""
import hashlib
import io
import json
import re
import zipfile

P, G, L, W = ('CURRENT_PROGRAM_SUITABILITY', 'KITCHEN_GUEST_PATH_SEPARATION',
              'CONTINUOUS_USEFUL_LIVING', 'NONFUNCTIONAL_WALL_EXCLUSION')
SCHEMAS = dict(zip((P,G,L,W), ('CURRENT_PROGRAMME_SOURCE_EVALUATION_V1',
    'SOURCE_BOUND_FOUR_GUEST_ROUTES_V1', 'CURRENT_LIVING_SOURCE_EVIDENCE_V1',
    'SOURCE_WALL_FUNCTION_EVIDENCE_V1')))
AUTH = ('accepted','qualified','display_allowed','delivery_allowed')
IDS = dict(zip((P,G,L,W), (
    'PROGRAM_IDENTITY PROGRAM_CAPACITY PROGRAM_ALTERNATIVES PROGRAM_QUALITY_FLOOR PROGRAM_PREFILTER PROGRAM_BUNDLE_USE PROGRAM_SERVICE_MINIMA'.split(),
    'GUEST_FOUR_ROUTES GUEST_WORK_EXCLUSION GUEST_FIRST_LIVING GUEST_PRIVATE_ACCESS GUEST_KITCHEN_LABEL'.split(),
    'LIVING_SOURCE_SEATS LIVING_FLOOR_CONTINUITY LIVING_USEFUL_AREA LIVING_SHORTER_ALTERNATIVE LIVING_GROUP_USE'.split(),
    'WALL_SOURCE_INVENTORY WALL_VIEW_ONLY WALL_ALIAS_MATERIAL WALL_ALTERNATIVE WALL_PRIVACY_TARGETS CORE_ENGINEERING'.split())))
REF = '09403734568eecd9125284e610dd1163b41118a9'
TREE = 'dd5af4f6791e0a41cb5b5c8a51b54b992b3712ae'
CAT = 'specs/V25_TASK_3_1_CURRENT_FUNCTIONAL_CRITERIA.json'
CAT_BLOB = 'df289f3a072083afc26247970e0804ee69331ede'
DEC_PATH = 'app/local_integration/current_four_decision.py'
ORIGINALS = set('coordinate_precision functional model_transport physical preconstruction_fit proposal_transport replay source_audit'.split())
ROUTES = ('entry_living','entry_dining','entry_WC','living_dining')
DIR = 'app/local_integration/'
COMMON = DIR+'current_entry_boundary_x03.py'
REQUIRED = {
 P:{COMMON,CAT,DIR+'current_programme_evaluator.py',DIR+'program_profile_registry.py'},
 G:{COMMON,*(DIR+i+'.py' for i in ('current_programme_evaluator','guest_four_route_diagnostic','kitchen_guest_review','source_guest_route_evaluator'))},
 L:{COMMON,*(DIR+i+'.py' for i in ('fixed_route_clearance_diagnostic','kitchen_guest_review','living_connectivity_diagnostic','source_guest_route_evaluator','source_living_evaluator'))},
 W:{COMMON,*(DIR+i+'.py' for i in ('current_programme_evaluator','source_wall_counterfactual','source_wall_function_evaluator'))}}
REMAINING = {
 G:{0:'First-living/principal organisation unproved',
    4:'This actual-work-area profile differs from historical whole-kitchen-floor exclusion; it does not overwrite that FAIL'},
 L:{0:'Calibrated activity/ergonomic/quality profiles unavailable',
    1:'Coherent furnishing and all simultaneous use/exit scenarios unproved'},
 W:{0:'Alternative placement/shorter organisation per wall not proven',
    2:'Fresh rerouted access and full privacy scenarios not evaluated by this probe',
    3:'Core/shell non-module walls inventoried only, no removal authorization'}}
WC_EXCEPTION = 'Only target body intersection with own WC fixture; all remaining WC fixture material stays obstacle'
SOURCE_FOR = dict(zip((P,G,L,W), (DIR+'current_programme_evaluator.py', DIR+'source_guest_route_evaluator.py',
    DIR+'source_living_evaluator.py', DIR+'source_wall_function_evaluator.py')))
FA = {
 'SOURCE_BOUND_IDENTITY':'هویت برنامه و نقش خواب با مدل و درخواست تطبیق دارد.',
 'PLANAR_SLEEP_CAPACITY_ONLY':'چهار جای خواب واقعی برای هر واحد در کنترل محدود آشکار است.',
 'ALTERNATIVE_SEQUENCE_EVIDENCE_MISSING':'زنجیره کامل بدیل‌ها و دلیل حذف آن‌ها در این بسته نیست.',
 'OPERATIONAL_QUALITY_PROFILE_OPEN':'ضابطه وجود دارد؛ لنگر عملیاتی و کالیبراسیون کیفیت آماده نیست.',
 'PREFILTER_NOT_EVALUATED':'پیش‌فیلتر منبع‌دار ظرفیت در این ارزیابی اجرا نشده است.',
 'FULL_BUNDLE_USE_UNPROVED':'استفاده، خروج و هم‌زمانی کامل تجهیزات ثابت نشده است.',
 'INDEPENDENT_SERVICE_USE_UNPROVED':'موجودی فضا و وسایل به‌تنهایی کارکرد مستقل خدمات را ثابت نمی‌کند.',
 'FOUR_SCOPED_GUEST_ROUTES':'چهار مسیر مهمان هر واحد فقط در سناریوی منبع بررسی شده‌اند.',
 'SCOPED_KITCHEN_WORK_EXCLUSION':'بدنه مسیرهای بررسی‌شده با موانع کار و حرکت آشپزخانه برخورد ندارد.',
 'PRINCIPAL_FIRST_LIVING_UNPROVED':'تقدم واقعی نشیمن در سازمان اصلی اثبات نشده است.',
 'SCOPED_PUBLIC_WC_ACCESS':'دسترسی عمومی توالت فقط در سناریوی منبع شاهد دارد.',
 'DIFFERENT_KITCHEN_PROFILES':'آزمون ناحیه کار با منع عبور از کل کف آشپزخانه یکسان نیست.',
 'SEATING_INVENTORY_ONLY':'مقصدهای واقعی نشستن ثبت شده‌اند؛ استفاده کامل اثبات نشده است.',
 'DECLARED_LIVING_CONTINUITY_UNPROVED':'تداوم کف نشیمن اثبات نشده؛ شاهد دسترسی عمومی معادل آن نیست.',
 'USEFUL_LIVING_AREA_NOT_VERIFIED':'اندازه‌های هندسی مساحت مفید تأییدشده نیستند.',
 'SHORTER_ORGANIZATION_NOT_RUN':'بدیل واقعی با مسیر کوتاه‌تر مقایسه نشده است.',
 'GROUP_USE_PROFILE_OPEN':'استفاده و خروج هم‌زمان گروه با پروفایل معتبر اثبات نشده است.',
 'WALL_INVENTORY_AND_BOUNDARY_PROBES_ONLY':'فهرست و آزمون محدود مرز دیوار ضرورت کارکردی را ثابت نمی‌کند.',
 'VIEW_ONLY_CLASSIFICATION_NOT_IMPLEMENTED':'تشخیص کامل دیوار صرفاً پوشاننده دید پیاده نشده است.',
 'ALIAS_MATERIAL_GEOMETRY_ONLY':'اندازه مصالح منحصربه‌فرد حذف‌شده، اثبات فضای مفید نیست.',
 'FRESH_WALL_ALTERNATIVE_UNPROVED':'بدیل واقعی دیوار با بازسنجی دسترسی و استفاده موجود نیست.',
 'LIMITED_PRIVACY_TARGET_SET':'گواه محدود دید فقط برای هدف‌های منبع است، نه همه اتاق‌ها.',
 'CORE_ENGINEERING_OUTSIDE_SELECTED_SCOPE':'تأیید فنی پله و آسانسور خارج از دامنه این چهار گزارش است.',
 'EVIDENCE_ABSENT':'فیلد شاهد لازم موجود نیست.',
 'NO_VALID_SCOPED_WITNESS':'شاهد معتبر در همین دامنه وجود ندارد؛ ناممکنی ثابت نشده است.',
 'EVALUATOR_ERROR_RETAINED':'خطای ارزیاب ثبت شده و حذف یا تبدیل به قبولی نشده است.',
 'EVIDENCE_CONFLICT_RETAINED':'ناسازگاری شاهد ثبت شده و نتیجه قطعی نیست.',
 'ARCHIVED_NOT_EVALUATED':'این ارزیابی طبق گزارش بایگانی اجرا نشده یا پوشش ندارد.',
 'ARCHIVED_CAPACITY_VIOLATION':'گزارش همان مدل کمبود صریح ظرفیت خواب را نشان می‌دهد.',
}
VOCAB = set('PASS_SCOPED FAIL_SCOPED INDETERMINATE CONFLICT NOT_EVALUATED EVALUATION_ERROR NOT_APPLICABLE MEASURED_ONLY'.split())
ERRS = {'EVALUATOR_ERROR','UNKNOWN_EVALUATOR_OR_BINDING_ERROR','EVALUATOR_OR_SOURCE_BINDING_ERROR',
        'INTEGRITY_ERROR','MISSING_EVALUATOR_RESULT'}
H32 = re.compile(r'[0-9a-f]{32}\Z')
H64 = re.compile(r'[0-9a-f]{64}\Z')

def need(ok, code):
    if not ok:
        raise ValueError(code)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def digest(data):
    return sha(json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode())

def same(a,b):
    return digest(a)==digest(b)

def decode(raw):
    def pairs(kv):
        out={}
        for k,v in kv:
            need(k not in out,'P38_DUPLICATE_JSON_KEY')
            out[k]=v
        return out
    def reject(_):
        raise ValueError('P38_NONFINITE_JSON')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=reject)

def authority(x):
    need(all(x.get(k) is False for k in AUTH),'P38_AUTHORITY')

def catalog(raw):
    h=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    need(h==CAT_BLOB,'P38_CATALOG_BLOB')
    d=decode(raw)
    need(d['schema']=='V25_CURRENT_FUNCTIONAL_CRITERIA_CATALOG_V2'
         and [r['id'] for r in d['criteria']]==list(IDS),'P38_CATALOG_SHAPE')
    for r in d['criteria']:
        need([q['id'] for q in r['conditions']]==['P20_'+i for i in IDS[r['id']]],
             'P38_CATALOG_IDS')
    return d

def extract(raw, trusted_sha):
    need(type(trusted_sha) is str and H64.fullmatch(trusted_sha)
         and len(raw)<=24_000_000 and sha(raw)==trusted_sha,'P38_ARCHIVE_PIN')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        entries=z.infolist()
        names=[i.filename for i in entries]
        need(len(names)==len(set(names))==49 and sum(i.file_size for i in entries)<48_000_000
             and all(not i.is_dir() and not i.filename.startswith('/')
                     and all(x not in ('','.', '..') for x in i.filename.split('/')) for i in entries),
             'P38_ARCHIVE_MEMBERS')
        manifest='P04-private-manifest.json'
        need(manifest in names,'P38_MANIFEST_MISSING')
        files={k:z.read(k) for k in names}
    m=decode(files[manifest]); index=m['snapshot_files']
    need(m['commit']==REF and m['tree']==TREE and m['private_only'] is True
         and type(m['requested_case_count']) is int and m['requested_case_count']==2
         and set(index)==set(files)-{manifest},'P38_MANIFEST_COVERAGE')
    need(all(same(v,{'sha256':sha(files[k]),'size':len(files[k])}) for k,v in index.items()),
         'P38_MEMBER_HASH')
    return files

def model_bind(bundle, model, request):
    mh=digest(model)
    b=bundle['binding']; e=b['envelope']; raw=b['raw']; ct=b['contract']
    need(bundle['model_digest']==mh and bundle['model_binding_verified'] is True
         and bundle['object_integrity_verified'] is True
         and bundle['completed'] is True
         and same(e['received_input'],request)
         and same(raw,{**request,'requested_count':1})
         and same(model['inputs'],[request['W'],request['L'],request['n']])
         and bundle['packet']['family']=='FRONT_REAR'
         and ct['family']=='FRONT_REAR' and ct['engine_revision']==bundle['engine_revision']
         and same(b['contract_digest'],digest(ct)), 'P38_MODEL_REQUEST_BINDING')
    pr=model['program']
    need(same([pr['units'],pr['bedrooms_per_unit'],pr['design_occupants_per_unit'],pr['sleep_roles']],
              [2,2,4,['double','twin']]) and [u['id'] for u in model['units']]==['A','B'],
         'P38_MODEL_PROGRAMME')
    need(same(bundle['object_digests'],{k:digest(bundle[k]) for k in ('proposal','packet','context')}
              | {'core':digest(bundle['packet']['core']),'raw':digest(raw)}),'P38_OBJECT_BINDING')
    return mh

def verify_case(files, label, request, pins, catalog_bytes):
    root='observations/'+label+'/'
    ro=lambda n: decode(files[root+n])
    run=decode(files['procedure/proof-summary.json'])
    cases=[c for c in run['cases'] if c['label']==label]
    need(run['commit']==REF and run['tree']==TREE and len(run['cases'])==2
         and len(cases)==1 and same(cases[0]['request'],request),'P38_CASE_INDEX')
    case=cases[0]; nonce=case['nonce']
    need(type(nonce) is str and H32.fullmatch(nonce) and case['http_status']==200
         and case['offline_inner_receipt_verified'] is True and same(ro('request-body.json'),request),
         'P38_CASE_OBSERVATION')
    er='evidence/'+nonce+'/'
    member=lambda n: decode(files[er+n])
    req=member('request.json');rt=member('runtime-bundle.json')
    receipt=member('child-complete.json');scheduler=member('scheduler.json')
    dec=member('decision.json');reports={k:member(k+'.json') for k in IDS}
    body=bytes.fromhex(req['body_hex'])
    need(req['nonce']==nonce==receipt['nonce'] and same(decode(body),request)
         and same(receipt['request_digest'],digest(req))
         and sha(body)==rt['binding']['envelope']['transport_body_sha256']
         and req['preflight_digest']==receipt['preflight_digest']==digest(scheduler['preflight'])
         and same(ro('preflight.json'),scheduler['preflight'])
         and req['schema']=='LIVE_PROGRAM_ATTEMPT_V1'
         and receipt['schema']=='LIVE_SCHEDULER_CHILD_V1'
         and scheduler['head_sha']==REF and scheduler['source_integrity_verified'] is True,
         'P38_REQUEST_RECEIPT')
    mh=model_bind(rt,rt['packet']['world_model'],request)
    ph=rt['reports']['physical']; replay=rt['reports']['replay']
    original_digests={k:digest(v) for k,v in rt['reports'].items()}
    need(set(original_digests)==ORIGINALS and same(original_digests,rt['report_digests'])
         and same(rt['reports'],dec['original_reports'])
         and same(original_digests,dec['original_report_digests'])
         and original_digests['physical']==dec['physical_digest'] and ph['model_hash']==mh
         and replay['model_hash']==mh and replay['source_revision']==rt['engine_revision']
         and replay['verified'] is True and dec['engine_revision']==rt['engine_revision'],
         'P38_ORIGINAL_BINDING')
    need(case['model_digest']==mh==receipt['model_digest']==dec['model_digest']
         and receipt['runtime_digest']==digest(rt) and receipt['decision_digest']==digest(dec)
         and same(receipt['decision'],dec['decision'])
         and same(receipt['assessments'],reports) and same(dec['assessments'],reports)
         and same(dec['assessment_digests'],{k:digest(r) for k,r in reports.items()})
         and dec['schema']=='SAME_MODEL_CURRENT_FOUR_DECISION_V1'
         and dec['integrity_verified'] is True, 'P38_REPORT_DECISION_BINDING')
    attempts=scheduler['attempts']
    need(type(attempts) is list and len(attempts)==1,'P38_ATTEMPT_CARDINALITY')
    a=attempts[0]
    need(a['receipt_verified'] is True and a['attempted'] is True and a['timed_out'] is False
         and a['model_binding_verified'] is True and a['wait_completed'] is True
         and all(a[k]==v for k,v in {'nonce':nonce,'model_digest':mh,
           'runtime_digest':digest(rt),'decision_digest':digest(dec)}.items()),'P38_ATTEMPT_LINK')
    before={}
    for k,r in reports.items():
        authority(r)
        need(r['schema']==SCHEMAS[k] and r['criterion']==k and r['model_digest']==mh
             and r['current_domain_policy']=='CURRENT_ENTRY_DOMAIN_X03_V1',
             'P38_REPORT_IDENTITY')
        prefix='historical' if k==P else 'original'
        rp=r['reports']['replay'] if k==P else r['replay']
        need(r[prefix+'_physical_digest']==original_digests['physical']
             and same(r[prefix+'_physical_report'],ph) and same(rp,replay),'P38_REPORT_ORIGIN')
        need(set(r['source_snapshot'])==REQUIRED[k],'P38_REPORT_SOURCE_SET')
        for path,h in r['source_snapshot'].items():
            need(pins.get(path)==h and before.get(path,h)==h,'P38_REPORT_SOURCE')
            before[path]=h
    need(same(before,dec['source_snapshot']) and before.get(CAT)==sha(catalog_bytes)
         and same(dec['decision_source_snapshot'],{DEC_PATH:pins[DEC_PATH]}),'P38_DECISION_SOURCE')
    states={row['criterion']:row for row in dec['criteria']}
    need(len(dec['criteria'])==len(states)==4 and set(states)==set(IDS)
         and all(states[k]['reported_state']==reports[k]['state']
                 and states[k]['assessment_digest']==digest(reports[k]) for k in IDS),
         'P38_DECISION_STATES')
    for x in (rt,receipt,scheduler,dec,dec['decision']):
        authority(x)
    need(dec['decision']['state']=='BLOCKED','P38_ARCHIVED_SCOPE')
    return {'label':label,'request':request,'model_digest':mh,'nonce':nonce,
            'engine_revision':rt['engine_revision'],'report_revision':REF,
            'decision_digest':digest(dec),'decision_state':dec['decision']['state'],
            'blockers':dec['decision']['blockers'],'physical_status':ph['status'],
            'physical_digest':original_digests['physical'],
            'catalog_blob':CAT_BLOB,'reported_states':{k:states[k]['reported_state'] for k in IDS},
            'effective_states':{k:states[k]['effective_state'] for k in IDS},
            'source_snapshot':before,'observed_evaluator_errors':{k:states[k]['evaluator_errors'] for k in IDS},
            'reports':reports, 'raw_sha':{k:sha(files[er+k+'.json']) for k in IDS}}

def pointer(report,path):
    value=report
    for token in path:
        need((type(value) is dict and token in value) or
             (type(value) is list and type(token) is int and 0<=token<len(value)),
             'P38_DANGLING_POINTER')
        value=value[token]
    return value

def cited(report, f, model_digest, raw_sha, path):
    val=pointer(report,path)
    jp=''.join('/'+str(v).replace('~','~0').replace('/','~1') for v in path)
    return {'report_role':f,'raw_sha256':raw_sha,'model_digest':model_digest,
            'json_pointer':jp,'node_digest':digest(val)}

def classify(states, positive, *, diagnostic, reason):
    """Independent witness state vs normalized diagnosis; never an aggregate result."""
    s=set(states)
    if s & ERRS:
        return 'EVALUATION_ERROR','EVALUATOR_ERROR','EVALUATOR_ERROR_RETAINED'
    if s & {'CONFLICT','SOURCE_CONFLICT','CLEARANCE_CONTRADICTION'}:
        return 'CONFLICT','SOURCE_CONFLICT','EVIDENCE_CONFLICT_RETAINED'
    if 'ACTUAL_CAPACITY_SHORTFALL' in s and reason=='PLANAR_SLEEP_CAPACITY_ONLY':
        return 'FAIL_SCOPED','NECESSARY_SLEEP_CAPACITY_SHORTFALL','ARCHIVED_CAPACITY_VIOLATION'
    if positive:
        return 'PASS_SCOPED',diagnostic,reason
    if 'NOT_RUN' in s:
        return 'NOT_EVALUATED','NOT_RUN',reason
    if 'NOT_EVALUATED' in s:
        return 'NOT_EVALUATED',diagnostic,reason
    return ('MEASURED_ONLY' if diagnostic=='MEASURED_ONLY' else 'INDETERMINATE'),diagnostic,reason

def profile_rows(case, cat):
    specs={c['id']:c for c in cat['criteria']}; out={}
    def add(cid,id,diagnostic,reason,paths=(),states=(),positive=False,measure=None):
        r=case['reports'][cid]
        archived=list(states)
        if not paths:
            diagnostic,reason,positive='MISSING_EVIDENCE','EVIDENCE_ABSENT',False
        proof_states=list(states)
        if r.get('integrity_verified') is not True:
            proof_states.append('INTEGRITY_ERROR')
            paths=(*paths,('integrity_verified',)) if 'integrity_verified' in r else paths
        if r.get('missing'):
            proof_states.append('MISSING_EVALUATOR_RESULT')
            paths=(*paths,('missing',))
        result,tag,reason=classify(proof_states,positive,diagnostic=diagnostic,reason=reason)
        cond=next(c for c in specs[cid]['conditions'] if c['id']=='P20_'+id)
        refs=[cited(r,cid,case['model_digest'],case['raw_sha'][cid],p) for p in dict.fromkeys(paths)]
        out[id]={'condition':cond['id'],'criterion':cid,'catalogue_annotation':cond['runtime_condition_result'],
            'catalogue_condition_kind':cond['kind'],'rule_source_aliases':cond['source_refs'],
            'archived_evaluator_source':{'path':SOURCE_FOR[cid],
                'sha256':case['source_snapshot'][SOURCE_FOR[cid]]},
            'archived_report_state':r['state'],'archived_runtime_explicit_states':archived or None,
            'diagnostic_result':result,'diagnostic_reason':tag,'reason_code':reason,
            'rationale_fa':FA[reason],'references':refs,'measurement':measure}
    p,g,l,w=[case['reports'][k] for k in IDS]
    binds=[(i,) for i,u in enumerate(p['inventory']) if u.get('unit') in ('A','B')]
    inv=[('inventory',*i) for i in binds]
    identity=([u['unit'] for u in p['inventory']]==['A','B']
              and all(type(u['design_persons']) is int and u['design_persons']==4
                      and bool(u['module_bindings']) for u in p['inventory']))
    add(P,'PROGRAM_IDENTITY','TYPED_IDENTITY_ONLY','SOURCE_BOUND_IDENTITY',inv+[('reports','replay','verified')],positive=identity)
    cap=p['reports']['capacity']; ev=cap.get('evidence',{})
    places=ev.get('units',[])
    count=[u.get('actual_places',{}).get('sleeping_places') for u in places]
    cap_ok=([u.get('unit') for u in places]==['A','B'] and
            all(type(n) is int and n==4 for n in count)
            and all(type(u.get('residents_study')) is int and u['residents_study']==4 for u in places)
            and p.get('source_capacity_state')=='PASS_SCOPED'
            and ev.get('status')=='PASS_ACTUAL_INSTANCE_PLANAR_CAPACITY'
            and ev.get('model_hash')==case['model_digest'] and cap.get('errors')==[] and cap.get('pending')==[])
    cap_states=[p['source_capacity_state']] if 'source_capacity_state' in p else []
    pp=[('source_capacity_state',)] if cap_states else []
    pp += [('reports','capacity','evidence','units',i,'actual_places','sleeping_places')
           for i,u in enumerate(places) if 'sleeping_places' in u.get('actual_places',{})]
    for i,e in enumerate(cap.get('errors',[])):
        matching=[(j,u) for j,u in enumerate(places) if u.get('unit')==e.get('unit')]
        bound=len(matching)==1
        if bound:
            j,u=matching[0]
            actual=u.get('actual_places',{}).get('sleeping_places')
            required=u.get('residents_study')
            bound=(type(actual) is int and type(required) is int
                   and 0<=actual<required==4)
        if (e.get('code')=='ACTUAL_CAPACITY_SHORTFALL' and e.get('group')=='sleeping_places'
                and e.get('unit') in ('A','B') and bound and ev.get('model_hash')==case['model_digest']):
            cap_states.append('ACTUAL_CAPACITY_SHORTFALL'); pp.extend(
                [('reports','capacity','errors',i),('reports','capacity','evidence','units',j,'residents_study')])
    add(P,'PROGRAM_CAPACITY','PLANAR_CAPACITY_ONLY' if cap_ok else 'MISSING_EVIDENCE',
        'PLANAR_SLEEP_CAPACITY_ONLY',pp,cap_states,cap_ok,{'sleep_places':count})
    def pf(id, codes, diagnostic, reason):
        pairs=[(i,f) for i,f in enumerate(p.get('findings',[])) if f.get('code') in codes]
        add(P,id,diagnostic,reason,[('findings',i) for i,f in pairs],[f['kind'] for i,f in pairs])
        out[id]['archived_findings']=[{'kind':f['kind'],'code':f['code']} for _,f in pairs]
    pf('PROGRAM_ALTERNATIVES',{'AP07_ALTERNATIVE_SEQUENCE_AND_PARETO_SELECTION'},'MISSING_EVIDENCE','ALTERNATIVE_SEQUENCE_EVIDENCE_MISSING')
    pf('PROGRAM_QUALITY_FLOOR',{'CALIBRATED_ROOM_UNIT_QUALITY_AND_ERGONOMIC_SCENARIOS','OPERATIONAL_QUALITY_DIMENSIONS_AND_ACCEPTANCE_ANCHORS_OPEN'},'PROFILE_NOT_READY','OPERATIONAL_QUALITY_PROFILE_OPEN')
    pf('PROGRAM_PREFILTER',{'NET_CAPACITY_PREFILTER_SOURCE_BOUND_NOT_AVAILABLE'},'NOT_RUN','PREFILTER_NOT_EVALUATED')
    add(P,'PROGRAM_BUNDLE_USE','MISSING_EVIDENCE','FULL_BUNDLE_USE_UNPROVED',
        [(*i,'activity_phase_coverage') for i in inv]+[('reports','capacity','evidence','scope')],[p['inventory'][i[-1]]['activity_phase_coverage']['exit'] for i in inv])
    add(P,'PROGRAM_SERVICE_MINIMA','MISSING_EVIDENCE','INDEPENDENT_SERVICE_USE_UNPROVED',inv)
    def guest(id,needed,reason,extra=None):
        paths=[]; states=[]; ok=[u['unit'] for u in g['units']]==['A','B']; per={}
        for i,u in enumerate(g['units']):
            rows=[(j,x) for j,x in enumerate(u['routes']) if x['id'] in needed]
            paths.extend(('units',i,'routes',j) for j,x in rows)
            states.extend(x['state'] for _,x in rows)
            per[u['unit']]=sum(x['state']=='PASS_SOURCE_PROFILE_ROUTE_ONLY' for _,x in rows)
            if extra=='work' and 'kitchen_operation_digest' in u:
                paths.append(('units',i,'kitchen_operation_digest'))
            if 'destination_bindings' in u:
                paths.append(('units',i,'destination_bindings'))
            db=u.get('destination_bindings',{})
            dest=(type(db.get('living',{}).get('fixture_id')) is str
                 and type(db.get('living',{}).get('activity_id')) is str
                 and H64.fullmatch(db.get('dining',{}).get('module_hash','')) is not None
                 and type(db.get('dining',{}).get('seat_id')) is str
                 and db.get('WC',{}).get('activity_id')=='WC_use'
                 and H64.fullmatch(db.get('WC',{}).get('module_hash','')) is not None)
            ok=bool(ok and dest and [x['id'] for j,x in rows]==list(needed)
                 and all(x['state']=='PASS_SOURCE_PROFILE_ROUTE_ONLY' and x.get('body_m')=='7/10'
                         and type(x.get('path')) is list and len(x['path'])>=2
                         and type(x.get('segments')) is int and x['segments']>0
                         and all(H64.fullmatch(x.get(k,'')) for k in ('floor_digest','obstacle_digest','ownership_digest'))
                         and x.get('floor_roles')==['living','entry_circulation','dining','kitchen']+(['bath'] if x['id']=='entry_WC' else [])
                         and x.get('wc_exception')==(WC_EXCEPTION if x['id']=='entry_WC' else None) for _,x in rows)
                 and (extra!='work' or H64.fullmatch(u.get('kitchen_operation_digest',''))))
        add(G,id,'SOURCE_PROFILE_ONLY' if ok else 'MISSING_EVIDENCE',
            reason if ok else 'NO_VALID_SCOPED_WITNESS',paths,states,ok,per)
    guest('GUEST_FOUR_ROUTES',ROUTES,'FOUR_SCOPED_GUEST_ROUTES')
    guest('GUEST_WORK_EXCLUSION',ROUTES,'SCOPED_KITCHEN_WORK_EXCLUSION','work')
    guest('GUEST_PRIVATE_ACCESS',('entry_WC',),'SCOPED_PUBLIC_WC_ACCESS','wc')
    def rempaths(cid,*indices):
        v=case['reports'][cid].get('remaining',[])
        return [('remaining',i) for i in indices if i<len(v) and v[i]==REMAINING[cid][i]]
    def remaining(cid,index,id,tag,reason):
        add(cid,id,tag,reason,rempaths(cid,index))
    remaining(G,0,'GUEST_FIRST_LIVING','MISSING_EVIDENCE','PRINCIPAL_FIRST_LIVING_UNPROVED')
    remaining(G,4,'GUEST_KITCHEN_LABEL','PROFILE_SCOPE_DIFFERENCE','DIFFERENT_KITCHEN_PROFILES')
    lp=lambda key:[('units',i,key) for i,u in enumerate(l['units']) if key in u]
    add(L,'LIVING_SOURCE_SEATS','MEASURED_ONLY','SEATING_INVENTORY_ONLY',lp('actual_seat_endpoints'),
        measure={u['unit']:len(u['actual_seat_endpoints']) for u in l['units']})
    domains=[]
    for i,u in enumerate(l['units']):
        for j,s in enumerate(u['studies']):
            rowstates=[q['state'] for q in s['routes']]
            domains.append({'unit':u['unit'],'domain':s['domain'],
                            'all_targets_connected':s['all_targets_connected'],'states':rowstates})
    add(L,'LIVING_FLOOR_CONTINUITY','MISSING_EVIDENCE','DECLARED_LIVING_CONTINUITY_UNPROVED',
        lp('studies'),[s for d in domains for s in d['states']],measure=domains)
    add(L,'LIVING_USEFUL_AREA','MISSING_EVIDENCE','USEFUL_LIVING_AREA_NOT_VERIFIED',
        [(*i,'verified_useful_living_area_m2') for i in lp('area_accounting')
         if 'verified_useful_living_area_m2' in pointer(l,i)])
    add(L,'LIVING_SHORTER_ALTERNATIVE','MISSING_EVIDENCE','SHORTER_ORGANIZATION_NOT_RUN',
        lp('shorter_organisation_comparison'),[u['shorter_organisation_comparison']['state'] for u in l['units']])
    add(L,'LIVING_GROUP_USE','PROFILE_NOT_READY' if rempaths(L,0) else 'MISSING_EVIDENCE','GROUP_USE_PROFILE_OPEN',
        rempaths(L,0,1)+lp('activity_phase_coverage'),
        [u['activity_phase_coverage']['exit_and_simultaneous_group_use'] for u in l['units']])
    add(W,'WALL_SOURCE_INVENTORY','MEASURED_ONLY','WALL_INVENTORY_AND_BOUNDARY_PROBES_ONLY',
        [('walls',),('counts',)],measure={k:w['counts'][k] for k in ('all_source_walls','boundary_dependency_probes','non_module_inventory_only')})
    add(W,'WALL_VIEW_ONLY','IMPLEMENTATION_GAP','VIEW_ONLY_CLASSIFICATION_NOT_IMPLEMENTED',
        [('walls',)]+rempaths(W,2))
    add(W,'WALL_ALIAS_MATERIAL','MEASURED_ONLY','ALIAS_MATERIAL_GEOMETRY_ONLY',
        [('walls',),('counts','zero_unique_material_probes')],measure=w['counts']['zero_unique_material_probes'])
    remaining(W,0,'WALL_ALTERNATIVE','MISSING_EVIDENCE','FRESH_WALL_ALTERNATIVE_UNPROVED')
    priv=[('walls',i,'privacy_scope') for i,r in enumerate(w['walls']) if 'privacy_scope' in r]
    add(W,'WALL_PRIVACY_TARGETS','PARTIAL_SCOPE','LIMITED_PRIVACY_TARGET_SET',
        priv+rempaths(W,2),measure={'scoped_rows':len(priv)})
    add(W,'CORE_ENGINEERING','OUT_OF_SCOPE','CORE_ENGINEERING_OUTSIDE_SELECTED_SCOPE',
        rempaths(W,3))
    if out['CORE_ENGINEERING']['diagnostic_reason']=='OUT_OF_SCOPE' and out['CORE_ENGINEERING']['diagnostic_result']=='INDETERMINATE':
        out['CORE_ENGINEERING']['diagnostic_result']='NOT_EVALUATED'
    # Criterion errors are also retained verbatim in the outer archive report, not guessed for a subcondition.
    return [out[i] for ids in IDS.values() for i in ids]

def project(archive_bytes, expected_archive_sha, catalog_bytes, independent_source_pins):
    cat=catalog(catalog_bytes)
    files=extract(archive_bytes,expected_archive_sha)
    reqs={'d18p1x22p2':{'W':'18.1','L':'22.2','n':2},'b25x25':{'W':'25','L':'25','n':2}}
    out=[]
    for label,request in reqs.items():
        verified=verify_case(files,label,request,independent_source_pins,catalog_bytes)
        rows=profile_rows(verified,cat)
        result={k:v for k,v in verified.items() if k not in ('reports','raw_sha')}
        result['conditions']=rows
        out.append(result)
    need(out[0]['model_digest']!=out[1]['model_digest'] and out[0]['nonce']!=out[1]['nonce'],
         'P38_CROSSED_CASES')
    return {'schema':'P38_ARCHIVED_CONDITION_COVERAGE_V1','archive_sha256':expected_archive_sha,
            'archive_count':2,'now_evaluated':False,'product_available':False,'cases':out,
            **{k:False for k in AUTH}}

def persian(report):
    lines=['ردیابی شروط کیفیت در دو بسته بایگانی‌شده؛ ارزیابی تازه یا مجوز تحویل نیست.']
    for result in report['cases']:
        req=result['request']
        lines.append(f"زمین {req['W']} × {req['L']} متر، {req['n']} واحد؛ تصمیم اصلی: {result['decision_state']}")
        for row in result['conditions']:
            lines.append(f"{row['condition']} | {row['diagnostic_result']} | {row['rationale_fa']}")
    return '\n'.join(lines)+'\n'
