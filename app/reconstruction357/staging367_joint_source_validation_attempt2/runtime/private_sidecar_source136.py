"""Fixed actual-source sidecar primitive. Fit is not whole-plan admission."""
from fractions import Fraction as F
from contract114 import S

def build(core,variant=3):
 x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);ox=ex-F('8.35');oy=y0
 if ox<x0 or ox+F('16.7')>x1 or y1-y0<F('7.1'):return None
 local={'bed1':['12.8','.15','16.4','5.6'],'bed2':['.15','.15','5.6','4.65'],'bed3':['6.9','.15','12.35','4.65']}
 rects={k:list(map(S,[ox+F(a),oy+F(b),ox+F(c),oy+F(d)]))for k,(a,b,c,d)in local.items()}
 return {'kind':'SIDECAR_T136','origin':list(map(S,[ox,oy])),'rectangles':rects,'bed_door_sides':{'bed1':'top','bed2':'right','bed3':'left'},'private_interface_center_x':S(ex),'scope':'Sidecar private-source primitive; full plan requires independent admission'}
