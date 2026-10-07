"""Referee w9 (typeclosed#1): condition L's pair clause a_i+b_i<=x_i cannot be dropped from GGP (exact example,
the heavyparts agent's pair).  Parts (j,k,0), x=(6/5,6/5,19/60), b=(41/50,0,9/50) j-heavy, a=(0,41/50,9/50) k-heavy."""
from fractions import Fraction as F
from w9_ref_typeclosed1_e2e import mass_Qb, mass_Qa, mass_V
x=[F(6,5),F(6,5),F(19,60)]; b=[F(41,50),F(0),F(9,50)]; a=[F(0),F(41,50),F(9,50)]
j,k=0,1
assert 4*x[k]<7*a[k] and 4*x[j]<7*b[j] and (x[j]-b[j])+(x[k]-a[k])>F(3,4)
assert 7*a[2]<=4*x[2] and 7*b[2]<=4*x[2] and 3*a[2]/2<=x[2] and a[2]+b[2]>x[2]
for n,f in (('Qb',mass_Qb),('Qa',mass_Qa),('V(a,b)',mass_V),('V(b,a)',lambda s,t: mass_V(t,s))):
    print(n,'fails in parts',[i for i in range(3) if f(a[i],b[i])>x[i]])
