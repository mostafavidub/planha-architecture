"""R4-1.01 retained historical baseline audit. No generation or qualification."""
import copy,hashlib,json,pathlib,subprocess,sys
HISTORICAL='a1dcf7827ff59f49b7daa205368fcd2a29c26c27'
PARENT='67857a94b8bab1f46741871fd074e1eafd0c86b8330db13a420d245618df8181'
CHILD='dd3b0a37e617005d69be77ba3f47cce624a827fdad528b4ba7377ffa8916f83a'
COMPLETE='5d41eb715a570420484bca662a99f6a2c4965fce39db770375b7e51839c273e4'
PHYSICAL='f8d212d92e4641f01af6ffd51d09ad9652cc528950a168dffece0cb950854697'
IDS=('CURRENT_PROGRAM_SUITABILITY','KITCHEN_GUEST_PATH_SEPARATION','CONTINUOUS_USEFUL_LIVING','NONFUNCTIONAL_WALL_EXCLUSION')
AUTH=('accepted','qualified','display_allowed','delivery_allowed')
def require(ok,msg):
 if not ok:raise ValueError(msg)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()
def one(root,name):
 paths=list(root.rglob(name));require(len(paths)==1,'UNIQUE_FILE:'+name);return json.loads(paths[0].read_bytes())
def validate(controller,complete,bundle,decision,operator):
 require(controller['head_sha']==HISTORICAL and controller['mode']=='ORIGINAL_CHILD_WIRING','HISTORICAL_COMMIT')
 require(controller['source_integrity_verified'] is True and controller['child_receipt_verified'] is True and controller['account_finalization_verified'] is True,'CONTROLLER_INTEGRITY')
 p=controller['process'];require(type(p['returncode']) is int and p['returncode']==0 and p['wait_completed'] is True and p['timed_out'] is False,'PROCESS')
 require(digest(complete)==COMPLETE==controller['observed_result_digest'],'PINNED_COMPLETE')
 require(complete['nonce']==controller['nonce'] and complete['completed'] is True,'NONCE_COMPLETE')
 require(complete['parent_model_digest']==PARENT and complete['child_model_digest']==CHILD,'LINEAGE')
 require(type(complete['generated_count']) is int and complete['generated_count']==1 and complete['verified_generated_count']==1,'COUNT')
 require(digest(bundle)==complete['child_runtime_digest'],'RUNTIME_DIGEST')
 require(digest(bundle['packet']['world_model'])==bundle['model_digest']==CHILD,'MODEL_DIGEST')
 require(digest(operator)==complete['operator_result_digest'] and operator['child']['model_digest']==CHILD,'OPERATOR')
 require(digest(operator['child']['packet'])==digest(bundle['packet']),'OPERATOR_PACKET')
 require(digest(operator['child']['context'])==digest(bundle['context']),'OPERATOR_CONTEXT')
 for name,r in bundle['reports'].items():
  require(digest(r)==bundle['report_digests'][name]==complete['report_digests'][name]==digest(complete['reports'][name]),'REPORT_BINDING:'+name)
 require(bundle['report_digests']['physical']==PHYSICAL and bundle['reports']['physical']['model_hash']==CHILD,'PHYSICAL_MODEL')
 require(bundle['reports']['replay']['verified'] is True and bundle['reports']['replay']['model_hash']==CHILD,'REPLAY_MODEL')
 require(digest(decision)==complete['current_decision_digest'] and decision['integrity_verified'] is True,'DECISION')
 require(decision['model_digest']==CHILD and decision['physical_digest']==PHYSICAL,'DECISION_MODEL')
 require(digest(decision['original_reports'])==digest(bundle['reports']),'DECISION_ORIGINALS')
 require(set(decision['assessments'])==set(IDS) and set(decision['assessment_digests'])==set(IDS),'FOUR_SET')
 require(len(decision['criteria'])==4 and {x['criterion'] for x in decision['criteria']}==set(IDS),'FOUR_ROWS')
 for cid,r in decision['assessments'].items():
  require(digest(r)==decision['assessment_digests'][cid] and r['model_digest']==CHILD,'ASSESSMENT:'+cid)
  require(all(r[k] is False for k in AUTH),'ASSESSMENT_AUTHORITY')
 require(digest(decision['decision'])==digest(complete['current_decision'])==digest(controller['decision']),'DECISION_CHAIN')
 require(all(v[k] is False for v in (controller,complete,bundle,decision) for k in AUTH),'FALSE_AUTHORITY')
 require(controller['account']['parent_model_digest']==PARENT and controller['account']['history'][0]['observed_model_digest']==CHILD,'ACCOUNT_LINEAGE')
 return True
