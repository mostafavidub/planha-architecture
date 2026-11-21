import collections
import copy
import io
import json
from pathlib import Path
import unittest
import zipfile

from studies import p38_archived_quality_coverage as p

CAT = (Path(__file__).resolve().parents[2] / p.CAT).read_bytes()
H = 'a' * 64
FALSE = dict.fromkeys(p.AUTH, False)
REQ = {'W':'18.1','L':'22.2','n':2}
LABEL = 'd18p1x22p2'
NONCE = 'b' * 32
ER = 'evidence/'+NONCE+'/'
O = 'observations/'+LABEL+'/'
ROW = ('CALIBRATED_ROOM_UNIT_QUALITY_AND_ERGONOMIC_SCENARIOS', 'OPERATIONAL_QUALITY_DIMENSIONS_AND_ACCEPTANCE_ANCHORS_OPEN',
       'AP07_ALTERNATIVE_SEQUENCE_AND_PARETO_SELECTION','NET_CAPACITY_PREFILTER_SOURCE_BOUND_NOT_AVAILABLE')

def raw(x):
    return json.dumps(x, ensure_ascii=False, allow_nan=False).encode()

def synth():
    """Fictional structure only, no source-derived coordinates or project report data."""
    const = p.digest
    model={'inputs':[REQ['W'],REQ['L'],2],
           'program':dict(units=2,bedrooms_per_unit=2,design_occupants_per_unit=4,sleep_roles=['double','twin']),
           'units':[{'id':'A'},{'id':'B'}]}
    packet={'world_model':model,'core':{'synthetic':'core'},'family':'FRONT_REAR'}
    mh=const(model)
    replay={'verified':True,'model_hash':mh,'source_revision':H}
    physical={'model_hash':mh,'status':'PASS_CONCEPT_SCOPED_REVIEW','original_pending':['TEST_PENDING']}
    originals={k:{'fixture':k} for k in p.ORIGINALS}|{'replay':replay,'physical':physical}
    opins={k:const(v) for k,v in originals.items()}
    pf={'synthetic':True}
    body=raw(REQ)
    request={'schema':'LIVE_PROGRAM_ATTEMPT_V1','nonce':NONCE,'body_hex':body.hex(),
             'preflight_digest':const(pf)}
    contract={'family':'FRONT_REAR','engine_revision':H}
    binder={'raw':REQ|{'requested_count':1},'envelope':{'received_input':REQ,
            'transport_body_sha256':p.sha(body)},'contract':contract,'contract_digest':const(contract)}
    rt={**FALSE,'engine_revision':H,'binding':binder,'packet':packet,'context':{},'proposal':{},
       'reports':originals,'report_digests':opins,'model_digest':mh,'model_binding_verified':True,
       'object_integrity_verified':True,'completed':True}
    rt['object_digests']={i:const(rt[i]) for i in ('packet','context','proposal')}|{'raw':const(binder['raw']),'core':const(packet['core'])}
    pins={k:H for paths in p.REQUIRED.values() for k in paths}|{p.CAT:p.sha(CAT), p.DEC_PATH:H}
    reports={}
    for k,n in p.SCHEMAS.items():
        prefix='historical' if k==p.P else 'original'
        reports[k]={**FALSE,'schema':n,'criterion':k,'model_digest':mh,'state':'UNKNOWN','integrity_verified':True,
                    'current_domain_policy':'CURRENT_ENTRY_DOMAIN_X03_V1','source_snapshot':{v:pins[v] for v in p.REQUIRED[k]},
                    prefix+'_physical_digest':opins['physical'],prefix+'_physical_report':physical}
        if k!=p.P:reports[k]['replay']=replay
    rp=reports[p.P]
    rp['inventory']=[{'unit':u,'design_persons':4,'module_bindings':[{'synthetic':True}],
                      'activity_phase_coverage':{'exit':'NOT_INDEPENDENTLY_EVALUATED'}} for u in 'AB']
    rp['findings']=[dict(code=c,kind=s) for c,s in zip(ROW,('MISSING_PROFILE','MISSING_RULE','MISSING_EVIDENCE','NOT_EVALUATED'))]
    rp['source_capacity_state']='PASS_SCOPED'
    rp['reports']={'replay':replay,'capacity':{'errors':[],'pending':[],
        'evidence':{'model_hash':mh,'scope':'Synthetic','status':'PASS_ACTUAL_INSTANCE_PLANAR_CAPACITY',
                    'units':[{'unit':u,'residents_study':4,'actual_places':{'sleeping_places':4}} for u in 'AB']}}}
    def remainder(cid, n):
        rr=['synthetic']*n
        for i,text in p.REMAINING[cid].items():rr[i]=text
        return rr
    rr=[{'state':'PASS_SOURCE_PROFILE_ROUTE_ONLY','id':n,'body_m':'7/10',
         'path':[[0,0],[0,1]],'segments':1,'floor_digest':H,'obstacle_digest':H,'ownership_digest':H,
         'floor_roles':['living','entry_circulation','dining','kitchen']+(['bath'] if n=='entry_WC' else []),
         'wc_exception':p.WC_EXCEPTION if n=='entry_WC' else None} for n in p.ROUTES]
    rg=reports[p.G]
    rg['remaining']=remainder(p.G,5)
    rg['units']=[{'unit':u,'routes':copy.deepcopy(rr),'kitchen_operation_digest':H,'destination_bindings':{
        'WC':{'module_hash':H,'activity_id':'WC_use'}, 'dining':{'module_hash':H,'seat_id':'test'},
        'living':{'fixture_id':'test','activity_id':'test'}}} for u in 'AB']
    rl=reports[p.L]
    rl['remaining']=remainder(p.L,4)
    rl['units']=[{'unit':u,'actual_seat_endpoints':[],'shorter_organisation_comparison':{'state':'NOT_RUN'},
        'activity_phase_coverage':{'exit_and_simultaneous_group_use':'NOT_FULLY_VERIFIED'},
        'area_accounting':{'verified_useful_living_area_m2':None},
        'studies':[{'domain':'AUTHORIZED_LIVING_AND_CIRCULATION_ACCESS','all_targets_connected':True,
                    'routes':[{'state':'PASS_ACCESS_WITNESS_ONLY'}]}]} for u in 'AB']
    rw=reports[p.W]
    rw['walls']=[{'privacy_scope':'synthetic'}]; rw['remaining']=remainder(p.W,4)
    rw['counts']=dict(all_source_walls=1,boundary_dependency_probes=0,non_module_inventory_only=0,zero_unique_material_probes=0)
    ad={k:const(r) for k,r in reports.items()}
    dec={**FALSE,'schema':'SAME_MODEL_CURRENT_FOUR_DECISION_V1','integrity_verified':True,
        'engine_revision':H,'physical_digest':opins['physical'],'model_digest':mh,'assessments':reports,
        'assessment_digests':ad,'original_reports':originals,'original_report_digests':opins,
        'decision':{**FALSE,'state':'BLOCKED','blockers':['CURRENT_UNKNOWN','HISTORICAL_UNRESOLVED_RETAINED']},
        'source_snapshot':{k:v for k,v in pins.items() if k!=p.DEC_PATH},
        'decision_source_snapshot':{p.DEC_PATH:H},
        'criteria':[{'criterion':k,'reported_state':'UNKNOWN','effective_state':'UNKNOWN',
                     'assessment_digest':ad[k],'evaluator_errors':[]} for k in p.IDS]}
    links={'model_digest':mh,'runtime_digest':const(rt),'decision_digest':const(dec),'nonce':NONCE}
    receipt={**FALSE,**links,'schema':'LIVE_SCHEDULER_CHILD_V1','request_digest':const(request),
             'preflight_digest':const(pf),'assessments':reports,'decision':dec['decision']}
    scheduler={**FALSE,'head_sha':p.REF,'source_integrity_verified':True,'preflight':pf,'attempts':[
        {**links,'receipt_verified':True,'attempted':True,'timed_out':False,'wait_completed':True,'model_binding_verified':True}]}
    cc={'label':LABEL,'request':REQ,'model_digest':mh,'nonce':NONCE,'http_status':200,
        'offline_inner_receipt_verified':True}
    data={ER+'request.json':request,ER+'runtime-bundle.json':rt,ER+'decision.json':dec,ER+'child-complete.json':receipt,
          ER+'scheduler.json':scheduler,O+'request-body.json':REQ,O+'preflight.json':pf,
          'procedure/proof-summary.json':{'commit':p.REF,'tree':p.TREE,'cases':[cc,{'label':'second'}]}}
    return (data | {ER+k+'.json':r for k,r in reports.items()},pins)

