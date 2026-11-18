"""Deterministic left/right ownership with vertical shared core. Study only."""
from fractions import Fraction as F
import json,hashlib
from pathlib import Path

def build(W,L):
 W,L=F(str(W)),F(str(L));e=F('.25');t=F('.15');body=F('.7');sw,sh=F('4.55'),F('2.45');lw,lh=F('1.65'),F('1.65');entryw=F('1.3')
 cw=sw+2*t;x=(W-cw)/2;X=x+cw;s0=e+t;s1=s0+sh;l1=L-e-t;l0=l1-lh;low=s1+t;high=l0-t
 if high-low<max(entryw,body)or x-e<body:raise ValueError('OUTSIDE_CURRENT_COMMON_INTERFACE_METHOD_NOT_GLOBAL_INFEASIBILITY')
 cy=(low+high)/2;cx=W/2;stair=[x+t,s0,X-t,s1];lift=[cx-lw/2,l0,cx+lw/2,l1]
 hosts={'outer.left':[0,0,e,L],'outer.right':[W-e,0,W,L],'outer.front':[e,0,W-e,e],'outer.back':[e,L-e,W-e,L],'common.left':[x,e,x+t,L-e],'common.right':[X-t,e,X,L-e],'stair.front':[x+t,e,X-t,s0],'stair.back':[x+t,s1,X-t,low],'lift.left':[lift[0]-t,l0-t,lift[0],L-e],'lift.right':[lift[2],l0-t,lift[2]+t,L-e],'lift.front':[lift[0],l0-t,lift[2],l0],'lift.back':[lift[0],l1,lift[2],L-e]}
 openings=[{'id':'A.entry','host':'common.left','rect':[x,cy-entryw/2,x+t,cy+entryw/2],'connects':['A','lobby'],'kind':'UNIT_ENTRY_APERTURE_HARDWARE_NOT_EVALUATED'}, {'id':'B.entry','host':'common.right','rect':[X-t,cy-entryw/2,X,cy+entryw/2],'connects':['B','lobby'],'kind':'UNIT_ENTRY_APERTURE_HARDWARE_NOT_EVALUATED'}, {'id':'stair.entry','host':'stair.back','rect':[cx-F('.45'),s1,cx+F('.45'),low],'connects':['stair','lobby'],'kind':'CORE_INTERFACE_NO_HARDWARE_CLAIM'}, {'id':'lift.entry','host':'lift.front','rect':[cx-F('.45'),l0-t,cx+F('.45'),l0],'connects':['lift','lobby'],'kind':'CORE_INTERFACE_NO_HARDWARE_CLAIM'}]
 def subtract(a,b):
  x,y,X,Y=a;v,w,V,W=b;v=max(x,v);w=max(y,w);V=min(X,V);W=min(Y,W)
  if v>=V or w>=W:return[a]
  return[r for r in[(x,y,v,Y),(V,y,X,Y),(v,y,V,w),(v,W,V,Y)]if r[0]<r[2]and r[1]<r[3]]
 walls={}
 for k,r in hosts.items():
  parts=[r]
  for o in openings:
   if o['host']==k:parts=[z for p in parts for z in subtract(p,o['rect'])]
  for i,z in enumerate(parts):walls[k+'.'+str(i)]=z
 remaining=[[x,e,X,L-e]]
 for cut in list(walls.values())+[stair,lift]+[o['rect']for o in openings]:remaining=[z for r in remaining for z in subtract(r,cut)]
 units={'A':[[e,e,x,L-e]],'B':[[X,e,W-e,L-e]]};routes={}
 for src,sy in [('stair',s1-body/2),('lift',l0+body/2)]:
  for uid,tx in [('A',x-body/2),('B',X+body/2)]:routes[src+'_'+uid]=[[cx,sy],[cx,cy],[tx,cy]]
 src=Path(__file__).resolve().parent/'references/core125_contract_source.py'
 m={'schema':'LEFT_RIGHT_COMMON_OWNERSHIP125_STUDY','inputs':[str(W),str(L),2],'body_m':str(body),'units':units,'stair':stair,'lift':lift,'common_floor':remaining,'walls':walls,'wall_hosts':hosts,'openings':openings,'routes':routes,'reference_contract_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_dimensions':{'stair':[str(sw),str(sh)],'lift':[str(lw),str(lh)],'walls':{'outer':str(e),'internal':str(t)}},'method_domain':{'minimum_L':str(2*e+sh+lh+4*t+entryw),'minimum_W':str(2*e+cw+2*body),'meaning':'Necessary method bounds for common .7 interfaces only, NOT unit viability or universal bounds'},'accepted':False,'release_allowed':False,'scope':['No unit room/fixture/operation/privacy/capacity layout evaluated.','Routes start at modeled stair/lift interiors on this storey; street/vertical travel unverified.','Common remaining floor explicitly common/unprogrammed, not useful room or imposed open yard.','Apertures are physical geometry, no door hardware/panel-operation acceptance.','No lighting/ventilation evaluation.']}
 return json.loads(json.dumps(m,default=str))
if __name__=='__main__':Path(__file__).with_name('case39x7.07.json').write_text(json.dumps(build('39','7.07'),indent=2))
