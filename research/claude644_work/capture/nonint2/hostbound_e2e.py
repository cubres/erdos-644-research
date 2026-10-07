"""End-to-end check of the anchored 7.97-tuple used in Lemma H (two-anchor host bound).
Random host families F (edges inside U=[n]) with tau(F) = s'+1 computed exactly; random anchor A with
C = A n U.  If the block-size condition ceil((n-c)/3)+2*ceil(c/4) <= s' holds, build the six rows G_i in F
avoiding the blocks and verify that {A,G_1..G_6} has no 2-transversal (exhaustive over pairs)."""
import random, itertools, sys
def tau(F, n):
    for r in range(n+1):
        for T in itertools.combinations(range(n), r):
            Ts = set(T)
            if all(Ts & E for E in F): return r
def classes(pts, sizes):
    out=[]; i=0
    for z in sizes: out.append(set(pts[i:i+z])); i+=z
    return out
def split(m, parts):
    q, r = divmod(m, parts); return [q+1]*r + [q]*(parts-r)
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
tested = fails = 0
for trial in range(4000):
    n = random.randint(6, 12); k = random.randint(3, n-2)
    allk = [frozenset(E) for E in itertools.combinations(range(n), k)]
    F = [E for E in allk if random.random() < 0.85] or allk
    t = tau(F, n); sp = t-1
    c = random.randint(0, min(n, 6))
    U = list(range(n)); random.shuffle(U)
    C = U[:c]; rest = U[c:]
    if -(-(n-c)//3) + 2*(-(-c//4)) > sp: continue
    W = classes(rest, split(n-c, 3)); Cc = classes(C, split(c, 4))
    lab = {'12':W[0],'34':W[1],'56':W[2],'135':Cc[0],'146':Cc[1],'236':Cc[2],'245':Cc[3]}
    blocks = [set().union(*[S for L,S in lab.items() if str(i) in L]) for i in range(1,7)]
    rows = []
    for P in blocks:
        cand = [E for E in F if not (E & P)]
        assert cand, 'tau bound violated?'
        rows.append(random.choice(cand))
    A = set(C) | {100+j for j in range(random.randint(1,3))}   # private outside points
    tup = [A] + [set(E) for E in rows]
    pts = set().union(*tup)
    bad = not any(all((x in E) or (y in E) for E in tup) for x in pts for y in pts)
    tested += 1
    if not bad: fails += 1; print('FAIL', n, k, c, sp)
print('tested', tested, 'fails', fails)
