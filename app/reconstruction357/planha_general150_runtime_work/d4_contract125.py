"""Exact signed permutation matrices for rigid axis-aligned 2D frames."""
from fractions import Fraction as F

def matrix(value):
 if not isinstance(value,(list,tuple))or len(value)!=2 or any(not isinstance(r,(list,tuple))or len(r)!=2 for r in value):raise ValueError('NONRIGID_D4_MATRIX')
 try:m=tuple(tuple(F(str(x))for x in r)for r in value)
 except (ValueError,TypeError,ZeroDivisionError):raise ValueError('NONRIGID_D4_MATRIX')
 if any(v not in(-1,0,1)for row in m for v in row)or any(sum(v!=0 for v in row)!=1 for row in m)or any(sum(m[i][j]!=0 for i in range(2))!=1 for j in range(2))or abs(m[0][0]*m[1][1]-m[0][1]*m[1][0])!=1:raise ValueError('NONRIGID_D4_MATRIX')
 return m

def inverse(value):
 m=matrix(value);return [[m[j][i]for j in range(2)]for i in range(2)]

def compose(a,b):
 a,b=matrix(a),matrix(b);return [[sum(a[i][k]*b[k][j]for k in range(2))for j in range(2)]for i in range(2)]
