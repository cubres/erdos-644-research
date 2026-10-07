"""candidate canonical strategies in the balanced regime; each returns a margin (>=0 : strategy succeeds).
Types used: minimisers (unique assumed: argmin own trace, ties broken adversarially by taking the worst)."""
import itertools, numpy as np, b3lib as B
def mins_of(x, T):
    S, sig, e = B.regime(x, T)
    return S, sig, e, [[j for j in S[i] if abs(T[j][i]-sig[i]) < 1e-12] for i in range(3)]
def t_marg(x, a, b, c):
    x = np.asarray(x); a, b, c = map(np.asarray, (a, b, c))
    return min(((2*x-2*a-b)/x).min(), ((2*x-2*a-c)/x).min(), ((2*x-2*b-c)/x).min(), ((4*x-4*a-2*b-c)/x/2).min())
def v_marg(x, s, t):
    x = np.asarray(x); s, t = np.asarray(s), np.asarray(t)
    return min(((x-s-t)/x).min(), ((x-1.25*s-0.5*t)/x).min())
def mp_marg(x, tau, b, c):
    """mixed pencil (b,b,c) + requested quad: pencil 2b+c<=2x; cost 3/4+sum(c-2b)^+/4 < tau"""
    x = np.asarray(x); b, c = np.asarray(b), np.asarray(c)
    return min(((2*x-2*b-c)/x).min(), tau - 0.75 - np.maximum(c-2*b, 0).sum()/4)
def pt_marg(x, tau, p1, p2, p3):
    x = np.asarray(x); P = np.array([p1, p2, p3])
    ex = np.maximum(P.max(axis=0) - (P.sum(axis=0) - P.max(axis=0)), 0).sum()/4
    return min(((2*x - P.sum(axis=0))/x).min(), tau - 0.75 - ex)
def st1(x, T, tau=None):
    if tau is None: tau = B.tau_star(x, T)
    S, sig, e, mins = mins_of(x, T)
    worst = 1e9
    for al in itertools.product(*mins):
        M = [T[j] for j in al]; best = -1e9
        for X, Y, Z in itertools.permutations(range(3)):
            best = max(best, t_marg(x, M[X], M[Y], M[Z]))
        for Y, Z in itertools.permutations(range(3), 2):
            best = max(best, mp_marg(x, tau, M[Y], M[Z]))
        best = max(best, pt_marg(x, tau, *M))
        worst = min(worst, best)
    return worst

def best_over(x, tau, R, use=('T', 'V', 'MP', 'PT')):
    """best template margin using only the types in list R (vectors)"""
    best = -1e9; n = len(R)
    if 'T' in use:
        for a, b, c in itertools.product(range(n), repeat=3):
            best = max(best, t_marg(x, R[a], R[b], R[c]))
    if 'V' in use:
        for s, t in itertools.product(range(n), repeat=2):
            best = max(best, v_marg(x, R[s], R[t]))
    if 'MP' in use:
        for b, c in itertools.product(range(n), repeat=2):
            best = max(best, mp_marg(x, tau, R[b], R[c]))
    if 'PT' in use:
        for p in itertools.combinations_with_replacement(range(n), 3):
            best = max(best, pt_marg(x, tau, *[R[i] for i in p]))
    return best
def roles_vert(x, T, Tt=0.75):
    return [[j for j, a in enumerate(T) if a[z] <= x[z] - Tt + 1e-12] for z in range(3)]
def robust(x, T, tau, rolesets, use=('T', 'V', 'MP', 'PT'), cap=400):
    """min over selections (one type per role) of best template margin"""
    worst = 1e9; cnt = 0
    for sel in itertools.product(*rolesets):
        R = [T[j] for j in sorted(set(sel))]
        worst = min(worst, best_over(x, tau, R, use)); cnt += 1
        if cnt > cap: break
    return worst
def st2(x, T, tau=None):
    if tau is None: tau = B.tau_star(x, T)
    S, sig, e, mins = mins_of(x, T)
    return robust(x, T, tau, mins + roles_vert(x, T))
