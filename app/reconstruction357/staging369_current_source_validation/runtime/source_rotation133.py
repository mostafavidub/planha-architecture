"""Versioned D4 source extension. Does not modify or grant receipts to base source."""
from pathlib import Path
import hashlib
from contract114 import digest
MATRICES=[[[1,0],[0,1]],[[1,0],[0,-1]],[[-1,0],[0,1]],[[-1,0],[0,-1]],[[0,1],[1,0]],[[0,1],[-1,0]],[[0,-1],[1,0]],[[0,-1],[-1,0]]]
def build(role='double'):
 if role=='double':
  from bedroom_module116 import build as base
  name='bedroom_module116.py';m=base('5.45','3.6')
 elif role=='twin':
  from twin_module118 import build as base
  name='twin_module118.py';m=base('5.45','4.5')
 else:raise ValueError('UNSUPPORTED_REVIEWED_SOURCE_ROLE')
 return {'schema':'ROTATABLE_PRIVATE_SOURCE133','contract_version':'D4_SOURCE_EXTENSION_133_V1','base_module':m,'base_hash':digest(m),'placement_contract':{'allowed_matrices':MATRICES,'scale_allowed':False,'revalidate_after_placement':True},'provenance':{'base_producer':name,'base_producer_sha256':hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest(),'scope':'SOURCE_GEOMETRY_D4_EXTENSION_NOT_WHOLE_PLAN'},'accepted':False}
