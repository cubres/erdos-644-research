"""Exact brute-force check: FKW parity family (k=4k', N=7k'+1, |P|=4k', edges = k-sets with |E cap P| odd)
for k'=1,2: find a bad 7-tuple directly (SAT set cover on the explicit family, pysat) and verify it."""
import itertools, sys
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/mine')
from coded_families import is72
for kp in (1,2):
    k=4*kp; N=7*kp+1; P=set(range(4*kp))
    H=[frozenset(E) for E in itertools.combinations(range(N),k) if len(P&set(E))%2==1]
    ok,bad=is72(H,N)
    if not ok:
        # independent verification of badness
        assert len(bad)<=7 and all(E in set(H) for E in bad)
        assert not any(all((x in E) or (y in E) for E in bad) for x in range(N) for y in range(x,N))
    print(f"k={k} N={N} |H|={len(H)} (7,2)={ok}", ("bad tuple verified: "+str([sorted(E) for E in bad])) if not ok else "")
