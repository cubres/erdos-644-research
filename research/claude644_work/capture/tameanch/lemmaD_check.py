# Exact check of LEMMA D (deletion coupling), notes_tameanchored [a2]:
#   f_pi((u-s)^+) <= max_{W'': |W''|=|u|} #edges(H' inside W'') * (m/(k'+m))^s ,   m = |u| - k'.
# f computed EXACTLY (Fractions) by enumerating all sets W' of profile (u-s)^+ for random small families,
# random partitions (any number of parts, including tiny parts with u_i < s), random profiles, s in {1,2,3}.
# Also checks the mediant bound  prod_{i: e_i>0} C(d_i,s)/C(u_i,s) <= (m/(k'+m))^s  per edge (the inner step),
# and the per-W'' inequality  P(W' contains an edge | W'') <= #edges(W'') (m/(k'+m))^s.
import itertools, random, sys
from fractions import Fraction
from math import comb

def profile_sets(parts, prof):
    """all sets with |W cap P_i| = prof[i]"""
    choices = [list(itertools.combinations(P, prof[i])) for i, P in enumerate(parts)]
    for combo in itertools.product(*choices):
        yield frozenset(x for c in combo for x in c)

def run(seed, ntests):
    rng = random.Random(seed)
    viol = 0; tested = 0; tight = 0
    for _ in range(ntests):
        N = rng.randint(6, 10)
        V = list(range(N))
        kmin = rng.randint(2, 4); kmax = kmin + rng.randint(0, 1)
        # random family of rank <= kmax with min edge size kmin
        nE = rng.randint(2, 12)
        H = set()
        while len(H) < nE:
            sz = rng.randint(kmin, kmax)
            H.add(frozenset(rng.sample(V, sz)))
        H = list(H); kp = min(len(E) for E in H)
        # random partition with p parts (1..N)
        p = rng.randint(1, N)
        labels = [rng.randrange(p) for _ in V]
        parts = [[x for x in V if labels[x] == i] for i in range(p)]
        parts = [P for P in parts if P]; p = len(parts)
        s = rng.randint(1, 3)
        # random profile u <= n with |u| >= kp
        for _try in range(20):
            u = [rng.randint(0, len(P)) for P in parts]
            if sum(u) >= kp: break
        else:
            continue
        m = sum(u) - kp
        us = [max(0, ui - s) for ui in u]
        # exact f((u-s)^+)
        tot = 0; good = 0
        for W in profile_sets(parts, us):
            tot += 1
            if any(E <= W for E in H): good += 1
        if tot == 0: continue
        f = Fraction(good, tot)
        # max over W'' of #edges inside, and per-edge mediant bound
        maxedges = 0
        bound_fac = Fraction(m, kp + m) ** s if (kp + m) > 0 else Fraction(0)
        for W2 in profile_sets(parts, u):
            inside = [E for E in H if E <= W2]
            maxedges = max(maxedges, len(inside))
            # per-edge exact deletion probability vs mediant bound
            pw = Fraction(0)
            for E in inside:
                pe = Fraction(1)
                for i, P in enumerate(parts):
                    ei = len(E & set(P)); di = u[i] - ei
                    if ei == 0: continue
                    if u[i] < s: pe = Fraction(0); break
                    pe *= Fraction(comb(di, s), comb(u[i], s))
                if pe > bound_fac + Fraction(0):
                    viol += 1; print("VIOL per-edge", N, kp, parts, u, s, sorted(E), pe, bound_fac)
                pw += pe
            if pw > len(inside) * bound_fac:
                viol += 1; print("VIOL per-W''", N, parts, u, s, pw, len(inside) * bound_fac)
        rhs = maxedges * bound_fac
        tested += 1
        if f > rhs:
            viol += 1
            print("VIOLATION", dict(N=N, H=[sorted(E) for E in H], parts=parts, u=u, s=s, f=f, rhs=rhs, maxedges=maxedges))
        if f == rhs and f > 0: tight += 1
    return tested, viol, tight

if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    ntests = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    tested, viol, tight = run(seed, ntests)
    print(f"seed={seed}: tested={tested} violations={viol} tight_cases={tight}")
