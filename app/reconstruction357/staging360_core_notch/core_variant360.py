"""Exact one-branch source variant: existing lift-tail floor to adjacent unit A.
Does not declare the tail unnecessary or the reassigned floor functionally useful.
"""
import copy
from fractions import Fraction as F
from contract114 import core_first,WALL,S,digest

def derive(compact):
 c=copy.deepcopy(compact);T=WALL
 if c['kind']!='COMPACT_CONNECTED_CENTRAL_CORE118'or len(c['lobby'])!=2:raise ValueError('SOURCE_COMPACT_TWO_LOBBY_REGIONS_ONLY')
 main,tail=[tuple(map(F,r))for r in c['lobby']];lift=tuple(map(F,c['lift']));y=F(c['band'][1]);lx,ly,rx,ry=tail
 if not(lx==main[2]==lift[0]-T and ly==main[1]==y and rx==lift[2]and ry==lift[1]-T):raise ValueError('SOURCE_LIFT_TAIL_PROFILE')
 if lx+T>=rx or ly-T>=ry:raise ValueError('NO_POSITIVE_TRANSFER')
 # Preserve the complete existing entry sliding rail, whose host ends at lx.
 entryx=F(c['entry_centers']['A'][0]);railend=entryx+F('.65')+F('1.3')
 if railend>lx:raise ValueError('ENTRY_RAIL_HOST_WOULD_BE_TRUNCATED')
 transfer=[lx+T,ly-T,rx,ry];separator=[lx,ly-T,lx+T,ry]
 c['kind']='COMPACT_CORE_SOUTH_LIFT_NOTCH360';c['lobby']=[list(map(S,main))];c['unit_ownership']['A'].append(list(map(S,transfer)))
 c['notch360']={'branch':'FIXED_LITERAL_SOUTH_LIFT_TAIL','removed_lobby_tail':list(map(S,tail)),'new_A_floor_ownership':list(map(S,transfer)),'new_separator':list(map(S,separator)),'A_horizontal_boundary_end':S(lx),'source_compact_digest':digest(compact),'function_of_transferred_floor':'UNKNOWN_PENDING_INDEPENDENT_USE_PROOF','absence_of_required_maneuver':'NOT_PROVEN_BY_CURRENT_PATH_FOOTPRINT'}
 if c['stair']!=compact['stair']or c['lift']!=compact['lift']or c['entry_centers']!=compact['entry_centers']:raise ValueError('CORE_ASSETS_CHANGED')
 return c

def core(W,L):
 c=core_first(W,L)
 if c is None:raise ValueError('SOURCE_CORE_UNSUPPORTED')
 return derive(c)
