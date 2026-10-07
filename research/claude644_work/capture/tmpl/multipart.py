# Two fixed types over ANY number of parts: template-failure witness-part search (note Thm 7.71 by templates)
import sys, itertools
from scipy.optimize import linprog
from fractions import Fraction as F
from lib2 import FUNCS
Qv=0.75
STATES=['A','B','AB','BA']   # A: a>0,b=0 ; B: a=0,b>0 ; AB: a>=b>0 ; BA: b>=a>0
# template spec: list of (u,v) facets: u*a_i+v*b_i <= x_i
def T(k): return [(float(u),float(v)) for u,v in FUNCS[k-1]]
TEMPL={'Ha':[(1.75,0.0)],'Hb':[(0.0,1.75)],'Qb':T(9),'Qa':T(10),'V':T(39),"V'":T(40),
       'F61':T(1),'F16':T(2),'K4':T(21),"K4'":T(22),'D':T(41),"D'":T(42),'U':T(11),"U'":T(12)}
# check naming: fn9 = max(3t/2, s+3t/4): t=b on line => 'Qb'; fn10 = max(3s/4+t,3s/2): s=a on line => 'Qa'
def build(states, fails):
    # vars per part i: x,a,b (3 each) + eps ; returns LP maximizing eps
    p=len(states); nv=3*p+1; E=nv-1
    A=[];b=[]
    def add(coef,const):  # coef.z + const >= 0  -> -coef.z <= const
        A.append([-c for c in coef]); b.append(const)
    def z(): return [0.0]*nv
    for i,s in enumerate(states):
        X,Aa,Bb=3*i,3*i+1,3*i+2
        c=z(); c[Aa]=1; add(c,0); c=z(); c[Bb]=1; add(c,0)
        c=z(); c[X]=1; c[Aa]=-1; add(c,0); c=z(); c[X]=1; c[Bb]=-1; add(c,0)
        if s in ('A','AB','BA'): c=z(); c[Aa]=1; c[E]=-1; add(c,0)
        if s in ('B','AB','BA'): c=z(); c[Bb]=1; c[E]=-1; add(c,0)
        if s=='A': c=z(); c[Bb]=-1; add(c,0)
        if s=='B': c=z(); c[Aa]=-1; add(c,0)
        if s=='AB': c=z(); c[Aa]=1; c[Bb]=-1; add(c,0); c=z(); c[X]=1; c[Bb]=-1; add(c,-Qv)
        if s=='BA': c=z(); c[Bb]=1; c[Aa]=-1; add(c,0); c=z(); c[X]=1; c[Aa]=-1; add(c,-Qv)
    for i,si in enumerate(states):
        for j,sj in enumerate(states):
            if i!=j and si!='B' and sj!='A':
                c=z(); c[3*i]=1; c[3*i+1]=-1; c[3*j]=1; c[3*j+2]=-1; add(c,-Qv)
    c=z()
    for i in range(p): c[3*i+1]=-1
    add(c,1)
    c=z()
    for i in range(p): c[3*i+2]=-1
    add(c,1)
    for (i,u,v) in fails:  # u a_i + v b_i - x_i >= eps
        c=z(); c[3*i+1]=u; c[3*i+2]=v; c[3*i]=-1; c[E]=-1; add(c,0)
    cobj=[0.0]*nv; cobj[E]=-1
    bounds=[(None,None)]*(nv-1)+[(None,1.0)]
    r=linprog(cobj,A_ub=A,b_ub=b,bounds=bounds,method='highs')
    if r.status==2: return False
    if r.status!=0: return True
    return -r.fun>1e-9
leaves=0; nodes=0
def search(states, fails, order, depth=0, log=False):
    global leaves,nodes
    nodes+=1
    if not build(states,fails): leaves+=1; return True
    if depth>=len(order): 
        print('OPEN', states, fails); return False
    name=order[depth]; ok=True
    for i in range(len(states)+1):
        for s in (STATES if i==len(states) else [None]):
            st=states+[s] if s else states
            for (u,v) in TEMPL[name]:
                ok&=search(st, fails+[(i,u,v)], order, depth+1)
                if not ok: return False
    return ok
order=sys.argv[1].split(',')
ok=search([],[],order)
print('order',order,'OK' if ok else 'FAIL','leaves',leaves,'nodes',nodes)
