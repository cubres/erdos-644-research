"""balanced3proof library: 3-part continuous type-closed model (rank 1), rigid finite type sets."""
import sys, itertools, numpy as np
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import heavylib as h, pairlib as P
tau_star = h.tau_star_fast
def classes(x, T):
    """S[i] = indices of types super-heavy (>2x/3) at i"""
    return [[j for j, a in enumerate(T) if 3*a[i] > 2*x[i]] for i in range(len(x))]
def regime(x, T):
    S = classes(x, T); p = len(x)
    if any(not any(j in S[i] for i in range(p)) for j in range(len(T))): return None  # pencil lemma applies
    if any(len(S[i]) == 0 for i in range(p)): return None
    sig = [min(T[j][i] for j in S[i]) for i in range(p)]
    e = [x[i]-sig[i] for i in range(p)]
    return S, sig, e
def v_margin(x, T):
    """max over ordered pairs (s five rows, t two rows) of min_i normalised slack of max(s+t,5s/4+t/2)<=x"""
    x = np.asarray(x, float); T = np.asarray(T, float)
    S = T[:, None, :]; U = T[None, :, :]
    m = np.minimum((x - S - U)/x, (x - 1.25*S - 0.5*U)/x).min(axis=2)
    k = np.unravel_index(m.argmax(), m.shape); return float(m[k]), k
def t_margin(x, T):
    """T(a,b,c): a on the 4 quad lines, b on 2 pencil lines, c on 1: 2a+b,2a+c,2b+c<=2x, 4a+2b+c<=4x"""
    x = np.asarray(x, float); T = np.asarray(T, float)
    A = T[:, None, None, :]; B = T[None, :, None, :]; G = T[None, None, :, :]
    m = np.minimum(np.minimum((2*x-2*A-B)/x, (2*x-2*A-G)/x), np.minimum((2*x-2*B-G)/x, (4*x-4*A-2*B-G)/x/2)).min(axis=3)
    k = np.unravel_index(m.argmax(), m.shape); return float(m[k]), k
def fano_margin(x, T):
    return h.fano_margin(x, T)
def pair_margin(x, T):
    return P.pair_margin(x, T)
