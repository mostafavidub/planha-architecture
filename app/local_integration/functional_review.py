"""Source-profile internal capacity evidence, NOT a complete architectural gate.
Furniture is internal witness only and never a required output layer.
"""
import hashlib,json,sys
from pathlib import Path
from review_cycle import digest
ROOT=next(p for p in Path(__file__).resolve().parents if(p/'manifests/WORKTREE_STATE.json').is_file())
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'

def assess(model,physical_review,source_revision):
    local_files=['functional_review.py','guest_four_route_diagnostic.py','kitchen_guest_review.py','living_connectivity_diagnostic.py']
    local_before={n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in local_files}
    model_hash=digest(model)
    if physical_review.get('model_hash')!=model_hash:raise ValueError('FUNCTIONAL_MODEL_BINDING')
    sys.path.insert(0,str(ENGINE))
    from program_capacity_audit118 import examine
    result=examine(model)
    if result['evidence']['model_hash']!=model_hash:raise ValueError('CAPACITY_MODEL_BINDING')
    status='FAIL'if result['errors']else'UNKNOWN'if result['pending']else'PASS_SCOPED'
    requirements=[{'id':'INTERNAL_INSTANCE_CAPACITY','state':status,'basis':'actual source-profile instances and limited planar access, not area or room labels'},
      {'id':'CURRENT_PROGRAM_SUITABILITY','state':'UNKNOWN','basis':'actual supplied source profile is provisional; no current automatic programme suitability proof'},
      {'id':'KITCHEN_GUEST_PATH_SEPARATION','state':'UNKNOWN','basis':'four-route source-profile evidence attached; guest-first-living, scenario completeness, doorway/bottleneck and ergonomic closure remain unproven'},
      {'id':'CONTINUOUS_USEFUL_LIVING','state':'UNKNOWN','basis':'seat-access connectivity study attached; coherent group, shorter organization, functional activities and useful area remain unproved'},
      {'id':'NONFUNCTIONAL_WALL_EXCLUSION','state':'UNKNOWN','basis':'no per-wall alternative/removal comparison proving current owner requirement'}]
    from guest_four_route_diagnostic import assess as guest_study
    guest=guest_study(model)
    if guest['model_digest']!=model_hash:raise ValueError('GUEST_STUDY_MODEL_BINDING')
    from living_connectivity_diagnostic import assess as living_study
    living=living_study(model)
    if living['model_digest']!=model_hash:raise ValueError('LIVING_STUDY_MODEL_BINDING')
    local_hashes={n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in local_files}
    if local_hashes!=local_before:raise ValueError('LOCAL_FUNCTIONAL_SOURCE_CHANGED')
    files=['program_capacity_audit118.py','dining_motion_audit118.py','public_program_audit118.py','fixture_catalog114.json']
    return {'schema':'MAC_FUNCTIONAL_REVIEW_V1','model_digest':model_hash,'physical_review_digest':digest(physical_review),'source_revision':source_revision,
      'declared_source_program':model.get('program',{}),'internal_capacity':result,'guest_four_route_study':guest,'living_connectivity_study':living,'local_review_source_hashes':local_hashes,'requirements':requirements,'state':'REJECTED_FUNCTIONAL'if status=='FAIL'else'UNKNOWN_REQUIRED_FUNCTIONAL_PROOF',
      'display_allowed':False,'accepted':False,'delivery_allowed':False,'qualified':False,'source_hashes':{n:hashlib.sha256((ENGINE/n).read_bytes()).hexdigest()for n in files},
      'scope':'Internal planar capacity of provisional source profile only. Furniture omitted from user Preview/DXF. No complete architectural, ergonomic, programme or regulatory approval.'}
