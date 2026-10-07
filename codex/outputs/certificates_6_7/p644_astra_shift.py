"""Exact SAT search for failure of (7,2) under a standard 0<-1 shift.

The search is CEGAR, but every accepted witness is independently checked by
enumerating all its subfamilies of size at most seven. No UNSAT result is used
as a theorem without an independently checkable proof certificate.
"""
import argparse
import itertools as it
import json
import time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType


def shift(H, i=0, j=1):
    H = set(map(frozenset, H))
    return {((E - {j}) | {i}) if j in E and i not in E and
            ((E - {j}) | {i}) not in H else E for E in H}


def tau(H, n):
    for s in range(n + 1):
        for T in it.combinations(range(n), s):
            if all(set(T) & E for E in H):
                return s


def direct_72(H, n):
    H = list(map(frozenset, H))
    pairs = list(it.combinations(range(n), 2))
    # Padding with other edges makes it enough to check maximal subfamilies.
    for F in it.combinations(H, min(7, len(H))):
        if not any(all(set(P) & E for E in F) for P in pairs):
            return False, F
    return True, None


def bad_subfamily(H, n):
    H = list(H)
    with Cadical153() as S:
        for P in it.combinations(range(n), 2):
            S.add_clause([j+1 for j, E in enumerate(H) if not set(P) & E])
        C = CardEnc.atmost(list(range(1, len(H)+1)), bound=7,
                           top_id=len(H), encoding=EncType.seqcounter)
        S.append_formula(C.clauses)
        if not S.solve():
            return None
        model = set(x for x in S.get_model() if x > 0)
        return [E for j, E in enumerate(H) if j+1 in model]


def search(k, n, seconds=60, intersecting=False):
    E = list(map(frozenset, it.combinations(range(n), k)))
    idx = {e: j for j, e in enumerate(E)}
    m = len(E)
    with Cadical153() as S:
        for a, e in enumerate(E):
            z = m+a+1
            if 0 in e and 1 not in e:
                hi = idx[(e-{0}) | {1}]
                S.add_clause([-z, a+1, hi+1])
            elif 1 in e and 0 not in e:
                lo = idx[(e-{1}) | {0}]
                S.add_clause([-z, a+1]); S.add_clause([-z, lo+1])
            else:
                S.add_clause([-z, a+1])
        for P in it.combinations(range(n), 2):
            S.add_clause([m+j+1 for j, e in enumerate(E) if not set(P) & e])
        C = CardEnc.atmost(list(range(m+1, 2*m+1)), bound=7,
                           top_id=2*m, encoding=EncType.seqcounter)
        S.append_formula(C.clauses)
        if intersecting:
            for a, b in it.combinations(range(m), 2):
                if not E[a] & E[b]: S.add_clause([-a-1, -b-1])
        start = time.monotonic(); rounds = 0
        while time.monotonic()-start < seconds:
            rounds += 1
            if not S.solve():
                return {'status': 'UNSAT_SEARCH_ONLY', 'rounds': rounds}
            model = set(x for x in S.get_model() if x > 0)
            H = [e for a,e in enumerate(E) if a+1 in model]
            bad = bad_subfamily(H, n)
            if bad is None:
                out = shift(H)
                assert direct_72(H, n)[0]
                assert not direct_72(out, n)[0]
                return {'status': 'EXACT_WITNESS', 'rounds': rounds,
                        'H': sorted(map(sorted, H)), 'shifted': sorted(map(sorted, out)),
                        'bad_shifted': sorted(map(sorted, direct_72(out,n)[1])),
                        'tau_before':tau(H,n), 'tau_after':tau(out,n)}
            S.add_clause([-idx[e]-1 for e in bad])
        return {'status': 'TIME_LIMIT', 'rounds':rounds}


if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=int,default=60)
    ap.add_argument('--out',default='logs/astra_shift.json');args=ap.parse_args()
    results=[]
    for k,n in [(3,6),(3,7),(4,7),(4,8)]:
        r={'k':k,'n':n, 'intersecting':True,
           **search(k,n,args.seconds,intersecting=True)}
        print(json.dumps(r),flush=True);results.append(r)
        if r['status']=='EXACT_WITNESS':break
    with open(args.out,'w') as f:json.dump(results,f,indent=2)