def audit(root):
 paths=sorted(p for p in root.rglob('*') if p.is_file())
 before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
 names=['controller-receipt.json','repair-complete.json','child-runtime-bundle.json','child-current-decision.json','operator-result.json']
 values=[one(root,n) for n in names];controller,complete,bundle,decision,operator=values
 validate(*values)
 require([digest(one(root,n)) for n in names]==list(map(digest,values)),'REREAD_CHANGED')
 negatives=[]
 for label,mutate in [
  ('world_model_changed',lambda v:v[2]['packet']['world_model']['program'].__setitem__('units',2.0)),
  ('physical_model_swapped',lambda v:v[2]['reports']['physical'].__setitem__('model_hash',PARENT)),
  ('current_assessment_swapped',lambda v:v[3]['assessments'][IDS[0]].__setitem__('model_digest',PARENT)),
  ('authority_changed',lambda v:v[0].__setitem__('qualified',True))]:
  v=copy.deepcopy(values);mutate(v)
  try:validate(*v)
  except ValueError as ex:negatives.append({'case':label,'rejected':str(ex)})
  else:raise AssertionError('MUTATION_ACCEPTED:'+label)
 snapshots={}
 for record in [controller,complete,decision,*decision['assessments'].values()]:
  for key in ('source_snapshot','decision_source_snapshot'):
   for path,h in record.get(key,{}).items():
    require(path.startswith(('app/','specs/')) and '..' not in pathlib.PurePosixPath(path).parts,'SOURCE_PATH')
    require(path not in snapshots or snapshots[path]==h,'SOURCE_CONFLICT')
    historical=subprocess.check_output(['git','show',HISTORICAL+':'+path])
    require(hashlib.sha256(historical).hexdigest()==h,'HISTORICAL_SOURCE:'+path);snapshots[path]=h
 current_differences=[]
 for path,h in snapshots.items():
  current=hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
  if current!=h:current_differences.append({'path':path,'historical_sha256':h,'current_sha256':current})
 contract='app/local_integration/public_wln_contract.py'
 old=subprocess.check_output(['git','show',HISTORICAL+':'+contract]);now=pathlib.Path(contract).read_bytes()
 require(b'V25_PUBLIC_WLN_CONTRACT_V1' in old and b'V25_PUBLIC_WLN_CONTRACT_V2' in now,'PUBLIC_VERSION_DISTINCTION')
 require(before=={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'FILES_CHANGED')
 out={'schema':'R4_BASELINE_AUDIT_V1','task':'R4-1.01','state':'HISTORICAL_BASELINE_VERIFIED_NOT_QUALIFIED',
 'historical_commit':HISTORICAL,'audit_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 'parent_model_digest':PARENT,'child_model_digest':CHILD,'binding':bundle['binding'],
 'engine_revision':bundle['engine_revision'],'packet_family':bundle['packet']['family'],
 'actual_model_program':bundle['packet']['world_model']['program'],
 'report_digests':bundle['report_digests'],'physical_status':bundle['reports']['physical']['status'],
 'physical_error_count':len(bundle['reports']['physical']['errors']),'physical_pending_count':len(bundle['reports']['physical']['pending']),
 'criteria':decision['criteria'],'decision':decision['decision'],'file_sha256':before,
 'canonical_file_digests':dict(zip(names,map(digest,values))),'historical_source_snapshot':snapshots,
 'current_source_differences':current_differences,'public_contract_versions':{'historical':'V1','current':'V2','historical_sha256':hashlib.sha256(old).hexdigest(),'current_sha256':hashlib.sha256(now).hexdigest(),'fresh_V2_runtime_claim':False},
 'negative_tests':negatives,'reread_verified':True,'fresh_geometry_executed':False,
 'scope':'Byte-pinned historical artifact and report/model/source linkage. No replay or gate recomputation, no current-V2 compatibility or architectural acceptance claim. Full originals remain in pinned source artifact.',
 'remaining':['Four current conditions remain unresolved; see individual evidence','Historical V1 input evidence cannot establish fresh current V2 execution','Full artifact expires; small baseline manifest alone cannot reconstruct its geometry'],
 **{k:False for k in AUTH}}
 return out
if __name__=='__main__':
 out=audit(pathlib.Path(sys.argv[1]));pathlib.Path(sys.argv[2]).write_text(json.dumps(out,sort_keys=True,indent=2,ensure_ascii=False))
 print(json.dumps(out,sort_keys=True,ensure_ascii=False))
