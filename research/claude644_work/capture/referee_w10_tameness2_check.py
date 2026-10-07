# Referee check for tameness#2 (Prop S).  (1) exact small-case identities of the proof (Fractions),
# (2) finite-k evaluation of the full failure-probability bound (lgamma), (3) monotonicity of the psi gap.
import math, itertools, random
from fractions import Fraction as Fr
from math import comb, lgamma, log, exp

def psi(x): return x*math.log(x)-(x-1)*math.log(x-1)

# (1) identity sum_{all k-sets E} P(E subset W) = C(|v|,k) and weight bound, exact, small cases
def ff(a,e):
    r=1
    for j in range(e): r*= (a-j)
    return r
random.seed(1)
bad=0; tests=0
for trial in range(300):
    p=random.randint(1,3); ns=[random.randint(1,5) for _ in range(p)]; N=sum(ns)
    k=random.randint(1,N); s=random.randint(0,3)
    u=[random.randint(0,n) for n in ns]; v=[max(ui-s,0) for ui in u]
    labels=[i for i,n in enumerate(ns) for _ in range(n)]
    tot=Fr(0)
    for E in itertools.combinations(range(N),k):
        e=[0]*p
        for x in E: e[labels[x]]+=1
        w=Fr(1)
        for i in range(p): w*=Fr(ff(v[i],e[i]),ff(ns[i],e[i]))
        tot+=w
        if w>0:
            tests+=1
            if w > Fr(1)*1 and False: pass
            if float(w) > exp(-s*k/N)*(1+1e-12): bad+=1
    assert tot==comb(sum(v),k), (ns,k,v,tot)
print("identity sum P(E in W)=C(|v|,k): OK on 300 random cases; weight-bound violations:",bad,"of",tests)

# (3) gap monotone in beta
prev=-1
for b in [i/1000 for i in range(1,500)]:
    d=psi(1+b)-psi(1+b/2); assert d>prev; prev=d
print("psi gap increasing on (0,0.5): OK")

# (2) finite-k failure bound
def lC(n,r): return lgamma(n+1)-lgamma(r+1)-lgamma(n-r+1)
def fail_log(k,beta,p,s,eta=1/7):
    N=7*k//4-1; u0=int(math.floor((1+beta)*k)); m=int(math.floor((1+beta/2)*k))
    lrho=log(2*N*log(2))-lC(u0,k); lmu=lrho+lC(m,k)
    om=math.exp(-s*k/N); a=1-eta
    # exact Chernoff form (e mu/a)^{a/om}, not the 6/7 relaxation
    lc=N*log(p)+p*log(N+1)+(a/om)*(1+lmu-log(a))
    lt=-N*log(2)   # tau part: 2^N * 4^{-N}
    return lc,lt,(3/4-beta)*k-(s+1)*p-3*beta*k/8
for (beta,p,s) in [(0.1,2,5),(0.1,7,6),(0.1,64,8),(0.1,10**6,10),(0.02,2,7),(0.02,10**6,12),(0.02,10**6,13),(0.02,10**6,63),(0.1,2,13)]:
    kk=None
    for k in range(8,10**7,4):
        lc,lt,slack=fail_log(k,beta,p,s)
        if lc< log(0.01) and slack>0: kk=k;break
        if k>4000: k+=0
    print(f"beta={beta} p={p} s={s}: first k (4|k) with Chernoff-union bound <0.01: {kk}")

print("-- large p: geometric k scan (Chernoff bound log, tau-slack) --")
for (beta,p,s) in [(0.1,10**6,10),(0.02,10**6,12),(0.02,10**6,13),(0.02,10**6,63),(0.1,2,4),(0.02,10**6,11)]:
    out=[]
    for e in range(4,13):
        k=4*(10**e//4); lc,lt,sl=fail_log(k,beta,p,s)
        out.append((e,round(lc,1),sl>0))
    print(beta,p,s,out)
