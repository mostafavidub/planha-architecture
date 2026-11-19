"""R4-1.08 targeted counterexample proof; no admission or natural-failure claim."""
import hashlib,inspect,sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
sys.path[:0]=[str(ENGINE),str(ROOT/'app/local_integration'),str(ROOT/'studies/r4')]
from same_version_front_rear_contract import digest
from source_fit_profile207 import profiles,source_check
BEGIN=' # BEGIN R4_108_TARGETED_COUNTEREXAMPLE_SELECTOR\n'
END=' # END R4_108_TARGETED_COUNTEREXAMPLE_SELECTOR\n'
PINS={'app/reconstruction357/planha_general150_runtime_work/search114.py':'65e0f278c9f9ef480388d3ea8056161c0a938a36',
 'app/local_integration/cause_directed_candidate108.py':'5851a0e98162776ca292b40a5707d0ef8f477c8b',
 'app/local_integration/cause_directed_contract108.py':'f07e20e250199a51fce9a9042ea854258345310f',
 'studies/r4/actual_descriptor301.py':'02c3126479b9fee410d985afb7e58205bb55c0b3',
 'studies/r4/semantic_descriptor301.py':'8bdcf838386ea798405b8bc3d43b355fe0957777'}
def need(ok,code):
 if not ok:raise ValueError(code)
def strip_selector(text):
 need(text.count(BEGIN)==1 and text.count(END)==1,'SELECTOR_MARKERS')
 a,tail=text.split(BEGIN);_,b=tail.split(END)
 return a+b
def source_guard():
 for name,pin in PINS.items():
  b=(ROOT/name).read_bytes()
  need(hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==pin,'REGRESSION_SOURCE_PIN')
 import search114,cause_parent_witness108 as witness
 for mod in(search114,witness):
  expected=ENGINE/'search114.py'if mod is search114 else ROOT/'app/local_integration/cause_parent_witness108.py'
  need(Path(inspect.getsourcefile(mod.propose)).resolve()==expected,'REGRESSION_IMPORT_PATH')
 need(strip_selector((ROOT/'app/local_integration/cause_parent_witness108.py').read_text())==(ENGINE/'search114.py').read_text(),'ORIGINAL_SOURCE_CHANGED')
 source_check()
 return True
def compare_capture(base,extended):
 A=base['matrix'];B=extended['matrix'];m,n=A.shape
 need(B.shape[0]>m and B.shape[1]>n,'SELECTOR_ADDITIONS_REQUIRED')
 C=B[:m,:n].tocsr()
 for key in('data','indices','indptr'):
  need(np.array_equal(getattr(A,key),getattr(C,key)),'ORIGINAL_CSR_CHANGED')
 need(B[:m,n:].nnz==0,'OLD_ROWS_EXTRA_COLUMNS')
 for key in('objective','integrality'):
  need(np.array_equal(base[key],extended[key][:n]),'ORIGINAL_'+key.upper()+'_CHANGED')
 for key in('lb','ub'):
  need(np.array_equal(getattr(base['bounds'],key),getattr(extended['bounds'],key)[:n]),'ORIGINAL_BOUNDS_CHANGED')
 for key in('lower','upper'):
  need(np.array_equal(base[key],extended[key][:m]),'ORIGINAL_ROW_BOUNDS_CHANGED')
 need(base['specs']==extended['specs']and base['row_metadata']==extended['row_metadata'][:m],'ORIGINAL_METADATA_CHANGED')
 k=len(profiles()['bath_apron'])
 need(B.shape==(m+4*k+1,n+k),'SELECTOR_SHAPE')
 need(np.array_equal(extended['objective'][n:],np.zeros(k))and np.array_equal(extended['integrality'][n:],np.ones(k)),'SELECTOR_VARIABLES')
 need(np.array_equal(extended['bounds'].lb[n:],np.zeros(k))and np.array_equal(extended['bounds'].ub[n:],np.ones(k)),'SELECTOR_BOUNDS')
 return {'verified':True,'original_rows':m,'original_columns':n,'added_rows':4*k+1,'added_binary_columns':k,
  'original_csr_digest':hashlib.sha256(A.data.tobytes()+A.indices.tobytes()+A.indptr.tobytes()).hexdigest(),
  'scope':'Exact original CSR/bounds/objective/integrality/specs/metadata retained; added diagnostic selector only'}
