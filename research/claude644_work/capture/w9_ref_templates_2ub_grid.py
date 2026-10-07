# Referee w9, claim templates#1 (Theorem 2UB): EXHAUSTIVE exact grid check (integer arithmetic, numpy int64).
# All values are integers in units 1/D.  For every sorted capacity vector X (1..XMAX each), every pair of
# generators G,H (0<=G_i<=min(X_i,D), |G|<=D) with tau*(U(G) u U(H)) >= 3/4 (K0,K1',K2', equality allowed)
# and both generators heavy somewhere, and EVERY heavy pair (I,J), check: I!=J, admissibility of the canonical
# a=G+(D-|G|)e_J, b=H+(D-|H|)e_I, and that one of Qb, Qa, V(a,b) fits (template formulas; the formulas are the
# exact masses of the explicit constructions verified cell-by-cell in w9_ref_templates_2ub.py).
# Also records the minimum slack of the best template (to see tightness) and the K/L pattern counts.
# usage: python3 w9_ref_templates_2ub_grid.py P D XMAX
import itertools, sys
import numpy as np

P, D, XMAX = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
INF = 10 ** 9

def gens(X):
    out = []
    for G in itertools.product(*[range(0, min(X[i], D) + 1) for i in range(P)]):
        if sum(G) <= D: out.append(G)
    return np.array(out, dtype=np.int64)

def main():
    total = 0; checked_pairs = 0; wins = {'Qb': 0, 'Qa': 0, 'V': 0}; eq = 0
    minslack = None; pattern = {}
    for X in itertools.combinations_with_replacement(range(1, XMAX + 1), P):
        X = np.array(X, dtype=np.int64); N = X.sum()
        if 4 * (N - D) < 3 * D: continue                     # K0
        A = gens(X)
        heavy = (7 * A > 4 * X)                              # m x P
        hv = heavy.any(axis=1)
        Gs = A[hv]; Hh = heavy[hv]
        if len(Gs) == 0: continue
        # c_i = X_i - G_i if G_i>0 else INF
        C = np.where(Gs > 0, X - Gs, INF)                    # m x P
        m = len(Gs)
        # pairwise over (g,h): K1' min_i (G_i,H_i>0) X_i - min(G_i,H_i); K2' min_{i!=j} C_g[i] + C_h[j]
        for gi in range(m):
            G = Gs[gi]; Cg = C[gi]
            both = (G > 0)[None, :] & (Gs > 0)                   # m x P
            k1 = np.where(both, X - np.minimum(G[None, :], Gs), INF).min(axis=1)
            S = Cg[:, None] + C[:, None, :]                      # m x P(i) x P(j)
            S = S.copy()
            idx = np.arange(P); S[:, idx, idx] = INF
            k2 = S.reshape(m, -1).min(axis=1)
            tau = np.minimum(np.minimum(k1, k2), N - D)
            ok = 4 * tau >= 3 * D
            for hi in np.nonzero(ok)[0]:
                H = Gs[hi]; total += 1
                if 4 * tau[hi] == 3 * D: eq += 1
                for I in np.nonzero(Hh[gi])[0]:
                    for J in np.nonzero(Hh[hi])[0]:
                        assert I != J, ('I==J', X, G, H)
                        a = G.copy(); a[J] += D - G.sum(); b = H.copy(); b[I] += D - H.sum()
                        assert (a <= X).all() and (b <= X).all(), ('adm', X, G, H, I, J)
                        # slacks x4
                        sQb = np.minimum(4 * X - 6 * b, 4 * X - 4 * a - 3 * b).min()
                        sQa = np.minimum(4 * X - 6 * a, 4 * X - 4 * b - 3 * a).min()
                        sV = np.minimum(4 * X - 4 * a - 4 * b, 4 * X - 5 * a - 2 * b).min()
                        best = max(sQb, sQa, sV)
                        assert best >= 0, ('NO TEMPLATE', X, G, H, I, J, a, b)
                        checked_pairs += 1
                        wins['Qb' if sQb >= 0 else 'Qa' if sQa >= 0 else 'V'] += 1
                        if minslack is None or best < minslack[0]: minslack = (best, X.tolist(), G.tolist(), H.tolist(), int(I), int(J))
                        if sQb < 0 and sQa < 0:
                            Ks = tuple(np.nonzero(2 * X < 3 * b)[0]); Ls = tuple(np.nonzero(2 * X < 3 * a)[0])
                            key = ('K=J' if J in Ks else 'K!=J', 'L=I' if I in Ls else 'L!=I')
                            pattern[key] = pattern.get(key, 0) + 1
    print('P', P, 'D', D, 'XMAX', XMAX, 'instances(tau*>=3/4, both heavy)', total, 'tau*=3/4 exactly', eq)
    print('heavy pairs checked', checked_pairs, wins)
    print('min best-template slack (x4/D units)', minslack)
    print('V-case K/L patterns', pattern)
    print('ALL CHECKS PASSED')

main()
