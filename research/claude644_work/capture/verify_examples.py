"""
Exact checks (integer/bitmask arithmetic) for the examples used in the report.
Run: python3 verify_examples.py
 (A) Sharpness of the Triple Lemma: complete (4j+2)-uniform family on 7j+3 points, j=1:
     (7,2) [exact DFS], tau = 3j+2 = 5, and an explicit good triple with union 6j+3 = 9,
     so tau = floor(9/2)+1.
 (B) C_9 family (note 7.103): for every critical pair (E,B): tau(H^(m)_U) and tau(K_m), m=0..3.
 (C) Core+private-tails family: core = all r-subsets of an N-set (4N<7r), tails of length s:
     (7,2) [exact DFS], tau, every edge critical, profile tau(K_m) at every critical pair.
 (D) Host bound  tau(H^(m)_{E u B}) <= ceil(e/2) + max(0, e+|B|-2t+3+2m)  (when e+3+2m<=2t)
     checked for ALL edges E, ALL B subset V\\E of size t-1, m=0..2, on the families above.
"""
import itertools, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from lib72 import is_72, tau, complete, popcount

def bits(S): return sum(1 << v for v in S)

def critical_sets(H, n, t):
    """all (E,B): E in H, B a (t-1)-set disjoint from E meeting every other edge."""
    out = []
    for E in H:
        others = [F for F in H if F != E]
        for Bt in itertools.combinations([v for v in range(n) if not (E >> v) & 1], t - 1):
            B = bits(Bt)
            if all(F & B for F in others):
                out.append((E, B))
    return out

def light(H, U, m):
    return [F for F in H if popcount(F & ~U) <= m]

def heavy(H, U, m):
    return [F for F in H if popcount(F & ~U) > m]

def host_bound_check(H, n, t, label, mmax=2):
    viol = 0; checked = 0
    for E in H:
        e = popcount(E)
        for Bt in itertools.combinations([v for v in range(n) if not (E >> v) & 1], t - 1):
            U = E | bits(Bt)
            for m in range(mmax + 1):
                if e + 3 + 2 * m > 2 * t: continue
                q = tau(light(H, U, m), n)
                bound = (e + 1) // 2 + max(0, e + (t - 1) - 2 * t + 3 + 2 * m)
                checked += 1
                if q > bound:
                    viol += 1; print("HOST BOUND VIOLATION", label, bin(E), Bt, m, q, bound)
    print(f"  host bound: {checked} (E,B,m) triples checked on {label}, violations: {viol}")

# (A)
j = 1; k = 4 * j + 2; n = 7 * j + 3
H = complete(n, k)
print("(A) complete %d-uniform on %d points:" % (k, n))
print("  is (7,2):", is_72(H, n))
t = tau(H, n); print("  tau =", t, " (3j+2 =", 3 * j + 2, ")")
X, Y, Z = range(0, 2*j+1), range(2*j+1, 4*j+2), range(4*j+2, 6*j+3)
E, F, G = bits(list(X)+list(Y)), bits(list(Y)+list(Z)), bits(list(X)+list(Z))
assert E in H and F in H and G in H and (E & F & G) == 0
N = popcount(E | F | G)
print("  good triple union N =", N, " floor(N/2)+1 =", N // 2 + 1, " tau == bound:", t == N // 2 + 1)
host_bound_check(H, n, t, "complete(10,6)", mmax=0)

# (B) C_9
n = 9
H = [bits([(i + 2 * a) % 9 for a in range(4)]) for i in range(9)]
print("(B) C_9 family: (7,2):", is_72(H, n), " tau:", tau(H, n))
t = tau(H, n)
cps = critical_sets(H, n, t)
print("  number of critical pairs:", len(cps))
prof = set()
for (E, B) in cps:
    U = E | B
    row = tuple((tau(light(H, U, m), n), tau(heavy(H, U, m), n)) for m in range(4))
    prof.add(row)
print("  profiles {(tau(H^(m)_U), tau(K_m)) for m=0..3}:", prof)
host_bound_check(H, n, t, "C_9", mmax=1)

# (C) core + private tails
r, Ncore, s = 4, 6, 2
cores = list(itertools.combinations(range(Ncore), r))
n = Ncore + s * len(cores)
H = []
for idx, A in enumerate(cores):
    tail = [Ncore + s * idx + a for a in range(s)]
    H.append(bits(list(A) + tail))
k = r + s
print("(C) core+tails: r=%d N=%d s=%d k=%d n=%d edges=%d" % (r, Ncore, s, k, n, len(H)))
print("  is (7,2):", is_72(H, n))
t = tau(H, n); print("  tau =", t, " (N-r+1 =", Ncore - r + 1, ")")
# criticality: B_A = core \ A works for each edge
crit_ok = all(all((F & bits([v for v in range(Ncore) if not (E >> v) & 1])) for F in H if F != E) for E in H)
print("  every edge critical via B = core minus its core part:", crit_ok)
prof = set()
for E in H:
    B = bits([v for v in range(Ncore) if not (E >> v) & 1])
    U = E | B
    prof.add(tuple(tau(heavy(H, U, m), n) for m in range(s + 1)))
print("  tau(K_m) for m=0..s at these critical pairs:", prof, " (t-1 =", t - 1, ")")
