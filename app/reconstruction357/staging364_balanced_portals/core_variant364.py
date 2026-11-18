"""Deterministic finite boundary solution; balanced candidate, not Pareto repair."""
from fractions import Fraction as F
import importlib.util
from pathlib import Path
from contract114 import S,digest
PARENT=Path(__file__).resolve().parents[1]/'staging362_core_notch'
def core(W,L):
 spec=importlib.util.spec_from_file_location('_basecore362',PARENT/'core_variant362.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);c=base.core(W,L);before=digest(c)
 y,Y=map(F,(c['band'][1],c['band'][3]));mid=(y+Y)/2;lift=list(map(F,c['lift']));stair=list(map(F,c['stair']));pl=lift[1]+F('1.1')/2;d=2*(pl-mid);ps=mid-d/2
 # Finite objective: select the lowest source-compatible lift portal, then solve
 # both equal-length equations. Not an epsilon-tuned path or owner threshold.
 if not(d>0 and stair[1]+F('.9')/2<=ps<=stair[3]-F('.9')/2 and pl<=lift[3]-F('1.1')/2):raise ValueError('FINITE_BOUNDARY_SOLUTION_UNSUPPORTED')
 xb=F(c['entry_centers']['B'][0]);xa=xb+d;c['entry_centers']['A'][0]=S(xa)
 lobby=list(map(F,c['lobby'][0]))
 if any(not(lobby[0]+F('.7')<=x<=lobby[2]-F('.7'))for x in(xa,xb)):raise ValueError('LOBBY_ACTOR_DOMAIN')
 if xa+F('.65')>F(c['notch362']['A_horizontal_boundary_end']):raise ValueError('A_APERTURE_HOST')
 if xa-F('1.95')<F(c['core_extent_x'][0]):raise ValueError('A_REVERSE_RAIL_HOST')
 c['balanced_portals364']={'source_base_core_digest':before,'portal_y':{'stair':S(ps),'lift':S(pl)},'slide_direction':{'A':-1,'B':1},'parameter_selection':'FINITE_LOWEST_LIFT_PORTAL_BOUNDARY_THEN_EXACT_TWO_BALANCE_EQUATIONS','source_body_pose':'SOURCE_INSIDE_INSET_0.4_AT_ACTUAL_NEW_PORTAL_CENTER','metric_policy':'INDEPENDENT_CANDIDATE_EXPLICIT_TRADEOFF_NOT_PARETO_REPAIR','predictions_not_review':True,'accepted':False}
 return c
