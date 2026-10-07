import sys; sys.path.insert(0,'heavy')
from heavylib import *
from fractions import Fraction as F
X=F(513,8); x=[X,X,X]
T=[(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
T=[tuple(F(v) for v in t) for t in T]
r=80
print('tau*', tau_star(x,T)/r)
for j in range(len(T)):
    R=T[:j]+T[j+1:]
    print(j, T[j], 'tau*(C-t)=', float(tau_star(x,R)/r))
# super-heavy classes
for i in range(3):
    S=[j for j,t in enumerate(T) if 3*t[i]>2*X]
    print('S',i,S, 'sigma', min(T[j][i] for j in S), 'e', float((X-min(T[j][i] for j in S))/r))
# Fano assignments using subsets
fs=all_fano(x,T,0)
print('num fano reps', len(fs))
from collections import Counter
c=Counter(tuple(sorted(set(a))) for a in fs)
for k,v in sorted(c.items(), key=lambda kv: len(kv[0]))[:40]: print(k,v)
