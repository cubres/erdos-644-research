import sys, itertools
import w4_handbound_chain as C
from w4_handbound_pat import pat_budget, pattern
beta=float(sys.argv[1]); h=float(sys.argv[2]); N=int(sys.argv[3]); names=sys.argv[4].split(',')
lo=2-beta-2*h
pts=[]
for i in range(N+1):
    m=lo+(h-lo)*i/N
    w=min(m,1-(beta+m)/2)
    for j in range(N+1):
        for k in range(j+1):
            y=w*j/N; z=w*k/N
            if C.bestg(m,y,z,m,h,beta,names,False)[0]>beta+1e-12: pts.append((m,y,z))
print(len(pts))
# collect candidate patterns from MILP at sample points
cands=[]
import random
random.seed(1)
for p in random.sample(pts,min(25,len(pts))):
    v,pat=pattern(*p)
    if pat not in cands: cands.append(pat)
print('cands',len(cands))
def cov(pat,p): return min(pat_budget(pat,*q) for q in set(itertools.permutations(p)))<=beta+1e-12
res=[]
for pat in cands:
    c=sum(cov(pat,p) for p in pts); res.append((c,pat))
res.sort(key=lambda r:-r[0])
for c,pat in res[:6]: print(c,pat)
