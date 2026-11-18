"""Post-assembly local packet proposal, not a runtime admission hook."""
from fractions import Fraction as F
from contract114 import S
from shared_binding137 import reconstruct,obstacles,IDS,SCENARIO,check
from shared_geometry137 import local_polyline_clear
from contract114 import BODY

def propose(model,uid,proposal):
 u,uses,g=reconstruct(model,uid,proposal)
 a,b,c,d=map(F,proposal['shared_body_witness'])
 if uid=='B':L=F(model['inputs'][1]);b,d=L-d,L-b
 center=((a+c)/2,(b+d)/2);paths={}
 for ident in IDS:
  target=tuple(map(F,u['route_targets'][ident+'_front']));x,y=center;tx,ty=target
  for path in ([center,(tx,y),target],[center,(x,ty),target]):
   if local_polyline_clear(path,BODY,g,obstacles(model,u,ident+'_front')):
    paths[ident]=[list(map(S,p))for p in path];break
  if ident not in paths:return {'status':'NO_TWO_L_LOCAL_PROPOSAL','target':ident,'not_global_infeasibility':True}
 packet={'scenario':SCENARIO,'witness':list(map(S,(a,b,c,d))),'paths':paths}
 return {'packet':packet,'audit':check(model,uid,proposal,packet)}
