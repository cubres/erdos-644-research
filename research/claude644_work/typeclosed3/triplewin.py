"""Part A numerics: triple windows.  A window (box of cost 3/4) contains types of all three super-heavy classes iff
some triple (a,b,c) in S_1 x S_2 x S_3 has |a v b v c| <= N - 3/4 (join = componentwise max).
Also: boundary 'vertex labels' of the covering of T_{3/4} (which classes cover u = (3/4) e_i) and the KKM-type
degree of the boundary covering (computed on a fine subdivision of the boundary of T_{3/4}).
Usage: python3 triplewin.py            (7.79 family + the strategy agent's adversaries if present)
"""
import json, sys, itertools, glob
from fractions import Fraction as Fr
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3')
from tc3lib import tau_star, fano_search, v_search


def classes(K, x):
    return [[k for k, c in enumerate(K) if 3 * c[i] > 2 * x[i]] for i in range(3)]


def triple_window(K, x):
    """min over class triples of |join| - (N - 3/4); <= 0 means a triple window exists. returns (val, triple)"""
    S = classes(K, x)
    N = sum(x)
    best = None
    for a in S[0]:
        for b in S[1]:
            for c in S[2]:
                j = sum(max(K[a][i], K[b][i], K[c][i]) for i in range(3))
                v = j - (N - Fr(3, 4))
                if best is None or v < best[0]:
                    best = (v, (a, b, c))
    return best


def covering_labels(K, x, s=Fr(3, 4), n=240):
    """labels along the boundary of T_s = {u>=0, |u|=s, u<=x} (assumes x_i >= s; else truncated -> reported).
    returns list of (point, set of classes covering it) and the degree of the nerve map."""
    S = classes(K, x)
    N = sum(x)
    if any(xi < s for xi in x):
        return None
    verts = [tuple(s if j == i else 0 for j in range(3)) for i in range(3)]
    # boundary: v0 -> v1 -> v2 -> v0
    pts = []
    for e in range(3):
        p, q = verts[e], verts[(e + 1) % 3]
        for k in range(n):
            t = Fr(k, n)
            pts.append(tuple(p[j] + (q[j] - p[j]) * t for j in range(3)))
    labs = []
    for u in pts:
        w = tuple(x[j] - u[j] for j in range(3))
        L = set()
        for i in range(3):
            if any(all(K[k][j] <= w[j] for j in range(3)) for k in S[i]):
                L.add(i)
        labs.append(L)
    # degree: forward transitions 0->1, 1->2, 2->0 count +1, backward -1, over a chosen single label per point
    # choose labels greedily to keep continuity (if the previous label is still available keep it)
    chosen = []
    cur = None
    for L in labs:
        if not L:
            return labs, None
        if cur in L:
            chosen.append(cur)
        else:
            cur = min(L)
            chosen.append(cur)
    tot = 0
    for k in range(len(chosen)):
        a, b = chosen[k], chosen[(k + 1) % len(chosen)]
        if b == (a + 1) % 3:
            tot += 1
        elif a == (b + 1) % 3:
            tot -= 1
    return labs, Fr(tot, 3)


def report(name, K, x):
    N = sum(x)
    tau = tau_star(K, x)
    S = classes(K, x)
    tw = triple_window(K, x)
    print('==', name, 'x =', [str(v) for v in x], 'N =', float(N), 'tau* =', float(tau), 'G =', float(N - Fr(7, 4)))
    print('   classes', S, ' multi-class types:', [k for k in range(len(K)) if sum(k in Si for Si in S) > 1])
    print('   triple-window value min|join|-(N-3/4) = %.4f  (<=0: triple window exists) triple %s' % (float(tw[0]), tw[1]))
    cl = covering_labels(K, x)
    if cl is None:
        print('   boundary: truncated (some x_i < 3/4)')
    else:
        labs, deg = cl
        n = len(labs) // 3
        print('   vertex labels: v0', labs[0], 'v1', labs[n], 'v2', labs[2 * n], ' degree', deg)
        # compress label word along boundary
        word = []
        for L in labs:
            key = tuple(sorted(L))
            if not word or word[-1] != key:
                word.append(key)
        print('   boundary label word (compressed):', word)
    return tw


if __name__ == '__main__':
    d = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_three_part_two_type_barrier.json'))
    K = [tuple(Fr(v, 80) for v in t) for t in d['types']]
    x = [Fr(513, 640)] * 3
    report('7.79 family', K, x)
    for fn in sorted(glob.glob('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/adv_*.json')):
        try:
            a = json.load(open(fn))
        except Exception as e:
            continue
        if 'x' in a and ('roles' in a or 'types' in a or 'K' in a):
            xs = [Fr(v).limit_denominator(10 ** 6) for v in a['x']]
            T = a.get('types') or a.get('K') or a.get('roles')
            if isinstance(T, dict):
                T = list(T.values())
            try:
                Ks = [tuple(Fr(v).limit_denominator(10 ** 6) for v in t) for t in T]
            except Exception:
                continue
            report(fn.split('/')[-1], Ks, xs)
