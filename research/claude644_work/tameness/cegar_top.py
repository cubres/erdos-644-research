# CEGAR search: k-uniform families on [N] with tau >= t and property (7,2) (lazy bad-tuple cuts, exact C check).
# Each solution is saturated (random order) and reported with its twin classes; then excluded by requiring an
# edge outside its saturation, so successive solutions lie in pairwise different maximal families.
# usage: python3 cegar_top.py N k t [maxsol] [allvertices]
import sys, itertools, subprocess, time
from pysat.solvers import Cadical153
N,k,t=map(int,sys.argv[1:4]); maxsol=int(sys.argv[4]) if len(sys.argv)>4 else 20
allv=int(sys.argv[5]) if len(sys.argv)>5 else 1
E=[sum(1<<v for v in c) for c in itertools.combinations(range(N),k)]
var={F:i+1 for i,F in enumerate(E)}
S=Cadical153()
for T in itertools.combinations(range(N),t-1):
    Tm=sum(1<<v for v in T); S.add_clause([var[F] for F in E if not F&Tm])
if allv:
    for v in range(N): S.add_clause([var[F] for F in E if F>>v&1])
bad=subprocess.Popen(['./badfind','30'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
sat=subprocess.Popen(['./satur','7'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
def check(H):
    bad.stdin.write(f"{N} {len(H)} "+" ".join(map(str,H))+"\n"); bad.stdin.flush()
    tuples=[]
    while True:
        l=bad.stdout.readline().split()
        if l[0]=='END': break
        if l[0]=='BAD': tuples.append(list(map(int,l[1:])))
    return tuples
it=0; nsol=0; t0=time.time()
while nsol<maxsol:
    if not S.solve(): print(f"UNSAT after {it} iterations ({time.time()-t0:.0f}s): no further (7,2) family with tau>={t}"); break
    it+=1
    m=S.get_model(); H=[F for F in E if m[var[F]-1]>0]
    tu=check(H)
    if tu:
        for tt in tu: S.add_clause([-var[F] for F in set(tt)])
        if it%100==0: print(f'  iter {it} ({time.time()-t0:.0f}s) |H|={len(H)} cuts so far ~{it*len(tu)}',flush=True)
        continue
    sat.stdin.write(f"{N} {k} {len(H)} "+" ".join(map(str,H))+"\n"); sat.stdin.flush()
    info=sat.stdout.readline().strip(); fam=list(map(int,sat.stdout.readline().split()[1:]))
    nsol+=1
    print(f"SOL {nsol} (iter {it}, {time.time()-t0:.0f}s): found |H|={len(H)}; saturation: {info}",flush=True)
    print("   SATFAM", " ".join(format(F,'b').zfill(N)[::-1] for F in fam),flush=True)
    fs=set(fam); S.add_clause([var[F] for F in E if F not in fs])