def constraint_retention(core):
 source_guard()
 import search114,cause_parent_witness108 as witness
 opts={'sleep_roles':['double','twin'],'variant':0,'topology':'SIDE_ROOTED_SERVICES','diagnostic_capture':lambda d:d}
 a=search114.propose(core,2,**opts);b=witness.propose(core,2,**opts)
 result=compare_capture(a,b);source_guard();return result
def selector_geometry(proposal):
 from core_wall_audit118 import q
 from contract114 import GRID
 r=proposal['rectangles'];bath=q(r['bath']);dining=q(r['dining'])
 overlaps=[]
 for piece in profiles()['bath_apron']:
  a,b,c,d=q(piece);a+=bath[0];c+=bath[0];b+=bath[1];d+=bath[1]
  overlaps.append(min(c,dining[2])-max(a,dining[0])>=GRID and min(d,dining[3])-max(b,dining[1])>=GRID)
 return {'positive_source_piece_overlap':any(overlaps),'overlapping_piece_count':sum(overlaps),
  'scope':'One GRID positive overlap is regression witness selection, not architectural acceptance threshold'}
def bind_current(name,report,evidence):
 import actual_descriptor301 as a
 need(Path(inspect.getsourcefile(a.current_report_binding)).resolve()==ROOT/'studies/r4/actual_descriptor301.py','CURRENT_BINDER_PATH')
 a.current_report_binding(name,report,evidence)

def readback(folder,result):
 """Data consistency only, no replay/evaluator/solver execution."""
 import json,math
 def read(path):
  with path.open('rb')as f:data=f.read(96*1024*1024+1)
  need(len(data)<=96*1024*1024,'READBACK_BYTE_LIMIT')
  def bad(value):raise ValueError('READBACK_NONFINITE')
  def unique(rows):
   out={}
   for k,v in rows:need(k not in out,'READBACK_DUPLICATE_KEY');out[k]=v
   return out
  return json.loads(data,parse_constant=bad,object_pairs_hook=unique)
 reports=read(folder/'reports.json')
 need(type(reports)is dict and type(result.get('report_digests'))is dict,'READBACK_REPORT_FIELDS')
 need(set(reports)==set(result['report_digests']),'READBACK_REPORT_SET')
 for key,value in reports.items():need(digest(value)==result['report_digests'][key],'READBACK_REPORT_DIGEST')
 bundles=0
 for label in('parent','child'):
  key=label+'_bundle_digest'
  if key not in result:continue
  bundle=read(folder/(label+'-bundle.json'));bundles+=1
  need(digest(bundle)==result[key],'READBACK_BUNDLE_DIGEST')
  mh=digest(bundle['packet']['world_model'])
  need(mh==result[label+'_model_digest'],'READBACK_MODEL')
  if label+'_physical'in reports:
   physical=reports[label+'_physical'];need(physical['model_hash']==mh,'READBACK_PHYSICAL_MODEL')
   from one_bed_pair_source_study import code_counts
   expected={'status':physical.get('status'),'errors':code_counts(physical.get('errors',[])),'pending':code_counts(physical.get('pending',[])),
    'not_evaluated_count':len(physical.get('not_evaluated',[])),'out_of_scope_count':len(physical.get('out_of_scope',[]))}
   need(digest(result[label+'_physical'])==digest(expected),'READBACK_PHYSICAL_SUMMARY')
  if label+'_replay'in reports:need(reports[label+'_replay']['model_hash']==mh,'READBACK_REPLAY_MODEL')
 if 'cause_resolution'in reports:
  resolution=reports['cause_resolution']
  need(digest(result.get('resolution_rows'))==digest(resolution['rows']),'READBACK_RESOLUTION_ROWS')
  expected=resolution['all_target_causes_resolved'] and not resolution['new_supported_causes']
  need(result.get('cause_repair_verified')is expected,'READBACK_RESOLUTION_STATE')
  need(result.get('protected_verified')is reports['child_preservation']['protected_verified'],'READBACK_PROTECTION_STATE')
 return {'verified':True,'bundle_count':bundles,'full_report_count':len(reports),'reports_file_digest':hashlib.sha256((folder/'reports.json').read_bytes()).hexdigest(),
  'scope':'Same-process file consistency readback, not independent engine replay or durable archive'}
