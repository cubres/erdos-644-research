# one-sided two-box families, canonical pair (minO,minO): chain search per chamber. vars z=(xA,xB,xL,tA,tB)
import itertools, sys
from scipy.optimize import linprog
XA,XB,XL,TA,TB=range(5); NV=5
def L(d,c=0.0):
    v=[0.0]*NV
    for k,x in d.items(): v[k]+=x
    return (v,c)
def add(l1,l2,s=1.0):
    return ([a+s*b for a,b in zip(l1[0],l2[0])], l1[1]+s*l2[1])
def scale(l,s): return ([a*s for a in l[0]], l[1]*s)
CONST=lambda c: ([0.0]*NV,c)
def types(ca,cb):
    # returns a,b as lists of affine forms per part (A,B,L)
    if ca==0: a=[L({TA:1}), L({TA:-1},1.0), CONST(0.0)]           # 1-tA <= xB
    else:     a=[L({TA:1}), L({XB:1}), L({TA:-1,XB:-1},1.0)]      # 1-tA > xB
    if cb==0: b=[L({TB:-1},1.0), L({TB:1}), CONST(0.0)]
    else:     b=[L({XA:1}), L({TB:1}), L({TB:-1,XA:-1},1.0)]
    return a,b
def domain(ca,cb):
    W=[L({TA:1,XA:-4/7}), L({TB:1,XB:-4/7}),            # strict really
       L({XA:1,TA:-1}), L({TA:-1},1.0), L({XB:1,TB:-1}), L({TB:-1},1.0),
       L({TA:1,XB:1,XL:1},-1.0), L({TB:1,XA:1,XL:1},-1.0),
       L({TA:1,TB:1,XL:1},-1.0), L({XA:1,XB:1,TA:-1,TB:-1},-0.75), L({XA:1,XB:1,XL:1},-1.75), L({XL:1})]
    W.append(L({XB:1,TA:1},-1.0) if ca==0 else L({XB:-1,TA:-1},1.0))
    W.append(L({XA:1,TB:1},-1.0) if cb==0 else L({XA:-1,TB:-1},1.0))
    return W
TEMPL={'Ha':[(1.75,0)],'Hb':[(0,1.75)],'Qb':[(0,1.5),(1,0.75)],'Qa':[(1.5,0),(0.75,1)],
       'V':[(1,1),(1.25,0.5)],"V'":[(1,1),(0.5,1.25)],'K4':[(2/3,1),(4/3,0.5)],"K4'":[(1,2/3),(0.5,4/3)],
       'F61':[(0,1),(1.5,0.25)],'F16':[(1,0),(0.25,1.5)]}
def tfacets(name,a,b):
    out=[]
    X=[L({XA:1}),L({XB:1}),L({XL:1})]
    for i in range(3):
        for u,v in TEMPL[name]:
            # x_i - u a_i - v b_i >= 0
            f=add(add(X[i],a[i],-u),b[i],-v); out.append((f'{name}@{"ABL"[i]}:{u},{v}',f))
    return out
def maxeps(W,viol):
    A=[];bb=[]
    for g,k in W: A.append([-x for x in g]+[0.0]); bb.append(k)
    for g,k in viol: A.append(list(g)+[1.0]); bb.append(-k)
    r=linprog([0.0]*NV+[-1.0],A_ub=A,b_ub=bb,bounds=[(None,None)]*NV+[(None,1.0)],method='highs')
    if r.status==2: return None
    if r.status!=0: return 1.0
    return -r.fun
def canfail(W,viol,f):
    m=maxeps(W,viol+[f]); return m is not None and m>1e-9
def chain_valid(W,a,b,chain):
    viol=[]
    for name in chain[:-1]:
        fl=[f for _,f in tfacets(name,a,b) if canfail(W,viol,f)]
        if len(fl)!=1: return False
        viol=viol+fl
    m=maxeps(W,viol)
    if m is None or m<=1e-9: return True
    return not any(canfail(W,viol,f) for _,f in tfacets(chain[-1],a,b))
names=list(TEMPL)
for ca in (0,1):
    for cb in (0,1):
        W=domain(ca,cb); a,b=types(ca,cb)
        m=maxeps(W,[])
        if m is None: print(ca,cb,'empty'); continue
        sol=None
        for r in range(1,5):
            for ch in itertools.permutations(names,r):
                if chain_valid(W,a,b,list(ch)): sol=ch; break
            if sol: break
        print('chamber',ca,cb,'chain',sol,flush=True)
