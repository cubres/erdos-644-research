"""Self-contained exact certificate for Theorem 4.6 (sigma_2 <= 1/2 + GAP).

Phase A (augment): for each template in the coverage JSON, recompute an inner polygon as the convex
hull of rational points (d, c) together with explicit rational cell masses, and store the points WITH
their masses.  Phase B (verify, independent of any solver): re-check from the certificate alone that
  (1) every template's support (plus admissible singleton cells) contains no two cells covering [7];
  (2) every stored point (d, c, masses) satisfies all template constraints exactly
      (edge traces, part capacities, masses >= DELTA for support cells, slacks >= 0);
  (3) the stored polygon equals the convex hull of the stored points;
  (4) the closed region {GAP <= d <= 1/2, 1/2 <= c <= d + 1/2 - GAP} is covered by the union of the
      polygons (exact adaptive triangulation with inclusion-exclusion on slivers).
A True verdict means: for every rational (d, c) in the region, F_{d,c} contains a non-2-pierceable
7-tuple (at every scale where d, c and the masses are integral), hence sigma_2 <= 1/2 + GAP.
"""
import json, sys, time, math
from fractions import Fraction as Fr
from p644_nu2_pattern_thm import (DELTA, GAP, area, region_polygon, convex_hull, inside_poly, lp_point,
                                  rationalize_point, exact_feasible, template_data, eval_target)
from p644_cover_check import covered

def augment(path_in, path_out, ndir=24):
    data = json.load(open(path_in)); out = []
    t0 = time.time()
    for i, t in enumerate(data['templates']):
        types = tuple(t['types']); support = tuple((s, tuple(c)) for s, c in t['support'])
        xc = lp_point(types, support, 0, 0, margin=True)
        if xc is None: continue
        center = rationalize_point(types, support, xc)
        if center is None: continue
        pts = [center]
        for k in range(ndir):
            th = 2 * math.pi * k / ndir
            x = lp_point(types, support, math.cos(th), math.sin(th))
            if x is None: continue
            p = rationalize_point(types, support, x, center=center)
            if p is not None: pts.append(p)
        hull = convex_hull([(p[0], p[1]) for p in pts])
        if len(hull) < 3 or area(hull) == 0: continue
        out.append({'types': list(types), 'support': [(s, list(c)) for s, c in support],
                    'points': [{'d': str(p[0]), 'c': str(p[1]), 'm': [str(v) for v in p[2]]} for p in pts],
                    'poly': [(str(x), str(y)) for x, y in hull]})
        if i % 20 == 0: print(f"  augmented {i+1}/{len(data['templates'])} [{time.time()-t0:.0f}s]", flush=True)
    json.dump({'delta': str(DELTA), 'gap': str(GAP), 'templates': out}, open(path_out, 'w'), indent=1)
    print(f"certificate written: {len(out)} templates -> {path_out} [{time.time()-t0:.0f}s]", flush=True)

def verify(path):
    data = json.load(open(path)); t0 = time.time()
    assert Fr(data['delta']) == DELTA and Fr(data['gap']) == GAP
    polys = []
    for i, t in enumerate(data['templates']):
        types = tuple(t['types']); support = tuple((s, tuple(c)) for s, c in t['support'])
        # (1) no covering pair among support cells and the singleton slacks actually used
        rows = template_data(types, support); assert rows is not None
        cells = [frozenset(c) for _, c in support]
        slack_cells = [frozenset([j]) for (side, j, tgt, cc, kind) in rows if kind == 'le']
        allc = cells + slack_cells
        for a in allc:
            for b in allc:
                assert a | b != frozenset(range(7)), f"template {i}: covering pair {sorted(a)} {sorted(b)}"
        # (2) every stored point is exactly feasible
        pts = []
        for p in t['points']:
            d = Fr(p['d']); c = Fr(p['c']); m = [Fr(v) for v in p['m']]
            assert len(m) == len(support)
            assert exact_feasible(types, support, d, c, m), f"template {i}: point ({d},{c}) not feasible"
            pts.append((d, c))
        # (3) polygon = convex hull of the points
        hull = convex_hull(pts)
        poly = [(Fr(x), Fr(y)) for (x, y) in t['poly']]
        assert set(hull) == set(poly), f"template {i}: stored polygon is not the hull of its points"
        polys.append(hull)
    print(f"  {len(polys)} templates: supports, points and hulls verified [{time.time()-t0:.0f}s]", flush=True)
    R = tuple(region_polygon()); stats = {'leaf': 0, 'ie': 0}
    ok = covered(R, polys, 0, 9, stats)
    print(f"COVERAGE of region gap={GAP}: {ok}  (leaves {stats['leaf']}, slivers {stats['ie']}) [{time.time()-t0:.0f}s]", flush=True)
    return ok

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'augment': augment(sys.argv[2], sys.argv[3])
    else: verify(sys.argv[2])
