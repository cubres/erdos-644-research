#!/usr/bin/env python3
"""w9_ref_dense3_red.py -- exact random tests of R1, R2, R3 and the M1 components (referee w9, dense#3).
Rank normalised to r (integer), caps integers, types with Fraction coordinates (half-integers).
For each random instance (anchor + random types, intersecting or not):
 R1: G_S (types vanishing on S, S projected away): tau*(G_S) >= tau*(G) - x(S); intersecting(G) => intersecting(G_S);
     any config found in G_S lifts (zeros on S) to a config of G.
 R2: types with b_s <= x_s/2, part s projected: tau* >= tau*(G) - x_s/2; intersecting preserved; configs lift.
     MUTATIONS: threshold 3/5 instead of 1/2 (intersecting / lifting should fail sometimes); loss x_s/3 (bound fails).
 R3: part with x_s >= 2r: projecting away keeps tau* (>=), intersecting preserved, configs lift.
 NOFANO: any 6 rows of rank <= r with anchor 0 on part s, x_s >= 3r/2: part s constraints hold; mutation x_s < 3r/2.
 M1c: G_h over (E0, X): intersecting(G) => intersecting(G_h); tau*(G_h) >= tau*(G); every config of G_h lifts.
Usage: python3 w9_ref_dense3_red.py SEED N"""
import sys, random
from fractions import Fraction as Fr
from w9_ref_dense3_lib import *

def rand_type(rnd, caps, r, e):
    p = len(caps)
    tot = Fr(rnd.randint(2, 2*r), 2)
    g = [Fr(0)]*p
    # random composition of tot among parts with caps, E0 part guaranteed positive mostly
    units = int(tot*2)
    order = list(range(p))
    for _ in range(units):
        i = rnd.choice(order) if rnd.random() < 0.7 else rnd.choice(order[:1] + order[1+rnd.randrange(p-1):][:1])
        if g[i] + Fr(1, 2) <= caps[i]: g[i] += Fr(1, 2)
    return tuple(g)

def proj(g, drop): return tuple(v for i, v in enumerate(g) if i not in drop)

