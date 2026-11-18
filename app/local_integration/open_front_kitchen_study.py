"""Independent open-front kitchen study. No whole-model or historical admission."""
from copy import deepcopy
from fractions import Fraction as F
import hashlib,inspect
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'manifests/WORKTREE_STATE.json').is_file())
ENGINE=ROOT/'app/reconstruction357/planha_general150_runtime_work'
SCHEMA='KITCHEN_OPEN_FRONT_STUDY_V1'
def source():
    import kitchen_module117
    if Path(inspect.getsourcefile(kitchen_module117.build)).resolve()!=(ENGINE/'kitchen_module117.py').resolve():
        raise ValueError('KITCHEN_BASE_IMPORT_PATH')
    return kitchen_module117
def build(width,depth):
    from contract114 import S,digest
    base=source().build(width,depth);m=deepcopy(base)
    m['schema']=SCHEMA;m['contract_version']='OPEN_FRONT_CONTROLLED_DELTA_V1'
    del m['walls']['front.right']
    m['openings'][0]['rect']=[S(F('.6')),S(F('-.15')),S(F(str(width))),'0']
    m['source_binding']={'producer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'base_module_digest':digest(base),'base_producer_sha256':base['source_binding']['producer_sha256'],
        'fixture_source_sha256':base['source_binding']['fixture_source_sha256'],
        'delta_contract':'remove front.right; expand existing permanent arch to W; retain every other value'}
    return m
