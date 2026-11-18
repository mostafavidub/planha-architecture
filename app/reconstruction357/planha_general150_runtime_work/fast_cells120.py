"""Exact rational rectangle set difference using integer lifting, never rounding.
Same grid, inclusion rule, merge order and output serialization as geometry114.cells.
This is a computational change only: no geometry, precision or acceptance changes.
"""
from fractions import Fraction as F
from math import lcm
from contract114 import S

def cells(gross,subtract):
 g=[tuple(F(str(x))for x in r)for r in gross]
 s=[tuple(F(str(x))for x in r)for r in subtract]
 if not g:return []
 den=lcm(*(x.denominator for r in g+s for x in r))
 g=[tuple(int(x*den)for x in r)for r in g]
 s=[tuple(int(x*den)for x in r)for r in s]
 xs=sorted({r[i]for r in g+s for i in(0,2)});ys=sorted({r[i]for r in g+s for i in(1,3)})
 # Doubled midpoint coordinates preserve inclusive boundary semantics exactly.
 gg=[tuple(2*x for x in r)for r in g];ss=[tuple(2*x for x in r)for r in s]
 out=[]
 for a,b in zip(xs,xs[1:]):
  x=a+b
  # Scan only rectangles whose X span contains this actual cell midpoint.
  gx=[r for r in gg if r[0]<=x<=r[2]]
  if not gx:continue
  sx=[r for r in ss if r[0]<=x<=r[2]]
  for c,d in zip(ys,ys[1:]):
   y=c+d
   if any(r[1]<=y<=r[3]for r in gx)and not any(r[1]<=y<=r[3]for r in sx):out.append((a,c,b,d))
 rows={}
 for a,c,b,d in out:rows.setdefault((c,d),[]).append((a,b))
 horizontal=[]
 for (c,d),ivs in rows.items():
  merged=[]
  for a,b in sorted(ivs):
   if merged and merged[-1][1]==a:merged[-1]=(merged[-1][0],b)
   else:merged.append((a,b))
  horizontal.extend((a,c,b,d)for a,b in merged)
 cols={}
 for a,c,b,d in horizontal:cols.setdefault((a,b),[]).append((c,d))
 result=[]
 for (a,b),ivs in cols.items():
  merged=[]
  for c,d in sorted(ivs):
   if merged and merged[-1][1]==c:merged[-1]=(merged[-1][0],d)
   else:merged.append((c,d))
  result.extend([S(F(a,den)),S(F(c,den)),S(F(b,den)),S(F(d,den))]for c,d in merged)
 return result
