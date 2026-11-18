"""Actual left/right ownership in a local front/rear solver frame.
This is an isometry binding contract, not a whole-model transformation receipt.
"""
from fractions import Fraction as F
from common_core125 import build
from contract114 import S,digest

def local_core(W,L):
 m=build(W,L);W,L=F(str(W)),F(str(L));t=F('.15');e=F('.25')
 def rect(r):x,y,X,Y=map(F,r);return list(map(S,(y,x,Y,X)))
 x=F(m['units']['A'][0][2]);X=F(m['units']['B'][0][0])
 openings={o['id']:o for o in m['openings']}
 entries={}
 for uid in ('A','B'):
  a,b,c,d=map(F,openings[uid+'.entry']['rect']);entries[uid]=list(map(S,((b+d)/2,(a+c)/2)))
 core={'kind':'LOCAL_FRAME_OF_LEFT_RIGHT_COMMON_CORE125','band':list(map(S,(e,x+t,L-e,X-t))),
       'stair':rect(m['stair']),'lift':rect(m['lift']),'lobby':[rect(q)for q in m['common_floor']],
       'units':{u:rect(m['units'][u][0])for u in ('A','B')},
       'unit_ownership':{u:[rect(q)for q in m['units'][u]]for u in ('A','B')},
       'entry_centers':entries,'core_extent_x':list(map(S,(e,L-e))),
       'physical_core_model':m,'physical_core_hash':digest(m),
       'solver_inputs':list(map(S,(L,W)))+[2],
       'world_from_local':{'matrix':[[0,1],[1,0]],'translation':['0','0']},
       'assumptions':['Source physical core125 is actually different from core118, not a mirrored plan claimed as architectural diversity.',
        'Local units retain full physical ownership. Source operations/fixtures need exact whole-frame transformation and fresh independent checks before world admission.',
        'No light/ventilation evaluation. Common-only proof does not establish unit program viability.']}
 return core
