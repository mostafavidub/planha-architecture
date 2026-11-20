"""Optional, response-scoped capability disclosure. Never an execution decision."""
import hashlib,json,re

SCHEMA='PUBLIC_WLN_CAPABILITY_P36_V1'
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
CURRENT=('CURRENT_PROGRAM_SUITABILITY','KITCHEN_GUEST_PATH_SEPARATION','CONTINUOUS_USEFUL_LIVING','NONFUNCTIONAL_WALL_EXCLUSION')
PAIR='HTTP_FULL_EVIDENCE_X07_V1'
SINGLE='SINGLE_READBACK_P17_V1'
PLANS={'FRONT_REAR':('CONSTRUCTOR127_COMPACT_PAIR','PROGRAM_2BED_V1'),'SINGLE_FRONT_TOP_CORE_P15_V1':('SINGLE_CONSTRUCTION_REPLAY_P15_V1','PROGRAM_2BED_V1')}
COMPLETED='LIVE_ORIGINAL_CHAIN_AND_CURRENT_DECISION_COMPLETED_NOT_QUALIFIED'
PAIR_STATE='LIVE_SINGLE_CASE_EVIDENCE_RECORDED_NOT_QUALIFIED'
BLOCKED='BLOCKED'

def h(v,n=64):return type(v)is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',v) is not None
def as_dict(v):return v if type(v)is dict else {}
def authority_false(v):return type(v)is dict and all(v.get(k)is False for k in AUTH)
def number(q):
 p=as_dict(q)
 return set(p)=={'numerator','denominator'} and all(type(x)is str and re.fullmatch('[1-9][0-9]{0,70}',x) for x in p.values())
def canonical(envelope,body_pin):
 e=as_dict(envelope);raw=as_dict(e.get('canonical_request'));d=as_dict(raw.get('dimensions_m'));n=raw.get('unit_count')
 if e.get('schema')!='V25_PUBLIC_WLN_CONTRACT_V3' or e.get('transport_body_sha256')!=body_pin or set(d)!={'W','L'} or type(n)is not int or n not in (1,2) or not all(number(v)for v in d.values()):return None
 return {'dimensions_m':{k:dict(v)for k,v in d.items()},'unit_count':n}

def evidence(body_pin,case,result):
 r=as_dict(result);rows=r.get('attempts');decision=as_dict(r.get('current_decision'));proof=as_dict(r.get('http_full_evidence'))
 if not (r.get('fresh_model_executed')is True and r.get('source_integrity_verified')is True and
     authority_false(r) and authority_false(decision) and decision.get('state')=='BLOCKED' and type(rows)is list and len(rows)==1 and
     as_dict(rows[0]).get('receipt_verified')is True and proof.get('binding_verified')is True):return None
 row=rows[0];n=case['unit_count']
 if n==2 and proof.get('schema')==PAIR and r.get('schema')=='AUTOMATIC_PROGRAM_LIVE_SINGLE_CASE_V1':
  if (r.get('state')==PAIR_STATE and row.get('state')==COMPLETED and proof.get('request_digest')==body_pin and
   proof.get('state')=='SAME_REQUEST_FULL_REPORT_CONSISTENCY_VERIFIED_SCOPED' and type(proof.get('file_count'))is int and proof['file_count']==9 and
   all(h(proof.get(k))for k in ('nonce_digest','model_digest','decision_digest','source_digest','file_hashes_digest')) and
   h(row.get('nonce'),32) and hashlib.sha256(json.dumps(row['nonce']).encode()).hexdigest()==proof['nonce_digest'] and row.get('model_digest')==proof['model_digest'] and row.get('decision_digest')==proof['decision_digest'] and
   authority_false(proof)):return PAIR
 if n==1 and proof.get('schema')==SINGLE and r.get('schema')=='SINGLE_HTTP_RESULT_P17_V1':
  diag=as_dict(r.get('http_diagnostic'));hashes=as_dict(row.get('observed_file_hashes'));states=as_dict(row.get('current_states'))
  d_files=as_dict(diag.get('observed_file_hashes'))
  if (r.get('state')==BLOCKED and row.get('state')=='FULL_SINGLE_EVALUATION_COMPLETE_BLOCKED' and row.get('timed_out')is False and
   row.get('wait_completed')is True and type(row.get('returncode'))is int and row['returncode']==0 and
   diag.get('schema')=='P17_PRIVATE_DIAGNOSTIC_V1' and diag.get('request_digest')==body_pin and
   diag.get('source_integrity_observed')is True and diag.get('within_budget_observed')is True and h(row.get('nonce'),32) and
   diag.get('runtime_nonce')==row['nonce'] and diag.get('observed_model_digest')==row.get('model_digest') and
   row.get('model_digest')==row.get('observed_model_digest')==hashes.get('model') and h(row.get('model_digest')) and
   h(row.get('runtime_digest')) and hashes.get('summary')==row['runtime_digest'] and h(hashes.get('decision')) and all(hashes[k]==d_files.get(k)for k in ('model','summary','decision')) and set(states)==set(CURRENT)):return SINGLE
 return None

def disclose(*,kind,body=None,envelope=None,preflight=None,result=None):
 p=as_dict(preflight);r=as_dict(result)
 body_pin=hashlib.sha256(body).hexdigest()if type(body)is bytes else None
 c=canonical(envelope,body_pin)if body_pin else None
 valid=c is not None and p.get('input_valid')is True
 ready=valid and p.get('execution_ready')is True
 permitted={'STUDY_PERMITTED','STUDY_BUSY','STUDY_RESULT_WITHHELD','SERVER_RESULT_UNAVAILABLE'}
 selected=None
 if ready and kind in permitted:
  family='SINGLE_FRONT_TOP_CORE_P15_V1'if c['unit_count']==1 else'FRONT_REAR'
  contract,programme=PLANS[family]
  selected={'family':family,'contract':contract,'programme':programme}
 proof=None
 if kind=='STUDY_PERMITTED' and ready:
  # Bind to the actual server preflight's original parsed envelope, not a
  # guessed type or an aliased/stale runtime preflight.
  runtime_pf=as_dict(r.get('preflight'))
  q=runtime_pf.get('envelope')if c['unit_count']==1 else runtime_pf.get('public_envelope')
  if canonical(q,body_pin)==c and runtime_pf.get('execution_ready')is True:proof=evidence(body_pin,c,r)
 return {'schema':SCHEMA,'request_digest':body_pin,
  'input_state':'VALID'if valid else kind if kind in ('INVALID_INPUT','WIRE_UNSUPPORTED')else'UNASSESSED',
  'capability_state':kind,'canonical_case':c if valid else None,'selected_study':selected,
  'evidence_state':'SAME_REQUEST_STUDY_REPORTS_VERIFIED'if proof else'NOT_VERIFIED',
  'evidence_contract':proof,'product_available':False,**{k:False for k in AUTH}}
