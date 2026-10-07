"""Erdős #644, fast exact small cases.

Question: is there a k-uniform family on N vertices with the (7,2)-property
(every subfamily of AT MOST 7 edges has a 2-point transversal) and tau >= t ?

Improvements over p644_sat.py:
  * mode nu2 : WLOG two disjoint edges A={0..k-1}, B={k..2k-1} are present and no edge is
               disjoint from A∪B (three pairwise disjoint edges form a bad 3-family).
  * mode int : intersecting families only (forbid disjoint pairs). Valid when t <= k.
  * pre-seeding of all minimal bad subfamilies of size <= s (branch on the lowest uncovered pair).
  * batch learning: per SAT model, a bounded DFS emits many minimal bad subfamilies at once.
  * cardinality cap |H| <= C(t+k-1, k) (Bollobás: a tau-critical k-uniform family with tau=t).

A subfamily F is 2-pierceable iff some pair {a,b} meets every edge of F, i.e. iff the OR of the
edges' "missed-pair" masks is not the full mask.
"""
import itertools, sys, time, math, argparse
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType


class Instance:
    def __init__(self, k, N):
        self.k, self.N = k, N
        self.edges = list(itertools.combinations(range(N), k))
        self.eidx = {E: i for i, E in enumerate(self.edges)}
        self.pairs = list(itertools.combinations(range(N), 2))
        self.pidx = {p: i for i, p in enumerate(self.pairs)}
        self.FULL = (1 << len(self.pairs)) - 1
        # miss[i] = bitmask of pairs disjoint from edge i
        self.miss = []
        for E in self.edges:
            Es = set(E); m = 0
            for pi, (a, b) in enumerate(self.pairs):
                if a not in Es and b not in Es: m |= 1 << pi
            self.miss.append(m)
        # avoiders[pi] = list of edge indices missing pair pi
        self.avoiders = [[i for i in range(len(self.edges)) if self.miss[i] >> pi & 1] for pi in range(len(self.pairs))]

    def is_bad(self, idxs):
        m = 0
        for i in idxs: m |= self.miss[i]
        return m == self.FULL

    def enum_bad(self, max_size, base=(), allowed=None, budget=10**7):
        """All minimal bad families of size <= max_size containing `base` (edge indices),
        using only edges in `allowed` (set) if given. Branch on the lowest uncovered pair."""
        base = tuple(base); m0 = 0
        for i in base: m0 |= self.miss[i]
        out = set(); nodes = [0]
        allowed_set = None if allowed is None else set(allowed)
        def rec(chosen, mask, last_added_set):
            nodes[0] += 1
            if nodes[0] > budget: return
            if mask == self.FULL:
                # minimality: no proper subfamily (dropping one non-base edge) is bad
                for i in chosen:
                    if i in base: continue
                    mm = 0
                    for j in chosen:
                        if j != i: mm |= self.miss[j]
                    if mm == self.FULL: return
                out.add(frozenset(chosen)); return
            if len(chosen) >= max_size: return
            # lowest uncovered pair
            unc = (~mask) & self.FULL
            pi = (unc & -unc).bit_length() - 1
            for i in self.avoiders[pi]:
                if i in last_added_set: continue
                if allowed_set is not None and i not in allowed_set: continue
                rec(chosen + (i,), mask | self.miss[i], last_added_set | {i})
        rec(base, m0, set(base))
        return out, nodes[0]


