# TEST_ONLY kitchen3.05 candidate. Necessary prefilter only; exact full gates mandatory.
"""Restricted three-room domain parameters derived from unchanged module bounds.
Furniture is never scaled. Every parameter instance still needs module/whole gates.
"""
from fractions import Fraction as F
from contract114 import S,GRID

def build(core,variant=2):
 x0,y0,x1,y1=map(F,core['units']['A']);ex=F(core['entry_centers']['A'][0]);wall=F('.15');gap=F('1.3')
 available=(x1-x0-2*wall-2*gap)/3
 width=min(F('5.8'),(available//GRID)*GRID);depth=F('4.5')
 if width<F('5.45')or depth<F('4.5'):return None
 span=3*width+2*gap;start=(x0+x1-span)/2
 if y1-y0<depth+F('1.3')+F('1.0')+F('3.05'):return None
 if not(start+F('.55')<=ex<=start+span-F('.55')):return None
 beds={f'bed{i+1}':list(map(S,[start+i*(width+gap),y0,start+i*(width+gap)+width,y0+depth]))for i in range(3)}
 return {'kind':'PARAMETRIC_THREE_SOURCE_ROOMS_REAL_PRIVATE_HALL129','rectangles':beds,'bed_door_sides':{'bed1':'right','bed2':'left','bed3':'left'},'private_hall_clear_depth':'1.0','private_interface_center_x':S(ex),'module_parameters':{'width':S(width),'depth':S(depth),'minimum_width':'5.45','minimum_twin_depth':'4.5','source':'bedroom_module116.py and twin_module118.py actual study bounds; not universal room minimum'},'scope':'Restricted real-front-wall-attached domain; no lighting criterion. One actual hall and three source-bound operational rooms, not entire envelope useful floor.','raw_inputs_not_rounded':True,'internal_position_grid_m':S(GRID)}
