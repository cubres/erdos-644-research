"""Referee w9, heavyparts#0, part B (exact, Fractions).
One type per class, 3 classes, each type super-heavy (>2x/3) at its class part; optional extra parts.
For every random family: brute force all 3^7 row assignments against Lemma 7.63 (primal form, independent code).
 (1) pencil-only feasibility  ==  'no mutual/cyclic conflict'   (the claim)   -- must agree 100%
 (2) full feasibility (rows, lines, totals) vs corrected criterion via (pattern set, counts) table
 (3) collect families with NO conflict but NO Fano tuple (totals obstruction), with exact tau*.
usage: python3 w9_ref_heavyparts0brk_random.py SEED N [extra_parts]"""
import sys, random, itertools
from fractions import Fraction as Fr
from w9_ref_heavyparts0brk_arccsp import LINES, PATSETS, minimal_hitting
MH = [set(F) for F in minimal_hitting()]
CL = 'ABC'

def forbidden(x, T):
    F = set()
    for trip in itertools.combinations_with_replacement(range(3), 3):
        if len(set(trip)) == 1: continue
        if any(sum(T[c][i] for c in trip) > 2*x[i] for i in range(len(x))):
            F.add(''.join(sorted(CL[c] for c in trip)))
    return F

def feas(x, T, totals=True):
    p = len(x)
    for asg in itertools.product(range(3), repeat=7):
        ok = True
        for i in range(p):
            z = [T[c][i] for c in asg]
            if max(z) > x[i] or (totals and sum(z) > 4*x[i]) or any(sum(z[q] for q in L) > 2*x[i] for L in LINES):
                ok = False; break
        if ok: return asg
    return None

def corrected(x, T):
    Fb = forbidden(x, T)
    for ps, cnts in PATSETS.items():
        if ps & Fb: continue
        for n in cnts:
            if all(sum(n[c]*T[c][i] for c in range(3)) <= 4*x[i] for i in range(len(x))): return True
    return False

def tau_star(x, T):
    p = len(x); best = None
    # FIX (entry 1): a type can only be blocked at a part where its trace is POSITIVE (u_i < a_i, u_i >= 0)
    for pi in itertools.product(*[[i for i in range(p) if a[i] > 0] for a in T]):
        t = [Fr(0)]*p
        for a, i in zip(T, pi): t[i] = max(t[i], x[i]-a[i])
        s = sum(t); best = s if best is None or s < best else best
    return best

def rand_family(rng, p, D=120):
    while True:
        x = [Fr(rng.randint(D//3, 2*D), D) for _ in range(p)]
        T = []
        for c in range(3):
            lo = 2*x[c]/3
            if lo >= 1 or lo >= x[c]: break
            hi = min(x[c], Fr(1))
            # super-heavy trace at own part
            a_c = lo + (hi-lo)*Fr(rng.randint(1, D), D)
            rest = 1 - a_c
            a = [Fr(0)]*p; a[c] = a_c
            others = [i for i in range(p) if i != c]
            w = [rng.random()**2 for _ in others]; s = sum(w) or 1
            for i, wi in zip(others, w): a[i] = min(x[i], Fr(round(D*rest*wi/s)), rest-sum(a[j] for j in others))
            a[c] += 1 - sum(a) if a[c] + 1 - sum(a) <= x[c] else 0
            if sum(a) != 1 or any(v < 0 or v > x[i] for i, v in enumerate(a)): break
            T.append(a)
        if len(T) == 3: return x, T

if __name__ == '__main__':
    seed, N = int(sys.argv[1]), int(sys.argv[2]); extra = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    rng = random.Random(seed); p = 3 + extra
    stats = dict(n=0, conflict=0, pencil_ok=0, full_ok=0, mism1=0, mism2=0, totals_killed=0)
    ex = []
    for _ in range(N):
        x, T = rand_family(rng, p)
        Fb = forbidden(x, T); conf = any(F <= Fb for F in MH)
        pen = feas(x, T, totals=False) is not None
        full = feas(x, T, totals=True) is not None
        stats['n'] += 1; stats['conflict'] += conf; stats['pencil_ok'] += pen; stats['full_ok'] += full
        if pen == conf: stats['mism1'] += 1; print('MISMATCH(claim pencil-level)', x, T, Fb)
        if corrected(x, T) != full: stats['mism2'] += 1; print('MISMATCH(corrected)', x, T)
        if not conf and not full:
            stats['totals_killed'] += 1
            ts = tau_star(x, T); ex.append((ts, x, T, sorted(Fb)))
    print(stats)
    ex.sort(key=lambda z: -z[0])
    for ts, x, T, Fb in ex[:5]:
        print('TOTALS-KILLED tau*=%s (%.4f) x=%s T=%s forbidden=%s' % (ts, float(ts), [str(v) for v in x],
              [[str(v) for v in a] for a in T], Fb))
