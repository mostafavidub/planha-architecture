"""Independent physical-space ledger audit. No residual becomes useful by label."""
from fractions import Fraction as F
from space_accounting118 import rect,merge,overlap,subtract,ledger
from checker114 import digest

def partition_ledger(model):
 errors=[];pending=[];a=model.get('spatial_accounting');rows=[]
 try:
  if not a:return {'status':'NOT_EVALUATED','witness':{'reason':'PHYSICAL_LEDGER_MISSING'},'scope':'Exact physical partition and separate declared functional footprints'}
  W,L=map(lambda x:F(str(x)),model['inputs'][:2]);groups=a['plot_partition'];regions={}
  for g in groups:
   role=g['role']
   if role in regions:raise ValueError('DUPLICATE_LEDGER_ROLE')
   regions[role]=[rect(r)for r in g['regions']]
   actual=sum((r[2]-r[0])*(r[3]-r[1])for r in regions[role])
   if actual!=F(g['area_m2']):errors.append('AREA_NUMBER_MISMATCH:'+role)
   if role=='UNASSIGNED_PLOT_FLOOR'and actual:pending.append('UNASSIGNED_FLOOR_OWNER_AND_THRESHOLD_POLICY')
   for x,y,X,Y in regions[role]:
    if not(0<=x<X<=W and 0<=y<Y<=L):errors.append('LEDGER_REGION_OUTSIDE_PLOT:'+role)
   rows.append({'role':role,'area_m2':str(actual),'regions':len(regions[role])})
  ys=sorted({F(0),L}|{v for qs in regions.values()for r in qs for v in(r[1],r[3])})
  for y,Y in zip(ys,ys[1:]):
   mid=(y+Y)/2;occupied=[]
   for role,qs in regions.items():
    raw=[(x,X)for x,a,X,b in qs if a<mid<b];ints=merge(raw)
    if sum(b-a for a,b in raw)!=sum(b-a for a,b in ints):errors.append('INTRA_ROLE_OVERLAP:'+role)
    if overlap(occupied,ints):errors.append('INTER_ROLE_OVERLAP:'+role)
    occupied=merge(occupied+ints)
   if y>=0 and Y<=L and occupied!=[(F(0),W)]:errors.append('PLOT_PARTITION_GAP')
  if sum(F(r['area_m2'])for r in rows)!=W*L:errors.append('PLOT_AREA_CONSERVATION')
  independent=ledger(model)
  if independent['status']!='PASS_LIMITED':errors.append('UNIT_LEDGER_RECOMPUTATION_FAILED')
  elif independent['witness']['units']!=a['unit_ledger']['witness']['units']:errors.append('UNIT_FOOTPRINT_LEDGER_NOT_ACTUAL_GEOMETRY')
  for u in model['units']:
   role=u.get('spatial_role_bindings',{}).get('open_public_envelope',{})
   if role.get('counts_as_verified_useful_living')is not False or role.get('regions')!=u['rooms'].get('living'):errors.append('RESIDUAL_OPEN_ENVELOPE_MISCLAIMED')
 except (KeyError,TypeError,ValueError,ZeroDivisionError)as ex:errors.append('LEDGER_SCHEMA:'+str(ex))
 return {'status':'FAIL'if errors else'NOT_EVALUATED'if pending else'PASS_LIMITED','witness':{'model_hash':digest(model),'groups':rows,'errors':errors,'pending':pending,'declared_footprints_are_not_capacity_proof':True},'scope':'Exact disjoint physical plot partition, recomputed declared unit footprint ledger and explicit non-usefulness of residual open floor. Contractual gross wall/threshold ownership must be separately explicit; no useful-area, floor necessity or architectural quality inferred.'}
