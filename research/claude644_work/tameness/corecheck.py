# for the verified wide tau=4 family (N=11,k=5): over all vertex subsets U, max tau(H[U]) at each width of H[U]
import sys, itertools
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
import lib72 as L
line=open('logs/wide_tau4_k5_verified.txt').read().split('\n')[1]
H=list(map(int,line.split(':')[1].split())); n=11
def width(F,U):
    S=set(F); pts=[v for v in range(n) if U>>v&1]
    def geq(a,b): return all(((E^(1<<a)^(1<<b)) in S) for E in F if (E>>b&1) and not (E>>a&1))
    ge={(a,b):(a==b or geq(a,b)) for a in pts for b in pts}
    gt={(a,b):(a!=b and ge[a,b] and ((not ge[b,a]) or a<b)) for a in pts for b in pts}
    mR={v:-1 for v in pts}
    def aug(u,vis):
        for v in pts:
            if gt[u,v] and v not in vis:
                vis.add(v)
                if mR[v]<0 or aug(mR[v],vis): mR[v]=u; return True
        return False
    mm=sum(aug(u,set()) for u in pts)
    return len(pts)-mm
best={}
for U in range(1<<n):
    F=[E for E in H if E&~U==0]
    if not F: continue
    t=L.tau(F,n)
    if t<3: continue
    w=width(F,U)
    if t not in best or w<best[t][0]: best[t]=(w,U,len(F))
for t in sorted(best): print("tau(H[U])=%d: min width %d  (U=%s, %d edges)"%(t,best[t][0],[v for v in range(n) if best[t][1]>>v&1],best[t][2]))
