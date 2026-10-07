import sys, itertools, random
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
cands=[]
for p in pts[::max(1,len(pts)//40)]:
    v,pat=pattern(*p)
    if pat not in cands: cands.append(pat)
def cov(pat,p): return min(pat_budget(pat,*q) for q in set(itertools.permutations(p)))<=beta+1e-12
M=[[cov(pat,p) for p in pts] for pat in cands]
best=None
for i in range(len(cands)):
    if all(M[i]): print('single',cands[i]); best=1
if not best:
  for i,j in itertools.combinations(range(len(cands)),2):
    if all(a or b for a,b in zip(M[i],M[j])): print('pair',cands[i],cands[j]); break
for p in pts[:5]: print(p)
