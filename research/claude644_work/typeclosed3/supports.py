"""Full bad-support catalogue for seven rows (all 715 non-dictator orbits of maximal intersecting families on [7],
i.e. self-dual monotone Boolean functions of 7 variables up to S_7), with the EXACT vertex list of every dual
polytope P_D = {w >= 0 : w(C) <= 1 for every maximal cell C}.  Capacity function M_D(z) = max_v v.z (Lemma 7.63 /
Theorem 7.69 mechanism): seven row loads z (one part) are realisable on support D within capacity x iff M_D(z) <= x.

Cells are subsets of [7] (row sets of a vertex); a support D is the downset of the complements of a maximal
intersecting family F; maximal cells = complements of the minimal members of F.
Output: supports715.json  {orbits: [{minimal_F, maximal_cells, orbit_size, vertices (fractions as strings)}], counts}.
Vertices: Qhull (scipy HalfspaceIntersection) + rationalisation + exact verification (tight constraints of rank 7,
feasibility) + an LP cross-check of M_D on random loads.
"""
import itertools, json, sys, time
from fractions import Fraction as Fr
import numpy as np

HERE = '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/typeclosed3/'
FULL = 127


def popcount(a):
    return bin(a).count('1')


def enumerate_selfdual():
    """all maximal intersecting families on [7] as 64-bit masks over the 'small' sets (|A| <= 3), bit index = position
    of A in SMALL."""
    small = sorted([a for a in range(128) if popcount(a) <= 3], key=lambda a: (popcount(a), a))
    pos = {a: i for i, a in enumerate(small)}
    up = [0] * 128
    down = [0] * 128
    for a in range(128):
        for b in range(128):
            if a & b == a:
                up[a] |= 1 << b
            if a & b == b:
                down[a] |= 1 << b
    comp = [0] * 128
    # comp(mask over sets) -> mask over complements
    def compmask(m):
        r = 0
        while m:
            b = m & -m
            i = b.bit_length() - 1
            r |= 1 << (FULL ^ i)
            m ^= b
        return r
    upc = [compmask(up[a]) for a in range(128)]
    downc = [compmask(down[a]) for a in range(128)]
    out = []
    n = len(small)

    def rec(k, inm, outm):
        if k == n:
            out.append(inm)
            return
        a = small[k]
        bit = 1 << a
        if inm & bit:
            rec(k + 1, inm, outm)
            return
        if outm & bit:
            rec(k + 1, inm, outm)
            return
        # option in
        ni = inm | up[a]
        no = outm | upc[a]
        if ni & no == 0:
            rec(k + 1, ni, no)
        # option out
        no2 = outm | down[a]
        ni2 = inm | downc[a]
        if ni2 & no2 == 0:
            rec(k + 1, ni2, no2)

    rec(0, 0, 0)
    return small, pos, out


def minimal_members(inm):
    mem = [a for a in range(1, 128) if inm >> a & 1]
    return [a for a in mem if not any(b != a and a & b == b for b in mem)]


def orbits(small, pos, fams):
    perms = list(itertools.permutations(range(7)))
    smallidx = np.zeros((len(perms), len(small)), dtype=np.int64)
    for pi, p in enumerate(perms):
        for j, a in enumerate(small):
            b = 0
            for i in range(7):
                if a >> i & 1:
                    b |= 1 << p[i]
            smallidx[pi, j] = pos[b]
    # represent each family by its 64-bit small mask
    def smallmask(inm):
        m = 0
        for j, a in enumerate(small):
            if inm >> a & 1:
                m |= 1 << j
        return m
    fam_by_small = {}
    for inm in fams:
        fam_by_small[smallmask(inm)] = inm
    unseen = set(fam_by_small)
    reps = []
    one = np.uint64(1)
    while unseen:
        rep = min(unseen)
        idx = [j for j in range(len(small)) if rep >> j & 1]
        imgs = np.zeros(len(perms), dtype=np.uint64)
        for j in idx:
            imgs |= one << smallidx[:, j].astype(np.uint64)
        imgs = set(int(v) for v in imgs)
        assert imgs <= set(fam_by_small)
        unseen.difference_update(imgs)
        reps.append((fam_by_small[rep], len(imgs)))
    return reps


