"""Ephemeral request-owned full-report consumer. No persistence/export/admission.
Consumes the real file shapes before the request TemporaryDirectory is cleaned.
Controlled tempfile tests are NOT a fresh generation or authenticated execution.
"""
import copy
import hashlib
import json
import inspect
from pathlib import Path
from obligation_admission111 import digest, require, coverage_contract, AUTH
import current_report_adapter111 as adapter
MODS = {
 'current_programme_evaluator': 'CURRENT_PROGRAM_SUITABILITY',
 'source_guest_route_evaluator': 'KITCHEN_GUEST_PATH_SEPARATION',
 'source_living_evaluator': 'CONTINUOUS_USEFUL_LIVING',
 'source_wall_function_evaluator': 'NONFUNCTIONAL_WALL_EXCLUSION'}
def cycle_preflight(body):
    from request_trace109 import preflight
    pf = preflight(body)
    return {'schema':'CYCLE_PREFLIGHT112_V1', 'state':'NO_GO_COMPLETE_CYCLE',
            'target_public_raw':{'W':'18','L':'20','n':2,'requested_count':1},
            'requested_raw':pf['raw'], 'study_parent_ready':pf['execution_ready'],
            'reasons':['PUBLIC18X20_DIFFERS_FROM_STUDY18X22',
                       'PARENT_ONLY_NO_POSITIVE_REPAIR_CONTROLLER',
                       'QUALIFIED_WITNESS_ABSENT','DURABLE_REPLAY_BUNDLE_ABSENT'],
            **{k:False for k in AUTH}}
def _consume(folder, request, expected_request, process, reserved, expected_reserved, observed):
    import request_trace109 as trace
    import request_budget110 as ledger
    require(Path(inspect.getsourcefile(adapter.adapt)).resolve() == trace.ROOT/'app/local_integration/current_report_adapter111.py', 'ADAPTER_IMPORT')
    require(Path(inspect.getsourcefile(ledger.check)).resolve() == trace.ROOT/'app/local_integration/request_budget110.py', 'LEDGER_IMPORT')
    trace.validate_request(request, expected_request)
    anchor = ledger.anchor(request, expected_request)
    ledger.check(reserved, expected_reserved, anchor)
    require(reserved['state']=='ACTIVE' and reserved['active'] is not None, 'RESERVATION_REQUIRED')
    folder=Path(folder)
    # Fixed internal names only; no caller-selected file or public locator.
    paths={k:folder/(k+'.json') for k in ('summary','reports')}
    require(all(p.is_file() and not p.is_symlink() for p in paths.values()), 'FULL_REPORT_FILES_REQUIRED')
    # Private, process-local observation only. Never a verified receipt or public payload.
    data={}; hashes={}
    observed.update(raw_file_bytes=data, file_sha256=hashes, file_byte_count={},
                    raw_preservation='PARTIAL_FILE_BYTES_OBSERVED_UNVERIFIED',
                    observation_verified=False)
    for k,p in paths.items():
        data[k]=p.read_bytes()
        hashes[k]=hashlib.sha256(data[k]).hexdigest()
        observed['file_byte_count'][k]=len(data[k])
    observed['raw_preservation']='FILE_BYTES_OBSERVED_UNVERIFIED'
    def unique(pairs):
        result={}
        for k,v in pairs:
            require(k not in result, 'DUPLICATE_JSON_KEY')
            result[k]=v
        return result
    def invalid_number(value):
        raise ValueError('NONFINITE_JSON')
    parsed={}; parse_errors={}
    for k,v in data.items():
        try:
            parsed[k]=json.loads(v, object_pairs_hook=unique, parse_constant=invalid_number)
            observed['original_'+k]=copy.deepcopy(parsed[k])
        except (ValueError,TypeError,UnicodeError,RecursionError) as exc:
            parse_errors[k]=type(exc).__name__
    observed['file_parse_errors']=parse_errors
    if parse_errors:
        raise ValueError('FILE_JSON_PARSE_FAILED')
    out,reports=parsed['summary'],parsed['reports']
    observed['raw_reports_digest']=digest(reports)
    trace.bind_result(request,expected_request,out,reports,process)
    evidence={'schema':'EPHEMERAL_EVIDENCE112_V1','original_summary':copy.deepcopy(out),
              'original_reports':copy.deepcopy(reports),'file_sha256':hashes,
              'raw_reports_digest':digest(reports),'durable':False,
              'execution_authenticity_verified':False,**{k:False for k in AUTH}}
    safe={'schema':'LIFECYCLE_ADAPTER112_V1','state':'SKIPPED_NO_PARENT',
          'consistency_verified':True,'adapter_executed':False,
          'raw_report_count':len(reports),'raw_reports_digest':digest(reports),
          'file_sha256':hashes,'request_digest':expected_request,
          'nonce':request['nonce'],'account_id':request['account_id'],
          'reserved_account_digest':expected_reserved,'source_digest':digest(request['source_snapshot']),
          'programme_digest':request['programme_digest'],'durable_full_reports':False,
          'live_execution_authenticated':False,**{k:False for k in AUTH}}
    if out['state']=='BLOCKED_NO_PARENT_PROPOSAL':
        require(out.get('parent_model_digest') is None, 'NO_PARENT_MODEL_CONFLICT')
    if out['state']!='BLOCKED_NO_PARENT_PROPOSAL':
        raw={'physical':reports['parent_physical'],'replay':reports['parent_replay'],
             'current':{cid:reports['parent_current_'+mod] for mod,cid in MODS.items()}}
        c=coverage_contract()
        binding={'request_digest':expected_request,'model_digest':out['parent_model_digest'],
                 'source_digest':digest(request['source_snapshot']),
                 'profile_digest':request['programme_digest'],
                 'rule_digest':c['source_map_digest'],'coverage_digest':digest(c)}
        converted=adapter.adapt(raw,digest(raw),binding,digest(binding))
        evidence['adapter']=converted
        observed['adapter']=copy.deepcopy(converted)
        require(converted['consistency_verified'] is True,'RAW_ADAPTER_NOT_VERIFIED')
        safe.update(state=converted['state'],adapter_executed=True,
                    model_digest=out['parent_model_digest'],adapter_digest=digest(converted),
                    declared_row_count=len(converted['decision']['rows']),
                    decision_blocker_count=len(converted['decision']['blockers']),
                    rule_digest=binding['rule_digest'],coverage_digest=binding['coverage_digest'])
    require(all(p.read_bytes()==data[k] for k,p in paths.items()),'FILE_CHANGED_DURING_CONSUMPTION')
    trace.validate_request(request,expected_request)
    ledger.check(reserved,expected_reserved,anchor)
    return out,reports,{'safe_summary':safe,'private_evidence':evidence}

class EvidenceFailure(ValueError):
    """Internal-only evidence; message never includes raw report content."""
    def __init__(self, evidence, error_type):
        super().__init__('LIFECYCLE_EVIDENCE_FAILED_CLOSED')
        self.private_evidence=evidence
        self.error_type=error_type
def consume(folder, request, expected_request, process, reserved, expected_reserved):
    observed={'raw_preservation':'NOT_ESTABLISHED','durable':False,**{k:False for k in AUTH}}
    try:
        result=_consume(folder,request,expected_request,process,reserved,expected_reserved,observed)
        return result
    except (ValueError,KeyError,TypeError,OSError,UnicodeError,RecursionError) as exc:
        if 'original_reports' in observed:observed['raw_preservation']='PARSED_JSON_COPY'
        raise EvidenceFailure(observed,type(exc).__name__) from None
