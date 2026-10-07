# Referee w10, tameness#2 (Prop S): exact check of the per-edge weight bounds.
# w(E) = prod_i (v_i)_{e_i}/(n_i)_{e_i}.  Hypotheses: on met parts (e_i>0): e_i <= v_i <= n_i - s.
# Crude (claim):   w <= prod (1-s/n_i)^{e_i} <= exp(-s k/N)
# Refined (ref.):  w <= (1 - k/(sum_{met} v_i + |F| s))^s   <= (1-k/(m+p s))^s  when |v|<=m.
from fractions import Fraction as Fr
import random, math
def ff(a,e):
    r=1
    for j in range(e): r*=a-j
    return r
def w(n,v,e):
    r=Fr(1)
    for ni,vi,ei in zip(n,v,e):
        r*=Fr(ff(vi,ei),ff(ni,ei))
    return r
random.seed(1)
bad_crude=bad_ref=0; tests=0; tight=Fr(0)
for trial in range(200000):
    p=random.randint(1,4); s=random.randint(1,6)
    n=[random.randint(0,30) for _ in range(p)]
    e=[0]*p; v=[0]*p
    for i in range(p):
        if n[i]>s and random.random()<0.8:
            e[i]=random.randint(1,n[i]-s)
            v[i]=random.randint(e[i],n[i]-s)
        else:
            v[i]=random.randint(0,max(n[i]-s,0)) if n[i]>0 else 0
    k=sum(e)
    if k==0: continue
    tests+=1
    N=sum(n); W=w(n,v,e)
    crude=1.0
    for ni,ei in zip(n,e):
        if ei: crude*=(1-s/ni)**ei
    if float(W)>crude*(1+1e-12) or float(W)>math.exp(-s*k/N)*(1+1e-12): bad_crude+=1
    F=[i for i in range(p) if e[i]>0]
    D=sum(v[i] for i in F)+len(F)*s
    ref=(1-Fr(k,D))**s
    if W>ref: bad_ref+=1
    if ref>0 and W/ref>tight: tight=W/ref
print("tests",tests,"crude violations",bad_crude,"refined violations",bad_ref,"max W/refined",float(tight))
# tightness: single part n=m+s, v=m, E inside: W = C(m,k)/C(m+s,k) vs refined (1-k/(m+s))^s
for (m,k,s) in [(30,20,3),(60,50,5),(110,100,2)]:
    Wt=w([m+s],[m],[k]); print("single part",m,k,s,float(Wt),float((1-Fr(k,m+s))**s), math.exp(-s*k/(m+s)))
