"""Lemma IRR attempt (one light part L): intersecting, all types super-heavy at A or B, light at L, G: d_A+d_B>3/4.
Types: alpha (A-min), beta (B-min), a (A-type maximising the A-gap among L-trace <= lam*), b (same for B),
lam* = x_L - max(alpha_L, beta_L).  Maps: heavy (d_A+d_B) and L-block (F_A+F_B+max(alpha_L,beta_L)).
For each overlap pattern of the 4 A-B pairs (A, B or L) and each ordering of alpha_L, beta_L: LP maximise
the min of the two map costs.  Also the no-helper cases.  If every LP value <= 3/4 the lemma holds."""
import itertools, numpy as np
from scipy.optimize import linprog
V = ['xA','xB','xL','alA','alB','alL','beA','beB','beL','aA','aB','aL','bA','bB','bL','t']
ix = {v: i for i, v in enumerate(V)}; n = len(V); EPS = 1e-7
def row(d):
    r = np.zeros(n)
    for k, c in d.items(): r[ix[k]] += c
    return r
def solve(pattern, order, helpA, helpB):
    A = []; b = []
    def le(d, c=0.0): A.append(row(d)); b.append(c)          # sum d <= c
    # fit and nonneg
    for T in ['al','be','a','b']:
        for P in 'ABL':
            le({T+P: 1, 'x'+P: -1}); le({T+P: -1})
        le({T+'A': 1, T+'B': 1, T+'L': 1}, 1.0)
    # super-heavy: 3 alA > 2 xA  ; a_A >= alA (alpha is the minimiser); same for B
    le({'xA': 2, 'alA': -3}, -EPS); le({'xB': 2, 'beB': -3}, -EPS)
    le({'alA': 1, 'aA': -1}); le({'beB': 1, 'bB': -1})
    # light
    for T in ['al','a']: le({T+'B': 7, 'xB': -4}); le({T+'L': 7, 'xL': -4})
    for T in ['be','b']: le({T+'A': 7, 'xA': -4}); le({T+'L': 7, 'xL': -4})
    # t <= heavy map ; t <= L-block map
    le({'t': 1, 'xA': -1, 'alA': 1, 'xB': -1, 'beB': 1})
    big = 'alL' if order == 0 else 'beL'
    if order == 0: le({'beL': 1, 'alL': -1})
    else: le({'alL': 1, 'beL': -1})
    d = {'t': 1, big: -1}
    if helpA: d.update({'xA': -1, 'aA': 1})
    if helpB: d.update({'xB': -1, 'bB': 1})
    le(d)
    # helpers have L-trace <= lam* = xL - big
    if helpA: le({'aL': 1, 'xL': -1, big: 1})
    if helpB: le({'bL': 1, 'xL': -1, big: 1})
    # overlaps: pairs (alpha,beta),(alpha,b),(a,beta),(a,b); pattern entry in 'ABL'
    pairs = [('al','be'), ('al','b'), ('a','be'), ('a','b')]
    for (u, w), P in zip(pairs, pattern):
        if (u == 'a' and not helpA) or (w == 'b' and not helpB): continue
        le({u+P: -1, w+P: -1, 'x'+P: 1}, -EPS)       # u_P + w_P > x_P
    c = np.zeros(n); c[ix['t']] = -1
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, 5)]*n, method='highs')
    return (-res.fun, res.x) if res.status == 0 else (None, None)
best = (-1,)
for helpA, helpB in [(1,1),(1,0),(0,1),(0,0)]:
    for order in (0, 1):
        for pattern in itertools.product('ABL', repeat=4):
            v, sol = solve(pattern, order, helpA, helpB)
            if v is not None and v > best[0]: best = (v, pattern, order, helpA, helpB, sol)
print("max over cases of min(heavy, L-block):", best[0], best[1:5])
sol = best[5]; print({k: round(sol[ix[k]], 4) for k in V})
