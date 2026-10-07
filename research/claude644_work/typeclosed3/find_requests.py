"""Given an adversary configuration (roles3 JSON), find REQUESTS that would complete a template:
 (a) Fano with 6 actual points (valid roles) and 1 requested point (point 0 w.l.o.g.): requested row d must satisfy,
     per part, d <= 2x - (r+r') on each of the 3 lines through point 0 and d <= 4x - sum(6 actual); cost = |x - u|.
 (b) Fano with 5 actual + 2 requested points (points 0 and 1, on line (0,1,2) with actual point 2): budgets split
     equally on the common line and on the total.
 (c) MP: 3 actual on a line (b,b,c) + 4 requested (cost 3/4 + sum (c-2b)^+/4, condition 2b + c <= 2x).
A request is useful iff its cost < tau (then an answer exists and the template is feasible for ANY answer).
Output: sorted list of (cost, kind, roles at the actual points), and role dicts (roles3 'ureq' format) for the best ones.
"""
import sys, json, itertools
import numpy as np
from roles3 import LINES, PATS, ureq, R

PEN = [[l for l in LINES if q in l] for q in range(7)]


def cfg(sol):
    x = np.array(sol['x']); tau = sol['tau']; Rl = np.array(sol['roles'])
    valid = [q is None or q == 1 for q in sol['Q']]
    return x, tau, Rl, valid


def req_from_points(x, Rl, pts):
    """pts: dict point -> role index for the 6 actual points (point 0 requested). returns (u, cost, ok)"""
    u = x.copy(); ok = True
    for l in PEN[0]:
        others = [q for q in l if q != 0]
        s = Rl[pts[others[0]]] + Rl[pts[others[1]]]
        u = np.minimum(u, 2 * x - s)
    tot = sum(Rl[pts[q]] for q in range(1, 7))
    u = np.minimum(u, 4 * x - tot)
    # lines not through 0 must be feasible among actual rows
    for l in LINES:
        if 0 in l: continue
        if np.any(sum(Rl[pts[q]] for q in l) > 2 * x * (1 + 1e-9)): ok = False
    u = np.maximum(u, 0)
    return u, float((x - u).sum()), ok


def req_role_6plus1(pts):
    """roles3 'ureq' role for the request of req_from_points (linear exprs in role coordinates)"""
    u = []
    for i in range(3):
        ex = []
        for l in PEN[0]:
            others = [q for q in l if q != 0]
            d = {'x%d' % i: 2}
            for q in others:
                k = R(pts[q], i); d[k] = d.get(k, 0) - 1
            ex.append(d)
        d = {'x%d' % i: 4}
        for q in range(1, 7):
            k = R(pts[q], i); d[k] = d.get(k, 0) - 1
        ex.append(d)
        u.append(ex)
    return ureq(u, tag='6+1', pts=[pts[q] for q in range(1, 7)])


def search(sol, maxk=3, top=15):
    x, tau, Rl, valid = cfg(sol)
    n = len(Rl)
    groups = {}
    for j in range(n):
        if valid[j]: groups.setdefault(tuple(np.round(Rl[j], 6)), []).append(j)
    reps = [g[0] for g in groups.values()]
    found = []
    # (a) 6 actual + 1 requested: enumerate assignments of reps to points 1..6 with <= maxk distinct
    seen = set()
    for k in range(1, maxk + 1):
        for combo in itertools.combinations(reps, k):
            for pat in itertools.product(range(k), repeat=6):
                if len(set(pat)) != k: continue
                pts = {q + 1: combo[pat[q]] for q in range(6)}
                u, cost, ok = req_from_points(x, Rl, pts)
                if ok and cost < tau:
                    key = tuple(pts[q] for q in range(1, 7))
                    if key in seen: continue
                    seen.add(key)
                    found.append((cost, '6+1', key))
    # (c) MP(b, c): 2b + c <= 2x, cost 3/4 + sum (c - 2b)^+ / 4
    for b in reps:
        for c in reps:
            if b == c: continue
            if np.all(2 * Rl[b] + Rl[c] <= 2 * x * (1 + 1e-9)):
                cost = 0.75 + np.maximum(Rl[c] - 2 * Rl[b], 0).sum() / 4
                if cost < tau: found.append((cost, 'MP', (b, c)))
    found.sort(key=lambda r: r[0])
    return found[:top], found


if __name__ == '__main__':
    sol = json.load(open(sys.argv[1]))
    best, allf = search(sol)
    print('useful requests found:', len(allf))
    for cost, kind, key in best:
        print(' cost %.4f %s roles %s' % (cost, kind, key))
