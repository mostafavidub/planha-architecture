"""One fresh interpreter per declared source/reviewer phase. Test-only."""
import hashlib,json,sys,time,traceback
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;WORKSPACE=ROOT.parent
phase,folder,budget,run_id=sys.argv[1:];folder=Path(folder);budget=float(budget)
def failure(t,e,tb):
 with(folder/(phase+'_error.json')).open('x')as f:
  json.dump({'type':t.__name__,'message':str(e),'traceback':''.join(traceback.format_exception(t,e,tb))},f,indent=2)
 sys.__excepthook__(t,e,tb)
sys.excepthook=failure
sys.path.insert(0,str(WORKSPACE/'staging369_current_family_repair'))
from operator369 import digest
def read(name):return json.loads((folder/name).read_text())
def write(name,value):
 with(folder/name).open('x')as stream:json.dump(value,stream,ensure_ascii=False,indent=2)
if phase=='construct':
 sys.path.insert(0,str(ROOT/'staging369_current_source_validation'))
 from source369 import construct
 parent=json.loads((HERE/'parent368.json').read_text())
 record=construct(parent,'sofa1_use','-3/2','0',purpose='CONTROLLED_TEST_FIXTURE')
 write('fixture_record.json',record)
elif phase in ('fresh_first','fresh_second'):
 sys.path.insert(0,str(ROOT/'staging369_current_source_validation'))
 from evaluate369 import evaluate369
 record=read('fixture_record.json'if phase=='fresh_first'else'repaired_record.json')
 result=evaluate369(record,min(90,budget));write(phase+'.json',result)
elif phase=='propose':
 from operator369 import propose,rect,overlap
 record=read('fixture_record.json');fresh=read('fresh_first.json')
 unit=next(u for u in record['candidate']['model']['units']if u['id']=='A')
 if not overlap(rect(unit['fixtures']['sofa1']),rect(unit['fixtures']['armchair2'])):
  raise ValueError('DECLARED_CONTROLLED_COLLISION_NOT_PRODUCED')
 candidate_id=digest({'run_id':run_id,'model_digest':record['candidate']['model_digest'],'kind':'TEST_ONLY_DERIVED_BALANCED369'})
 binding={'run_id':run_id,'candidate_id':candidate_id,'review_id':fresh['review_id'],
          'record_digest':digest(record),'model_digest':record['candidate']['model_digest'],'fresh_digest':digest(fresh)}
 write('fixture_binding.json',binding)
 start=time.monotonic()
 try:
  plan=propose(record,fresh,binding)
  result={'status':'PROPOSAL_PREPARED','plan':plan,'seconds':time.monotonic()-start}
 except(ValueError,KeyError,TypeError)as error:
  result={'status':'STRICT_REJECTION_GATE_BLOCKED','reason':str(error),'seconds':time.monotonic()-start,
          'repair_attempted':False,'accepted':False,'delivery_allowed':False}
 write('proposal_result.json',result)
elif phase=='reconstruct_repair':
 from reconstruct369 import reconstruct
 result=reconstruct(read('fixture_record.json'),read('proposal_result.json')['plan'],run_id,ROOT)
 write('repaired_record.json',result['record']);write('repair_lineage.json',result['lineage'])
else:raise ValueError('UNREGISTERED_PHASE')