class Coverage(unittest.TestCase):
    def setUp(self):
        v,self.pins=synth()
        self.files={k:raw(d) for k,d in v.items()}
        self.ca=p.catalog(CAT)

    def case(self):
        return p.verify_case(self.files,LABEL,REQ,self.pins,CAT)

    def rows(self, c=None):
        return {r['condition']:r for r in p.profile_rows(c or self.case(),self.ca)}

    def alter(self,name,f):
        v=p.decode(self.files[name]);f(v);self.files[name]=raw(v)

    def test_cases_bind_all_reports_decision_and_true_typed_id(self):
        v=self.case()
        self.assertEqual(v['decision_state'],'BLOCKED')
        self.assertEqual(list(v['reported_states'].values()),['UNKNOWN']*4)
        self.assertEqual(set(v['raw_sha']),set(p.IDS))
        rows=self.rows(v)
        self.assertEqual(len(rows),23)
        self.assertEqual(collections.Counter(r['criterion'] for r in rows.values()),dict(zip(p.IDS,[7,5,5,6])))
        for r in rows.values():
            for ref in r['references']:
                self.assertEqual(ref['raw_sha256'],v['raw_sha'][r['criterion']])
                self.assertEqual(ref['model_digest'],v['model_digest'])

    def test_missing_report_and_swapped_role_rejected(self):
        k=ER+p.L+'.json'; val=self.files.pop(k)
        with self.assertRaises(KeyError):self.case()
        self.files[k]=self.files[ER+p.W+'.json']
        with self.assertRaisesRegex(ValueError,'REPORT_DECISION_BINDING'):self.case()
        self.files[k]=val

    def test_source_and_typed_request_rejected(self):
        old=self.pins[p.SOURCE_FOR[p.L]]
        self.pins[p.SOURCE_FOR[p.L]]='c'*64
        with self.assertRaisesRegex(ValueError,'REPORT_SOURCE'):self.case()
        self.pins[p.SOURCE_FOR[p.L]]=old
        with self.assertRaisesRegex(ValueError,'CASE_INDEX'):
            p.verify_case(self.files,LABEL,REQ|{'n':2.0},self.pins,CAT)

    def test_receipt_and_original_model_link_rejected(self):
        self.alter(ER+'child-complete.json',lambda r:r.update(nonce='c'*32))
        with self.assertRaisesRegex(ValueError,'REQUEST_RECEIPT'):self.case()

    def test_false_authority_exact_boolean(self):
        for v in (True,0,None):
            with self.assertRaisesRegex(ValueError,'AUTHORITY'):
                p.authority({**FALSE,'delivery_allowed':v})

    def test_path_json_pointer_uses_exact_typed_index(self):
        r={'/a~':[3]}
        c=p.cited(r,p.W,H,H,('/a~',0))
        self.assertEqual((c['json_pointer'],c['node_digest']),('/~1a~0/0',p.digest(3)))
        with self.assertRaisesRegex(ValueError,'DANGLING'):
            p.cited(r,p.W,H,H,('/a~',False))

    def test_catalog_unapproved_content(self):
        with self.assertRaisesRegex(ValueError,'CATALOG_BLOB'):
            p.catalog(CAT+b' ')

    def test_archive_pin_member_hash_and_duplicate_json(self):
        data={f'test/{i}':str(i).encode() for i in range(48)}
        index={k:dict(sha256=p.sha(v),size=len(v)) for k,v in data.items()}
        def pack():
            b=io.BytesIO()
            with zipfile.ZipFile(b,'w') as z:
                z.writestr('P04-private-manifest.json',raw(dict(commit=p.REF,tree=p.TREE,private_only=True,
                    requested_case_count=2,snapshot_files=index)))
                for k,v in data.items():z.writestr(k,v)
            return b.getvalue()
        b=pack()
        self.assertEqual(len(p.extract(b,p.sha(b))),49)
        with self.assertRaisesRegex(ValueError,'ARCHIVE_PIN'):p.extract(b,H)
        data['test/2']=b'3';b=pack()
        with self.assertRaisesRegex(ValueError,'MEMBER_HASH'):p.extract(b,p.sha(b))
        with self.assertRaisesRegex(ValueError,'DUPLICATE'):p.decode(b'{"a":1,"a":2}')

    def test_source_profile_pass_not_living_or_group_pass(self):
        v=self.rows()
        for n in ('GUEST_FOUR_ROUTES','GUEST_WORK_EXCLUSION','GUEST_PRIVATE_ACCESS','PROGRAM_CAPACITY'):
            self.assertEqual(v['P20_'+n]['diagnostic_result'],'PASS_SCOPED')
        self.assertEqual(v['P20_LIVING_FLOOR_CONTINUITY']['diagnostic_result'],'INDETERMINATE')
        self.assertEqual(v['P20_LIVING_SOURCE_SEATS']['diagnostic_result'],'MEASURED_ONLY')
        self.assertEqual(v['P20_LIVING_SHORTER_ALTERNATIVE']['diagnostic_reason'],'NOT_RUN')

    def test_guest_missing_fixture_and_wrong_body_no_pass(self):
        for mod in (lambda x:x['destination_bindings']['living'].pop('fixture_id'),
                    lambda x:x['routes'][0].update(body_m='.7'),
                    lambda x:x['routes'][2].update(wc_exception='Unverified exception'),
                    lambda x:x['routes'][0]['floor_roles'].append('bath'),
                    lambda x:x['routes'].pop(0)):
            v=self.case();mod(v['reports'][p.G]['units'][0])
            self.assertEqual(self.rows(v)['P20_GUEST_FOUR_ROUTES']['diagnostic_result'],'INDETERMINATE')

    def test_evaluator_errors_and_conflict_not_missing(self):
        v=self.case(); v['reports'][p.G]['units'][0]['routes'][0]['state']='UNKNOWN_EVALUATOR_OR_BINDING_ERROR'
        self.assertEqual(self.rows(v)['P20_GUEST_FOUR_ROUTES']['diagnostic_result'],'EVALUATION_ERROR')
        v['reports'][p.G]['units'][0]['routes'][0]['state']='SOURCE_CONFLICT'
        self.assertEqual(self.rows(v)['P20_GUEST_FOUR_ROUTES']['diagnostic_result'],'CONFLICT')
        v['reports'][p.P]['integrity_verified']=False
        self.assertEqual(self.rows(v)['P20_PROGRAM_CAPACITY']['diagnostic_result'],'EVALUATION_ERROR')

    def test_legacy_missing_rule_retained_but_profile_normalized(self):
        v=self.rows(); q=v['P20_PROGRAM_QUALITY_FLOOR']
        self.assertIn('MISSING_RULE',q['archived_runtime_explicit_states'])
        self.assertIn({'kind':'MISSING_RULE','code':ROW[1]},q['archived_findings'])
        self.assertEqual(q['diagnostic_reason'],'PROFILE_NOT_READY')
        self.assertEqual(v['P20_CORE_ENGINEERING']['diagnostic_reason'],'OUT_OF_SCOPE')
        self.assertEqual(v['P20_CORE_ENGINEERING']['diagnostic_result'],'NOT_EVALUATED')
        self.assertIsNone(v['P20_CORE_ENGINEERING']['archived_runtime_explicit_states'])

    def test_remaining_position_alone_is_no_evidence(self):
        v=self.case()
        v['reports'][p.G]['remaining'][0]='Unrelated'
        v['reports'][p.W]['remaining'][3]='Unrelated'
        rows=self.rows(v)
        self.assertEqual(rows['P20_GUEST_FIRST_LIVING']['reason_code'],'EVIDENCE_ABSENT')
        self.assertEqual(rows['P20_CORE_ENGINEERING']['reason_code'],'EVIDENCE_ABSENT')

    def test_capacity_failure_only_bind_real_source_code(self):
        v=self.case(); cap=v['reports'][p.P]['reports']['capacity']
        cap['errors']=[{'code':'ACTUAL_CAPACITY_SHORTFALL','group':'sleeping_places','unit':'A'}]
        self.assertEqual(self.rows(v)['P20_PROGRAM_CAPACITY']['diagnostic_result'],'INDETERMINATE')
        cap['evidence']['units'][0]['actual_places']['sleeping_places']=3
        self.assertEqual(self.rows(v)['P20_PROGRAM_CAPACITY']['diagnostic_result'],'FAIL_SCOPED')
        cap['errors'][0]['group']='dining_seats'
        self.assertEqual(self.rows(v)['P20_PROGRAM_CAPACITY']['diagnostic_result'],'INDETERMINATE')
        cap['errors'][0].update(group='sleeping_places',unit='wrong')
        self.assertEqual(self.rows(v)['P20_PROGRAM_CAPACITY']['diagnostic_result'],'INDETERMINATE')
        cap['errors'][0]['unit']='A'
        cap['evidence']['model_hash']='c'*64
        self.assertEqual(self.rows(v)['P20_PROGRAM_CAPACITY']['diagnostic_result'],'INDETERMINATE')

    def test_missing_scope_is_not_not_applicable_or_pass(self):
        v=self.case(); del v['reports'][p.L]['units'][0]['area_accounting']['verified_useful_living_area_m2']
        del v['reports'][p.L]['units'][1]['area_accounting']['verified_useful_living_area_m2']
        r=self.rows(v)['P20_LIVING_USEFUL_AREA']
        self.assertEqual(r['diagnostic_result'],'INDETERMINATE')
        self.assertEqual(r['reason_code'],'EVIDENCE_ABSENT')

if __name__=='__main__':
    unittest.main()