def main():
    seed = int(sys.argv[1]); N = int(sys.argv[2])
    rnd = random.Random(seed)
    st = {k: 0 for k in ['inst', 'inter', 'R1', 'R1_tau_fail', 'R1_int_fail', 'R1_cfg', 'R1_lift_fail',
                         'R2', 'R2_tau_fail', 'R2_int_fail', 'R2_cfg', 'R2_lift_fail', 'R2mut_int_fail',
                         'R2mut_lift_fail', 'R2mut_cfg', 'R2loss3_fail', 'R3', 'R3_tau_fail', 'R3_int_fail',
                         'R3_cfg', 'R3_lift_fail', 'NF_fail', 'NFmut_fail',
                         'M1_tau_fail', 'M1_int_fail', 'M1_cfg', 'M1_lift_fail', 'M1_tau_gain']}
    for it in range(N):
        r = rnd.randint(4, 8)
        m = rnd.randint(1, 3)
        e = rnd.randint((3*r)//4, r)
        xs = [rnd.randint(1, 2*r + 2) for _ in range(m)]
        caps = [e] + xs
        anchor = tuple([Fr(e)] + [Fr(0)]*m)
        G = [anchor] + [rand_type(rnd, caps, r, e) for _ in range(rnd.randint(2, 7))]
        G = [g for g in G if sum(g) > 0]
        want_int = rnd.random() < 0.7
        if want_int:
            H = [anchor]
            for g in G[1:]:
                if intersecting(H + [g], caps): H.append(g)
            G = H
        st['inst'] += 1
        isint = intersecting(G, caps)
        st['inter'] += isint
        T = tau_star(G, caps)
        # ---- R1
        S = set(rnd.sample(range(1, m+1), rnd.randint(1, m))) if m >= 1 else set()
        GS = [proj(g, S) for g in G if all(g[i] == 0 for i in S)]
        capsS = proj(caps, S); anchS = proj(anchor, S)
        if len(capsS) >= 1:
            st['R1'] += 1
            TS = tau_star(GS, capsS)
            if TS < T - sum(caps[i] for i in S): st['R1_tau_fail'] += 1
            if isint and not intersecting(GS, capsS): st['R1_int_fail'] += 1
            cfg = find_config(GS, capsS, anchS)
            if cfg:
                st['R1_cfg'] += 1
                # lift
                pre = {proj(g, S): g for g in G if all(g[i] == 0 for i in S)}
                rows = [pre[c] for c in cfg]
                if not config_ok(rows, caps) or rows[0] != anchor: st['R1_lift_fail'] += 1
        # ---- R2 (and mutation)
        for s in range(1, m+1):
            for thr, tag in [(Fr(1, 2), 'R2'), (Fr(3, 5), 'R2mut')]:
                keep = [g for g in G if g[s] <= thr*caps[s]]
                G2 = [proj(g, {s}) for g in keep]; caps2 = proj(caps, {s})
                if tag == 'R2':
                    st['R2'] += 1
                    T2 = tau_star(G2, caps2)
                    if T2 < T - Fr(caps[s], 2): st['R2_tau_fail'] += 1
                    if T2 < T - Fr(caps[s], 3): st['R2loss3_fail'] += 1
                if isint and not intersecting(G2, caps2): st[tag + '_int_fail'] += 1
                cfg = find_config(G2, caps2, proj(anchor, {s}))
                if cfg:
                    st[tag + '_cfg'] += 1
                    # try to lift with the WORST preimage (max b_s) to stress the lifting
                    pre = {}
                    for g in keep:
                        k = proj(g, {s})
                        if k not in pre or g[s] > pre[k][s]: pre[k] = g
                    rows = [pre[c] for c in cfg]
                    if not config_ok(rows, caps): st[tag + '_lift_fail'] += 1
        # ---- R3: parts with cap >= 2r
        for s in range(1, m+1):
            if caps[s] >= 2*r:
                st['R3'] += 1
                G3 = [proj(g, {s}) for g in G]; caps3 = proj(caps, {s})
                if tau_star(G3, caps3) < T: st['R3_tau_fail'] += 1
                if isint and not intersecting(G3, caps3): st['R3_int_fail'] += 1
                cfg = find_config(G3, caps3, proj(anchor, {s}))
                if cfg:
                    st['R3_cfg'] += 1
                    pre = {}
                    for g in G:
                        k = proj(g, {s})
                        if k not in pre or g[s] > pre[k][s]: pre[k] = g
                    if not config_ok([pre[c] for c in cfg], caps): st['R3_lift_fail'] += 1
        # ---- NOFANO: random 6 rows with part-s loads in [0, r], anchor 0
        for _ in range(5):
            loads = [Fr(0)] + [Fr(rnd.randint(0, 2*r), 2) for _ in range(6)]
            if not part_ok(loads, Fr(3*r, 2)): st['NF_fail'] += 1
            if not part_ok(loads, Fr(3*r, 2) - Fr(1, 4)): st['NFmut_fail'] += 1
        # ---- M1 components
        X = sum(xs)
        def hgt(g): return max(Fr(g[1+s]) / xs[s] for s in range(m))
        Gh_map = {}
        for g in G:
            k = (g[0], X*hgt(g))
            Gh_map.setdefault(k, g)
        Gh = list(Gh_map)
        capsh = (Fr(e), Fr(X))
        Th = tau_star(Gh, capsh)
        if Th < T: st['M1_tau_fail'] += 1
        if Th > T: st['M1_tau_gain'] += 1
        if isint and not intersecting(Gh, capsh): st['M1_int_fail'] += 1
        cfg = find_config(Gh, capsh, (Fr(e), Fr(0)))
        if cfg:
            st['M1_cfg'] += 1
            rows = [Gh_map[c] for c in cfg]
            if not config_ok(rows, caps): st['M1_lift_fail'] += 1
    print('seed', seed, st)

if __name__ == '__main__':
    main()
