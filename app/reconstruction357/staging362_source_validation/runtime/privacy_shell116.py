"""Independent sufficient U-shell certificate, module-only; no cabinet opacity.
Reference: audit_lr_target_privacy/preliminary.py three-face exit argument.
Missing proof is NOT_EVALUATED, never global impossibility. Actual material
opacity and sight heights remain the same explicitly hypothetical plan scope.
"""
from fractions import Fraction as F
from privacy115 import rect,separator,interval_covered,contained

def shell_certificate(aperture,target,envelope,shell_ids,actual_walls):
 """Only source-bound actual wall IDs; caller must independently bind provenance.
The envelope is a mathematical crossing box, not an opaque obstacle. Every ray
crosses its interior; its two lateral and downstream faces must be solid.
"""
 s,t,g=map(rect,(aperture,target,envelope));walls={k:rect(v)for k,v in actual_walls.items()}
 if not shell_ids or len(set(shell_ids))!=len(shell_ids) or any(k not in walls for k in shell_ids):return None
 shells=[walls[k]for k in shell_ids]
 for axis in (0,1):
  for sign in (1,-1):
   ordered=(s[axis+2]<g[axis] and g[axis+2]<t[axis])if sign==1 else(t[axis+2]<g[axis]and g[axis+2]<s[axis])
   if not ordered:continue
   crossing=separator(s,t,g)
   if not crossing:continue
   faces=[]
   for ax,high in ((1-axis,False),(1-axis,True),(axis,sign==1)):
    p=g[ax+2]if high else g[ax];other=1-ax
    intervals=[(w[other],w[other+2])for w in shells if (w[ax]<p<=w[ax+2]if high else w[ax]<=p<w[ax+2])]
    if not interval_covered(g[other],g[other+2],intervals):break
    faces.append({'axis':ax,'plane':str(p),'interval':[str(g[other]),str(g[other+2])]})
   if len(faces)==3:return {'status':'PASS_SCOPED_THREE_FACE_CERTIFICATE','crossing':crossing,'exit_faces':faces,'actual_wall_ids':list(shell_ids),'accepted':False,'scope':'All aperture-to-target rays hit actual three exit faces; no furniture-envelope opacity; not operation or whole-model approval.'}
 return None
