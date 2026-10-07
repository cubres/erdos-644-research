#!/usr/bin/env python3
"""w7_ref_denseTwoPart_check.py -- referee test of the ANCHORED TWO-PART THEOREM (continuous model).
Random hill-climb over intersecting integer type sets containing the anchor (e,0); for every visited state with
4 tau* > 3R (tau* computed independently by sup_free, cross-checked with the beta formula) we
  (1) recompute g*, a'', g'' from the definitions, check g'' in G, Claims A,B,C, Case facts;
  (2) build the explicit template realisation and verify it exactly (Fractions);
  (3) check Lemma 7.63 inequalities with explicit Fano pencils;
  (4) for a sample, integerise and brute-force the Venn badness of the actual 7 sets.
Also records the non-intersecting control: same climb without the intersecting constraint (to see whether the
conclusion fails without it) -- mode 'nonint'.
Usage: seed R steps restarts mode(int|nonint)"""
import sys, random
from fractions import Fraction as Fr
from math import lcm
from w7_ref_denseTwoPart_lib import *

seed, R, steps, restarts = (int(v) for v in sys.argv[1:5]); mode = sys.argv[5]
random.seed(seed)

def fast_tau(G, e, x):
    v = tau_star_fixed(G, e, x)
    return -1 if v is None else v

def rand_type(e, x):
    a = random.randint(1, e)
    bmax = min(x, R - a)
    if bmax < 0: return None
    if random.random() < 0.6: b = bmax
    else: b = random.randint(0, bmax)
    return (a, b)

stats = dict(visited=0, qualifying=0, case1=0, case2=0, formula_mismatch=0, gpp_not_type=0, claimA=0, claimB=0,
             claimC=0, xgt=0, template_fail=0, fano_fail=0, brute_fail=0, brute_checked=0, no_gstar=0, fixed_mismatch=0, claim_formula_mismatch_qual=0)
seen = set()
best_nonint = None

def test_state(G, e, x):
    global best_nonint
    key = (e, x, tuple(sorted(G)))
    if key in seen: return
    seen.add(key)
    if mode == 'int' and not intersecting(G, e, x): return
    ts = tau_star(G, e, x)
    if ts != fast_tau(G, e, x):
        stats['fixed_mismatch'] += 1; print('FIXED FORMULA MISMATCH', e, x, sorted(G), ts, fast_tau(G, e, x), flush=True)
    if ts != tau_star_beta(G, e, x):
        stats['formula_mismatch'] += 1
        if 4 * ts > 3 * R: stats['claim_formula_mismatch_qual'] += 1; print('CLAIM FORMULA MISMATCH (qualifying)', mode, e, x, sorted(G), ts, tau_star_beta(G, e, x), flush=True)
    if 4 * ts <= 3 * R: return
    stats['qualifying'] += 1
    small = [g for g in G if 2 * g[0] <= e]
    if not small:
        stats['no_gstar'] += 1; print('NO g*', e, x, sorted(G), flush=True); return
    bstar = min(g[1] for g in small); gstar = min(g for g in small if g[1] == bstar)
    if 3 * bstar <= 2 * x:
        stats['case1'] += 1; case = 1; gpp = None
    else:
        stats['case2'] += 1; case = 2
        # x > 9R/4 - 3e/2 (normalised x > 9/4-3e/2)
        if not (4 * x > 9 * R - 6 * e and 4 * x > 3 * R): stats['xgt'] += 1; print('x-bound FAIL', e, x, sorted(G), flush=True)
        app = min(g[0] for g in G if g[1] < bstar)
        bpp = beta(G, app); gpp = (app, bpp)
        if gpp not in G: stats['gpp_not_type'] += 1; print('g\'\' not a type', e, x, sorted(G), gpp, flush=True)
        if not (gstar[0] + app <= e): stats['claimA'] += 1; print('A FAIL', e, x, sorted(G), gstar, gpp, flush=True)
        if not (3 * app <= 2 * e): stats['claimB'] += 1; print('B FAIL', e, x, sorted(G), gstar, gpp, flush=True)
        if not (2 * bstar + bpp < 2 * x and 3 * bpp < 2 * x): stats['claimC'] += 1; print('C FAIL', e, x, sorted(G), gstar, gpp, flush=True)
    rows, m0, m1 = explicit_realisation(e, x, gstar, gpp, case)
    f = verify_realisation(rows, m0, m1, e, x)
    if f:
        stats['template_fail'] += 1; print('TEMPLATE FAIL', mode, e, x, sorted(G), gstar, gpp, f, flush=True)
        if mode == 'nonint':
            if best_nonint is None or ts > best_nonint[0]: best_nonint = (ts, e, x, sorted(G))
        return
    if not fano_ok(rows, (e, x)):
        stats['fano_fail'] += 1; print('FANO(7.63) FAIL but explicit OK?!', e, x, sorted(G), flush=True)
    if stats['brute_checked'] < 400 and random.random() < 0.3:
        den = 4
        verts, sets = integerise(rows, m0, m1, den)
        prof_ok = all(sum(1 for v in sets[i] if v[0] == 0) == den * rows[i][0] and
                      sum(1 for v in sets[i] if v[0] == 1) == den * rows[i][1] for i in range(7))
        stats['brute_checked'] += 1
        if not (prof_ok and brute_bad(verts, sets)):
            stats['brute_fail'] += 1; print('BRUTE FAIL', e, x, sorted(G), flush=True)

for rs in range(restarts):
    e = random.randint((3 * R) // 4 + 1, R)
    x = random.randint(R // 2, 2 * R)
    G = {(e, 0)}
    cur = fast_tau(G, e, x)
    for st in range(steps):
        H = set(G)
        mv = random.random()
        if mv < 0.55 or len(H) == 1:
            g = rand_type(e, x)
            if g is None: continue
            H.add(g)
        elif mv < 0.85:
            H.discard(random.choice([g for g in H if g != (e, 0)]))
        else:
            g = random.choice([g for g in H if g != (e, 0)]) if len(H) > 1 else None
            if g is None: continue
            H.discard(g); a, b = g
            a2 = min(e, max(1, a + random.randint(-2, 2))); b2 = min(x, R - a2, max(0, b + random.randint(-2, 2)))
            if b2 < 0: continue
            H.add((a2, b2))
        if mode == 'int' and not intersecting(H, e, x): continue
        new = fast_tau(H, e, x)
        if new >= cur or random.random() < 0.05:
            G, cur = H, new
            stats['visited'] += 1
            if 4 * cur > 3 * R or random.random() < 0.02:
                test_state(G, e, x)
        if random.random() < 0.01:
            x = min(2 * R, max(1, x + random.choice([-1, 1])))
            if mode == 'int' and not intersecting(G, e, x): x -= 0  # keep; next steps will repair
            cur = fast_tau(G, e, x)
print(mode, 'R', R, stats, flush=True)
if mode == 'nonint': print('best nonint template failure (tau*,e,x,G):', best_nonint)
