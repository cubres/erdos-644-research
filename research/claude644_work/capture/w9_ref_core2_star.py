"""Referee w9 core#2 IMPROVEMENT CHECK: 'Theorem L-' : (7,2) [at-most-7 convention], codegree <= lam, lam >= 1
  => tau <= 3lam - 1.   (Referee's hand proof; this script is the exhaustive adversarial e2e certificate.)
Proof: if |H|<=6, tau<=2<=3lam-1.  Else take any 7 distinct edges; their 2-transversal {x,y} puts >=4 of them
through one point x.  G1..G4 := four of them; all pairwise intersections contain x, so |I(mu)| <= 2lam-1.
Suppose tau >= t := 3lam.  G5 avoids I5 (<=2lam-1<=t-1); g in G5; G6 avoids I6+{g} (<=2lam<=t-1), so G6!=G5 and
|G5&G6|<=lam; G7 avoids I7+(G5&G6) (<=3lam-1=t-1).  Lemma Q logic => bad 7-tuple.  Contradiction.
Check: families with codegree lam and tau >= 3lam (so not (7,2) by the claim); ALL 'star quads' (4 distinct edges
through a common point) up to a sample, all 6 bijections, all adversarial G5,g,G6,G7 (capped); assert every
avoided set has size <= t-1 = 3lam-1, requested edges exist, and the 7 edges have no <=2-transversal."""
import itertools, random, sys
from w9_ref_core2_e2e import pg, tau, pierce2, pc
M = [((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))]
def starquads(H, n):
    out = set()
    for x in range(n):
        S = [E for E in H if E >> x & 1]
        for Q in itertools.combinations(S, 4): out.add(Q)
    return list(out)
def run(H, n, rnd, maxq=30, cap=6):
    lam = max(pc(a & b) for a, b in itertools.combinations(H, 2)); t = tau(H, n)
    assert lam >= 1 and t >= 3*lam
    t = 3*lam   # use only the weaker hypothesis tau >= 3lam: budget t-1 = 3lam-1
    Qs = starquads(H, n)
    if len(Qs) > maxq: Qs = rnd.sample(Qs, maxq)
    sub = lambda L: L if len(L) <= cap else rnd.sample(L, cap)
    cnt = 0
    for G in Qs:
        I = [(G[a] & G[b]) | (G[c] & G[d]) for ((a,b),(c,d)) in M]
        assert max(map(pc, I)) <= 2*lam - 1
        for o in itertools.permutations(range(3)):
            I5, I6, I7 = I[o[0]], I[o[1]], I[o[2]]
            C5 = [E for E in H if not E & I5]; assert pc(I5) <= t-1 and C5
            for G5 in sub(C5):
                for g in [v for v in range(n) if G5 >> v & 1]:
                    Z6 = I6 | 1 << g; assert pc(Z6) <= t-1
                    C6 = [E for E in H if not E & Z6]; assert C6
                    for G6 in sub(C6):
                        assert G6 != G5 and pc(G5 & G6) <= lam
                        Z7 = I7 | (G5 & G6); assert pc(Z7) <= t-1
                        C7 = [E for E in H if not E & Z7]; assert C7
                        for G7 in sub(C7):
                            assert not pierce2(list(G) + [G5, G6, G7], n); cnt += 1
    return lam, len(Qs), cnt
if __name__ == '__main__':
    rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    for q in (2, 3, 5):   # PG(2,2)=Fano: lam=1, tau=3 = 3lam (tight case)
        L, n = pg(q); lam, nq, c = run(L, n, rnd)
        print(f"PG(2,{q}) lam={lam} tau={tau(L,n)}: {nq} star quads, {c} tuples PASS", flush=True)
    for (n, k) in [(5, 2), (8, 3), (9, 3), (12, 4)]:   # tau = n-k+1 >= 3(k-1)
        H = [sum(1 << v for v in c) for c in itertools.combinations(range(n), k)]
        lam, nq, c = run(H, n, rnd, 15, 5)
        print(f"K_{n}^{k} lam={lam} tau={n-k+1}: {nq} star quads, {c} tuples PASS", flush=True)
    tot = fams = tight = 0
    while fams < 80:
        n = rnd.randint(6, 12); lam = rnd.choice([1, 1, 2, 2, 3])
        cand = [sum(1 << v for v in rnd.sample(range(n), rnd.randint(1, n - 1))) for _ in range(600)]
        H = []
        for E in cand:
            if E not in H and all(pc(E & F) <= lam for F in H): H.append(E)
        if len(H) < 4: continue
        l2 = max(pc(a & b) for a, b in itertools.combinations(H, 2))
        if l2 < 1: continue
        tt = tau(H, n)
        if tt < 3*l2: continue
        _, nq, c = run(H, n, rnd, 8, 5)
        if nq: fams += 1; tot += c; tight += (tt == 3*l2)
    print(f"random mixed-size families with tau>=3lam: {fams} ({tight} with tau==3lam exactly), {tot} tuples PASS", flush=True)
