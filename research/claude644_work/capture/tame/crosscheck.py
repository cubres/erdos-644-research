import itertools, random, sys, time
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/mine')
from tc_lib import *
from coded_families import is72 as sat72
def explicit(n,c,a,k):
    verts=[]
    for i,cnt in enumerate(n): verts+=[i]*cnt
    N=len(verts); H=[]
    for E in itertools.combinations(range(N),k):
        s=[0]*len(a)
        for x in E:
            for b in range(len(a)): s[b]^=c[verts[x]][b]
        if tuple(s)==tuple(a): H.append(frozenset(E))
    return H,N
random.seed(5); agree=0; tot=0
for trial in range(40):
    k=random.choice([4,5,6]); r=random.choice([1,2]); p=random.choice([2,3,4])
    n=[random.randint(1,5) for _ in range(p)]
    if sum(n)>13 or sum(n)<k+1: continue
    c=[tuple(random.randint(0,1) for _ in range(r)) for _ in range(p)]
    a=tuple(random.randint(0,1) for _ in range(r))
    H,N=explicit(n,c,a,k)
    if not H: continue
    t0=time.time(); mine=is72_code(n,c,a,k)[0]; sat=sat72(H,N)[0]
    tot+=1; agree+= (mine==sat)
    print(n,c,a,k,"|H|=",len(H),"tool",mine,"sat",sat, "%.1fs"%(time.time()-t0), flush=True)
print("agree",agree,"of",tot)