def solve(k, N, t, mode='plain', preseed=4, batch=200, cap=True, max_iter=10**6, verbose=True, log=None):
    inst = Instance(k, N)
    E, m = inst.edges, len(inst.edges)
    var = lambda i: i + 1
    S = Cadical153()
    t0 = time.time()
    def say(s):
        if verbose: print(s, flush=True)
        if log: log.write(s + '\n'); log.flush()
    # tau >= t : every (N-t+1)-set contains an edge
    for U in itertools.combinations(range(N), N - t + 1):
        Us = set(U); S.add_clause([var(i) for i, e in enumerate(E) if set(e) <= Us])
    base = []
    if mode == 'nu2':
        A = tuple(range(k)); B = tuple(range(k, 2 * k))
        if 2 * k > N: return None, 0, 'N<2k'
        base = [inst.eidx[A], inst.eidx[B]]
        S.add_clause([var(base[0])]); S.add_clause([var(base[1])])
        AB = set(A) | set(B)
        for i, e in enumerate(E):
            if not (set(e) & AB): S.add_clause([-var(i)])
    elif mode == 'int':
        for i in range(m):
            for j in range(i + 1, m):
                if not (set(E[i]) & set(E[j])): S.add_clause([-var(i), -var(j)])
    nclauses = 0
    if preseed:
        bad, nodes = inst.enum_bad(preseed, base=tuple(base))
        for F in bad: S.add_clause([-var(i) for i in F if i not in base] or [-var(base[0])])
        nclauses += len(bad)
        say(f"  preseed: {len(bad)} minimal bad families of size<={preseed} (containing base) [{nodes} nodes, {time.time()-t0:.1f}s]")
    top = m
    if cap:
        bound = math.comb(t + k - 1, k)
        if bound < m:
            card = CardEnc.atmost(lits=[var(i) for i in range(m)], bound=bound, top_id=top, encoding=EncType.seqcounter)
            for cl in card.clauses: S.add_clause(cl)
            top = max(top, card.nv)
            say(f"  cardinality cap |H| <= {bound}")
    it = 0
    while True:
        it += 1
        if it > max_iter: return 'TIMEOUT', it, None
        if not S.solve(): return None, it, None
        model = S.get_model(); chosen = [i for i in range(m) if model[i] > 0]
        # batch DFS for minimal bad subfamilies of size <= 7 among chosen (must contain base if nu2)
        bad, nodes = inst.enum_bad(7, base=tuple(base), allowed=chosen, budget=3 * 10**5)
        if not bad:
            # also families NOT containing base (in nu2 mode base edges are present but a bad
            # family may avoid them): run again without base
            if base:
                bad, nodes = inst.enum_bad(7, base=(), allowed=chosen, budget=3 * 10**5)
            if not bad:
                # exact fallback: set-cover SAT over chosen edges
                sub = Cadical153(); ok = True
                for pi in range(len(inst.pairs)):
                    cl = [j + 1 for j, i in enumerate(chosen) if inst.miss[i] >> pi & 1]
                    if not cl: ok = False; break
                    sub.add_clause(cl)
                if not ok: return [E[i] for i in chosen], it, chosen
                cd = CardEnc.atmost(lits=list(range(1, len(chosen) + 1)), bound=7, top_id=len(chosen), encoding=EncType.seqcounter)
                for cl in cd.clauses: sub.add_clause(cl)
                if sub.solve():
                    sm = sub.get_model(); bad = {frozenset(chosen[j] for j in range(len(chosen)) if sm[j] > 0)}
                else:
                    return [E[i] for i in chosen], it, chosen
        cnt = 0
        for F in bad:
            S.add_clause([-var(i) for i in F]); cnt += 1
            if cnt >= batch: break
        nclauses += cnt
        if verbose and it % 100 == 0:
            say(f"  iter {it}: |H|={len(chosen)}, +{cnt} clauses (total {nclauses}), {time.time()-t0:.0f}s")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('k', type=int); ap.add_argument('N', type=int); ap.add_argument('t', type=int)
    ap.add_argument('--mode', default='nu2', choices=['plain', 'nu2', 'int'])
    ap.add_argument('--preseed', type=int, default=4)
    ap.add_argument('--nocap', action='store_true')
    ap.add_argument('--log', default=None)
    a = ap.parse_args()
    log = open(a.log, 'a') if a.log else None
    t0 = time.time()
    print(f"k={a.k} N={a.N} tau>={a.t} mode={a.mode} preseed={a.preseed}", flush=True)
    res, it, chosen = solve(a.k, a.N, a.t, mode=a.mode, preseed=a.preseed, cap=not a.nocap, log=log)
    if res is None: msg = f"RESULT k={a.k} N={a.N} tau>={a.t} mode={a.mode}: NO ({it} iters, {time.time()-t0:.0f}s)"
    elif res == 'TIMEOUT': msg = f"RESULT k={a.k} N={a.N} tau>={a.t} mode={a.mode}: TIMEOUT"
    elif isinstance(res, str): msg = f"RESULT k={a.k} N={a.N} tau>={a.t} mode={a.mode}: {res}"
    else: msg = f"RESULT k={a.k} N={a.N} tau>={a.t} mode={a.mode}: YES |H|={len(res)} ({it} iters, {time.time()-t0:.0f}s) edges={res}"
    print(msg, flush=True)
    if log: log.write(msg + '\n'); log.close()
