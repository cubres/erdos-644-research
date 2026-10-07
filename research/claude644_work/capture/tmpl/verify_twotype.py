# Exact randomized check of the two-type two-part theorem with the explicit templates
# F61 (6a+1b Fano), F16, V (5a+2b, explicit 11-cell support), V' (mirror), Q (3a on a line + 4b quad), Q' (mirror).
import random, itertools
from fractions import Fraction as F
random.seed(1)
def tau(x,a,b):
    p=len(x); best=None
    for i in range(p):
        if a[i]<=0: continue
        for j in range(p):
            if b[j]<=0: continue
            c = x[i]-min(a[i],b[i]) if i==j else x[i]-a[i]+x[j]-b[j]
            best=c if best is None or c<best else best
    return best
# explicit per-part constructions: return list of (cell(frozenset of rows), mass) realizing loads >= given
FANO_LINES=[{0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}]
def fano_cells(): return [frozenset(set(range(7))-L) for L in FANO_LINES]
def lp_realize(cells, loads):
    # exact small LP via scipy then verify exactly after rationalization: use explicit formulas instead where possible
    from scipy.optimize import linprog
    A=[[-1.0 if j in c else 0.0 for c in cells] for j in range(7)]
    r=linprog([1.0]*len(cells),A_ub=A,b_ub=[-float(l) for l in loads],method='highs')
    return r.fun
def V_cells():
    # rows 0,1 = b ; rows 2,3,4,5 = W, 6 = z ; matchings mu1={34|25} for b0, mu2={24|35} for b1
    C=[frozenset({0,1})]+[frozenset(set(range(2,7))-{j}) for j in range(2,7)]
    C+=[frozenset({0,3,4,6}),frozenset({0,2,5,6}),frozenset({1,2,4,6}),frozenset({1,3,5,6})]
    return C
def V_masses(s,t):
    # explicit construction from the notes: returns dict cell->mass with total max(s+t,5s/4+t/2)
    C=V_cells(); m={c:F(0) for c in C}
    if t<=s/2:
        k=t; r=s-2*t
    else:
        k=s/2; r=F(0)
    # k * (2,1)-construction: W mass 1, four mixed 1/2
    m[frozenset({2,3,4,5})]+=k
    for c in C[6:]: m[c]+=k/2
    # r * (1,0): five 4-subsets 1/4
    for c in C[1:6]: m[c]+=r/4
    # remaining b load
    m[C[0]]+=max(F(0),t-k)
    return m
def check_V(s,t):
    m=V_masses(s,t); loads=[sum(v for c,v in m.items() if j in c) for j in range(7)]
    need=[t,t,s,s,s,s,s]
    assert all(l>=n for l,n in zip(loads,need)), (s,t,loads)
    tot=sum(m.values()); assert tot==max(s+t,5*s/4+t/2),(s,t,tot)
    return tot
def no_cover_pair(cells):
    return all(len(c|d)<7 for c in cells for d in cells)
assert no_cover_pair(V_cells()) and no_cover_pair(fano_cells())
def M61(s,t): return max(t,3*s/2+t/4)
def MV(s,t): return max(s+t,5*s/4+t/2)
def MQ(s,t): return max(3*s/2,3*s/4+t)   # s rows on a line (3), t rows on quadrilateral (4)
TEMPL={'F61':M61,'F16':lambda s,t:M61(t,s),'V':MV,"V'":lambda s,t:MV(t,s),'Q':MQ,"Q'":lambda s,t:MQ(t,s)}
def works(x,a,b):
    return [n for n,M in TEMPL.items() if all(M(a[i],b[i])<=x[i] for i in range(2))]
def rnd():
    d=random.choice([4,8,12,16,24,40,100])
    return F(random.randint(0,d),d)
cnt=0; hard=0
for it in range(200000):
    al,be=rnd(),rnd()
    if random.random()<0.1: al=F(0)
    if random.random()<0.1: be=F(1)
    if random.random()<0.05: be=al
    a=(al,1-al); b=(be,1-be)
    if a==b and random.random()<0.9: continue
    x=[max(al,be)+rnd()*F(3,2), max(1-al,1-be)+rnd()*F(3,2)]
    t=tau(x,a,b)
    if t< F(3,4):
        # push x up to reach boundary sometimes
        continue
    cnt+=1
    w=works(x,a,b)
    assert w, ('UNCOVERED',x,a,b,t)
    if w==['V'] or w==["V'"]: hard+=1
# also check V construction exactly on grid
for s in [F(i,12) for i in range(13)]:
    for t in [F(i,12) for i in range(13)]: check_V(s,t)
print('PASS', cnt, 'instances with tau*>=3/4 covered; V-only instances', hard)
# boundary sampling: y minimal given x
from collections import Counter
cnt2=0; C=Counter()
for it in range(200000):
    al,be=sorted([rnd(),rnd()])
    r=random.random()
    if r<0.1: al=F(0)
    elif r<0.2: be=F(1)
    a=(al,1-al); b=(be,1-be)
    x0=max(al,be)+rnd()*F(3,2)
    # find minimal y: tau is piecewise linear nondecreasing in y; exact bisection over candidate breakpoints
    lo=max(1-al,1-be); 
    def tt(y): return tau([x0,y],a,b)
    if tt(lo+10)<F(3,4): continue
    # candidates: y where some term equals 3/4
    cands=[lo]
    for yy in [F(7,4)-be, F(7,4)-x0+be-al, F(7,4)-x0-al+be, F(7,4)-x0+be-al, F(7,4)-x0+al-be+0, 1-al+F(3,4), 1-be+F(3,4), F(7,4)-x0+be+al-al]:
        if yy>=lo: cands.append(yy)
    cands=sorted(set(cands))
    y=next(c for c in cands if tt(c)>=F(3,4)) if any(tt(c)>=F(3,4) for c in cands) else None
    if y is None: continue
    x=[x0,y]; cnt2+=1
    w=works(x,a,b); assert w,('UNCOVERED',x,a,b,tau(x,a,b))
    C[tuple(sorted(w))]+=1
print('boundary PASS',cnt2); print(C.most_common(12))
