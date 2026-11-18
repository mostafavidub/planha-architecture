"""Bounded actual-core alternative comparison for the independently saved18x24.
This is not a universal long-corridor threshold, a minimum-area proof or whole
layout quality approval. Future inputs need their own actual baseline evidence.
"""
from pathlib import Path
import json,hashlib
from fractions import Fraction as F
from core_wall_audit118 import core_concept,opening_hosts,q,hit,output,safe
from circulation_named_audit118 import area,measures
BASELINE=Path(__file__).parent/'evidence/independent118/baseline_fullspan18_model.json'
BASELINE_MODEL_HASH='da7592ddf5dba37647ea8e2a731f501a05f0d6b4bb3dfc3e10be9dc827fabff1'
def digest(m):return hashlib.sha256(json.dumps(m,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def reference():
 m=json.loads(BASELINE.read_text())['model']
 if digest(m)!=BASELINE_MODEL_HASH:raise ValueError('ACTUAL_BASELINE_MODEL_CHANGED')
 return m

def applicability(m):
 # Conservative: this explicit bounded comparison is evaluated rather than
 # calling a rectangle "short" using an invented length/aspect threshold.
 return {'status':'PASS_LIMITED','witness':{'applies':True,'reason':'Assess actual common-core alternative and route-cost evidence; no arbitrary numeric long/short classification.'},'scope':'Applicability to source Q04 common-circulation comparison, not a claim all circulation is a long corridor.'}
@safe
def compare(m):
 old=reference();errors=[];pending=[]
 if old['inputs']!=m['inputs']:return output('Q04',[],['ACTUAL_SAME_INPUT_CORE_ALTERNATIVE_MISSING'],{'available_baseline_inputs':old['inputs'],'current_inputs':m['inputs']})
 def inventory(x):
  return {'program':x['program'],'furniture':{u['id']:sorted((v['kind'],tuple(v.get('source_size_m',[])))for v in u['fixture_metadata'].values())for u in x['units']}}
 if inventory(old)!=inventory(m):pending.append('ACTUAL_ALTERNATIVE_PROGRAM_OR_FURNITURE_INVENTORY_DIFFERS')
 def metrics(x):
  sizes={k:[str(q(x['common_spaces'][k])[2]-q(x['common_spaces'][k])[0]),str(q(x['common_spaces'][k])[3]-q(x['common_spaces'][k])[1])]for k in('stair','lift')}
  return {'core_clear_sizes':sizes,'lobby_union_area_m2':str(area([q(r)for r in x['common_spaces']['lobby']])),'routes':{k:measures(p)for k,p in x['common_routes'].items()}}
 before,after=metrics(old),metrics(m)
 if before['core_clear_sizes']!=after['core_clear_sizes']:errors.append('CORE_SIZE_CHANGED_IN_COMPARISON')
 checks={name:{'core':core_concept(x),'hosts':opening_hosts(x)}for name,x in [('before',old),('after',m)]}
 if any(r['status']!='PASS_LIMITED'for v in checks.values()for r in v.values()):pending.append('ACTUAL_BASE_FUNCTIONAL_CORE_OR_HOST_CHECK_NOT_PASSED')
 a=F(before['lobby_union_area_m2']);b=F(after['lobby_union_area_m2']);route_deltas={k:str(F(after['routes'][k]['length_m'])-F(v['length_m']))for k,v in before['routes'].items()}
 if b>=a or any(F(v)>0 for v in route_deltas.values())or not any(F(v)<0 for v in route_deltas.values()):pending.append('DECLARED_COMPACT_SELECTION_REASON_NOT_SUPPORTED_BY_MEASUREMENTS')
 # Every actual common route still joins a required core/entry; no route ends
 # at an invented target to justify an otherwise purposeless corridor branch.
 if set(m['common_routes'])!={k+'_'+u['id']for k in('stair','lift')for u in m['units']}:errors.append('NONPROGRAM_COMMON_ROUTE_TARGET')
 # Paired private approaches have a distinct source rule and are NOT excused
 # by this common-core comparison. Separate named gate is still mandatory.
 return output('Q04',errors,pending,{'before_model_hash':digest(old),'after_model_hash':digest(m),'before':before,'after':after,'route_length_changes_m':route_deltas,'lobby_area_change_m2':str(b-a),'base_functional_checks':checks,'selection_reason':'Retain this physically checked compact alternative because the same clear core sizes and same furniture program have smaller shared floor and no longer required common route versus the saved full-span alternative.','limitations':['Different unit furniture positions: no controlled proof of whole-plan superiority.','No global minimum lobby width or area claimed; open-panel X projection is not automatically required lobby-floor width.','No blanket necessity/quality approval for private paths or future input sizes.','Current geometry is compared as nominal Concept only, not stairs/lift installation approval.']})
