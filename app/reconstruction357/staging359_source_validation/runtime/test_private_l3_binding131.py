"""Negative binding tests; no solve/render/assembler. constructor builds core contract only."""
import copy,json
from pathlib import Path
from fractions import Fraction as F
from constructor129 import frame
from private_l3_binding131 import examine
from frame_audit125 import digest,rectangle
P=Path(__file__).parent;D=P/'evidence_l3_whole131'
c,_=frame({'W':'37.45','L':'19.97','n':2,'requested_count':6},'LEFT_RIGHT');l=json.loads((D/'local.json').read_text());w=json.loads((D/'world.json').read_text())
b=examine(w,l,c);assert not b['errors']and not b['pending'],b
out={'baseline':b,'negatives':{}}
for name in('rehashed_source','moved_boundary','extra_wall_disguised','moved_module_wall','source_host','frame','private_role','interface'):
 a,z=copy.deepcopy(l),copy.deepcopy(w)
 if name=='rehashed_source':
  for m in (a,z):
   s=m['module_placements'][0];s['module']['sleep_profile']['tamper']=True;s['module_hash']=digest(s['module'])
 if name in('moved_boundary','moved_module_wall','source_host'):
  k='A.private_l3.right_exposed'if name=='moved_boundary'else'A.bed1.back';fld='source_wall_hosts'if name=='source_host'else'walls';r=a[fld][k];r[0]=str(F(r[0])+F('.1'));z[fld][k]=list(map(str,rectangle(r,c['world_from_local'])))
 if name=='extra_wall_disguised':
  a['walls']['A.bed1.unknown']=['1','1','1.1','2'];z['walls']['A.bed1.unknown']=['1','1','2','1.1']
 if name=='frame':z['module_placements'][0]['transform']['translation'][0]='0'
 if name=='private_role':a['logical_regions']['A.private_access']['kind']='PUBLIC'
 if name=='interface':a['private_domains'][0]['public_interface']['rect'][0]='0'
 z['frame_binding125']['local_model_hash']=digest(a)
 r=examine(z,a,c);assert r['errors']or r['pending'],name
 out['negatives'][name]={'errors':r['errors'],'pending':r['pending']}
out['local_hash']=digest(l);out['world_hash']=digest(w)
(P/'audit_l3_whole_independent'/'binding131_tests.json').write_text(json.dumps(out,indent=2));print('baseline PASS limited; 8 negative mutations rejected')
