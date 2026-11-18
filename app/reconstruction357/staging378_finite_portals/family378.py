"""Finite interior portal family, selected before any independent review."""
import copy,hashlib,json,sys
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
for folder in ('staging362_core_notch','staging359_hall_clamp','planha_general150_runtime_work','staging365_balanced_portals'):
 sys.path.insert(0,str(ROOT/folder))
from selector365 import select
P=ROOT/'staging362_core_notch/actual362.json'
PIN='d448292d87b2fbd351f150bbfba3c7b6bf8acb4c074d31d4192f6ccc64f229d8'
POLICY='WIDEST_OPERATION_COMPONENT_INTERIOR_QUARTILES_MAX_SLACK_THEN_PARAMETER_SPREAD_V1'
def load_parent():
 data=P.read_bytes()
 if hashlib.sha256(data).hexdigest()!=PIN:raise ValueError('PARENT_SOURCE_CHANGED')
 return json.loads(data)
def validate_request(raw):
 if type(raw)is not dict or set(raw)!={'W','L','n','requested_count'}:raise ValueError('REQUEST_FIELDS')
 if any(type(raw[k])not in(str,int)for k in('W','L')) or type(raw['n'])is not int or type(raw['requested_count'])is not int:raise ValueError('REQUEST_TYPES')
 if (F(raw['W']),F(raw['L']),raw['n'],raw['requested_count'])!=(F(26),F(28),2,2):raise ValueError('FIXED_SOURCE_FAMILY_SCOPE')
 return raw

def enumerate_family(parent):
 validate_request(parent['candidate']['request'])
 base=select(parent);lo,hi=map(F,base['selected_interval'])
 if lo>=hi:raise ValueError('EMPTY_COMPONENT')
 xs=[lo+(hi-lo)*q for q in (F(1,4),F(1,2),F(3,4))]
 mid=(lo+hi)/2
 # First maximizes minimum coordinate slack; subsequent ranks maximize distance
 # from the first, tie-breaking by ascending coordinate. Not a quality objective.
 xs=sorted(xs,key=lambda x:(-min(x-lo,hi-x),x))
 xs=[xs[0]]+sorted(xs[1:],key=lambda x:(-abs(x-xs[0]),x))
 out=[];oldx=F(base['entry_x']['A'])
 for rank,x in enumerate(xs):
  p=copy.deepcopy(base);delta=x-oldx;p['entry_x']['A']=str(x)
  p['portal_y']['stair']=str(F(base['portal_y']['stair'])-delta/2)
  p['portal_y']['lift']=str(F(base['portal_y']['lift'])+delta/2)
  p.update(finite_rank378=rank,finite_policy378=POLICY,finite_parameter378=str(x),selection='FINITE_INTERIOR_QUARTILE_SOURCE_SELECTION',constraints_complete=False,
    unevaluated_constraints378=['CURRENT_FULL_ROUTE_REVIEW','CURRENT_FULL_FUNCTIONAL_REVIEW','SEMANTIC_QUALITY','OPTION_SET_DISTINCTNESS'],candidate_policy='SOURCE_PROPOSAL_NOT_ADMISSION',accepted=False)
  out.append(p)
 return out

def actual_selection(parent):
 # Preregistered first non-midpoint rank. Never changed after review results.
 return enumerate_family(parent)[1]
