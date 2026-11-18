from fractions import Fraction as F
from contract114 import S

def build(core,variant=3):
 x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);ox=ex-F('6.25');oy=y0
 if ox<x0 or ox+F('12.5')>x1 or y1-y0<F('12.45'):return None
 local={'bed1':['5.55','.15','9.15','5.6'],'bed2':['.15','6.9','5.6','11.4'],'bed3':['6.9','6.9','12.35','11.4']}
 rects={k:list(map(S,[ox+F(a),oy+F(b),ox+F(c),oy+F(d)]))for k,(a,b,c,d)in local.items()}
 return {'kind':'TURN_T133','origin':list(map(S,[ox,oy])),'rectangles':rects,'bed_door_sides':{'bed1':'top','bed2':'right','bed3':'left'},'private_interface_center_x':S(ex),'scope':'T-private-source primitive; full plan requires independent admission'}