def vertices_exact(maxcells):
    from scipy.spatial import HalfspaceIntersection
    from scipy.optimize import linprog
    rows = []
    for c in maxcells:
        v = [1.0 if c >> j & 1 else 0.0 for j in range(7)] + [-1.0]
        rows.append(v)
    for j in range(7):
        v = [0.0] * 8
        v[j] = -1.0
        rows.append(v)
    hs = np.array(rows)
    interior = np.full(7, 1.0 / 16)
    hi = HalfspaceIntersection(hs, interior)
    verts = set()
    for p in hi.intersections:
        q = tuple(Fr(float(v)).limit_denominator(200) for v in p)
        verts.add(q)
    # exact verification
    A = [[Fr(1) if c >> j & 1 else Fr(0) for j in range(7)] for c in maxcells]
    good = []
    for q in verts:
        if any(v < 0 for v in q):
            continue
        if any(sum(a[j] * q[j] for j in range(7)) > 1 for a in A):
            continue
        tight = [a for a in A if sum(a[j] * q[j] for j in range(7)) == 1]
        tight += [[Fr(1) if k == j else Fr(0) for k in range(7)] for j in range(7) if q[j] == 0]
        if rank(tight) == 7:
            good.append(q)
    # LP cross-check of the capacity function on random loads
    rng = np.random.default_rng(0)
    Af = np.array([[1.0 if c >> j & 1 else 0.0 for j in range(7)] for c in maxcells])
    for _ in range(5):
        z = rng.random(7)
        # min 1.m s.t. Af^T m >= z, m >= 0
        res = linprog(np.ones(len(maxcells)), A_ub=-Af.T, b_ub=-z, bounds=[(0, None)] * len(maxcells), method='highs')
        lp = res.fun
        mv = max(sum(float(q[j]) * z[j] for j in range(7)) for q in good)
        assert abs(lp - mv) < 1e-7, (lp, mv)
    return sorted(good)


def rank(vs):
    m = [list(v) for v in vs]
    r = 0
    cols = len(m[0]) if m else 0
    for c in range(cols):
        piv = None
        for i in range(r, len(m)):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [m[i][k] - f * m[r][k] for k in range(cols)]
        r += 1
    return r


def main():
    t0 = time.time()
    small, pos, fams = enumerate_selfdual()
    print('labelled self-dual monotone families:', len(fams), 'time', round(time.time() - t0, 1), flush=True)
    reps = orbits(small, pos, fams)
    print('orbits:', len(reps), 'time', round(time.time() - t0, 1), flush=True)
    out = []
    for inm, osz in reps:
        mins = minimal_members(inm)
        maxcells = [FULL ^ a for a in mins]
        if any(popcount(a) == 1 for a in mins):
            # dictator: some row gets no vertex at all (all cells avoid it) -> unusable
            out.append({'minimal_F': mins, 'maximal_cells': maxcells, 'orbit_size': osz, 'dictator': True, 'vertices': []})
            continue
        vs = vertices_exact(maxcells)
        out.append({'minimal_F': mins, 'maximal_cells': maxcells, 'orbit_size': osz, 'dictator': False,
                    'vertices': [[str(v) for v in q] for q in vs]})
    nd = [o for o in out if not o['dictator']]
    print('non-dictator orbits:', len(nd), 'labelled', sum(o['orbit_size'] for o in nd),
          'max cell sizes:', sorted(set(max(popcount(c) for c in o['maximal_cells']) for o in nd)),
          'time', round(time.time() - t0, 1), flush=True)
    json.dump({'orbits': out, 'labelled_total': len(fams)}, open(HERE + 'supports715.json', 'w'))


if __name__ == '__main__':
    main()
