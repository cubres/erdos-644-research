import sys, itertools, collections
import w4_handbound_chain as C
from w4_handbound_pat import pat_budget
from w4_handbound_explore import L18
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3])
def L32o(a,b,c): S=a+b+c; return max(S,.5+b,(1+2*a-b+c)/2,(1+2*a+b+3*c)/3)
def L31o(a,b,c): S=a+b+c; return max(a+b,.5+a,.5+b,1+a-b-c,1-a+b-c,1-S/3,(3+S)/5,(1+a+b+2*c)/3,(2+3*c)/4)
def L26o(a,b,c): S=a+b+c; return max(S,1-a+c,1-b+c,1-a+b/2,1-b+a/2,(1+2*(a+b)+c)/3)
P0=C.PATS['P0']; P4=C.PATS['P4']
def P0o(a,b,c): return pat_budget(P0,a,b,c)
def P4o(a,b,c): return pat_budget(P4,a,b,c)
F={'L32':L32o,'L31':L31o,'L26':L26o,'P0':P0o,'P4':P4o}
lo=2-beta-2*h
tools=collections.defaultdict(list)
pts=[]
for i in range(N+1):
    m=lo+(h-lo)*i/N
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            if m<=(3*beta-2)/2+1e-12: continue
            v=(m,y,z); names=('m','y','z')
            ok=set()
            for n,f in F.items():
                for perm in itertools.permutations(range(3)):
                    if f(*[v[t] for t in perm])<=beta+1e-12: ok.add((n,''.join(names[t] for t in perm)))
            pts.append((v,ok))
# greedy set cover
uncovered=set(range(len(pts))); chosen=[]
while uncovered:
    cnt=collections.Counter()
    for i in uncovered:
        for t in pts[i][1]: cnt[t]+=1
    if not cnt: print('UNCOVERABLE',[pts[i][0] for i in list(uncovered)[:5]]); break
    t,c=cnt.most_common(1)[0]; chosen.append((t,c)); uncovered={i for i in uncovered if t not in pts[i][1]}
print(chosen)
# exact min set cover
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
T=sorted({t for _,ok in pts for t in ok})
A=np.array([[1 if t in ok else 0 for t in T] for _,ok in pts])
res=milp(np.ones(len(T)),constraints=LinearConstraint(A,1,np.inf),integrality=np.ones(len(T)),bounds=Bounds(0,1))
print('min cover',res.fun,[T[i] for i in range(len(T)) if res.x[i]>0.5])
