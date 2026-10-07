"""NUMERICAL extremal problem for the |H|=2 case (3 parts, part 0 4/7-light for every type, every type heavy
(fill>4/7) in part 1 (B) or part 2 (A)).  Constraint: NO pair a in A, b in B with
   (L0) a0+b0 <= x0   and   (Gm) (x1-b1)+(x2-a2) > (3/4)max(1-a0, 1-b0).
(Such a pair gives a bad tuple by GGP-mass.)  Maximise exact(float) tau*.  If sup <= 3/4 the |H|=2 light case
follows from GGP-mass alone."""
import random, math, sys
from h2climb import tau_star
def classify(c,x):
    A=7*c[2]>4*x[2]; B=7*c[1]>4*x[1]
    return A,B
def valid(ts,x):
    if any(v<0.02 for v in x): return False
    As=[];Bs=[]
    for c in ts:
        if min(c)<-1e-12 or any(c[i]>x[i]+1e-12 for i in range(3)): return False
        if 7*c[0]>4*x[0]: return False
        A,B=classify(c,x)
        if not (A or B): return False
        if A: As.append(c)
        if B: Bs.append(c)
    for a in As:
        for b in Bs:
            if a[0]+b[0]<=x[0]+1e-12 and (x[1]-b[1])+(x[2]-a[2])>0.75*max(1-a[0],1-b[0])-1e-12: return False
    return True
def rtype(x,rng,heavy):
    for _ in range(200):
        c0=rng.uniform(0,4*x[0]/7)
        if heavy==2: c2=rng.uniform(4*x[2]/7,min(x[2],1-c0)); c=(c0,1-c0-c2,c2)
        else: c1=rng.uniform(4*x[1]/7,min(x[1],1-c0)); c=(c0,c1,1-c0-c1)
        if min(c)>=0 and all(c[i]<=x[i] for i in range(3)): return c
    return None
def run(m,rng,iters):
    while True:
        x=[rng.uniform(0.05,1.75),rng.uniform(0.6,1.75),rng.uniform(0.6,1.75)]
        ts=[rtype(x,rng,2 if k%2 else 1) for k in range(m)]
        if None not in ts and valid(ts,x): break
    cur=tau_star(ts,x); T=0.03; best=(cur,x,ts)
    for it in range(iters):
        x2=[v+rng.gauss(0,0.02) for v in x]; ts2=[]
        for c in ts:
            if rng.random()<0.6:
                d=[rng.gauss(0,0.02) for _ in range(3)]; s=sum(d)/3; c=tuple(c[i]+d[i]-s for i in range(3))
            ts2.append(c)
        if rng.random()<0.05 and len(ts2)<12:
            n=rtype(x2,rng,rng.choice([1,2]))
            if n: ts2.append(n)
        if rng.random()<0.05 and len(ts2)>2: ts2.pop(rng.randrange(len(ts2)))
        if not valid(ts2,x2): continue
        v=tau_star(ts2,x2)
        if v>=cur or rng.random()<math.exp((v-cur)/T): x,ts,cur=x2,ts2,v
        if cur>best[0]: best=(cur,x,ts)
        T=max(0.0005,T*0.9993)
    return best
rng=random.Random(int(sys.argv[1])); B=(0,)
for r in range(int(sys.argv[2])):
    res=run(rng.randint(2,6),rng,int(sys.argv[3]))
    if res[0]>B[0]:
        B=res; print('best',round(res[0],4),[round(v,4) for v in res[1]],[[round(v,4) for v in c] for c in res[2]],flush=True)
print('FINAL',B[0])
