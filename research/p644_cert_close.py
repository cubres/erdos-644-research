"""Close the last gaps: locate uncovered slivers in the certificate, sample the MILP at their centroids
(clamped into the region), augment the certificate with the new template (points + masses), re-verify."""
import json, sys, time, math, random
from fractions import Fraction as Fr
from p644_nu2_pattern_thm import (DELTA, GAP, area, region_polygon, convex_hull, inside_poly, lp_point,
                                  rationalize_point, fam2, extract_template, intersect_polys, union_area, in_region)
from p644_cover_check import tri_inside, bbox_overlap
from p644_patterns import venn_milp
from p644_cert_verify import verify

def slivers(tri, polys, depth, max_depth, out):
    cand = [p for p in polys if bbox_overlap(tri, p)]
    for p in cand:
        if tri_inside(tri, p): return
    if depth >= max_depth:
        cand2 = [q for q in cand if area(intersect_polys(tri, q)) > 0]
        if union_area(cand2, tri) != area(tri): out.append(tri)
        return
    (a, b, c) = tri
    mab = ((a[0]+b[0])/2, (a[1]+b[1])/2); mbc = ((b[0]+c[0])/2, (b[1]+c[1])/2); mca = ((c[0]+a[0])/2, (c[1]+a[1])/2)
    for t in [(a, mab, mca), (mab, b, mbc), (mca, mbc, c), (mab, mbc, mca)]: slivers(t, cand, depth + 1, max_depth, out)

def template_entry(T, ndir=24):
    types, support = T
    xc = lp_point(types, support, 0, 0, margin=True)
    if xc is None: return None
    center = rationalize_point(types, support, xc)
    if center is None: return None
    pts = [center]
    for k in range(ndir):
        th = 2 * math.pi * k / ndir
        x = lp_point(types, support, math.cos(th), math.sin(th))
        if x is None: continue
        p = rationalize_point(types, support, x, center=center)
        if p is not None: pts.append(p)
    hull = convex_hull([(p[0], p[1]) for p in pts])
    if len(hull) < 3 or area(hull) == 0: return None
    return {'types': list(types), 'support': [(s, list(c)) for s, c in support],
            'points': [{'d': str(p[0]), 'c': str(p[1]), 'm': [str(v) for v in p[2]]} for p in pts],
            'poly': [(str(x), str(y)) for x, y in hull]}

if __name__ == '__main__':
    path = sys.argv[1]; max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    data = json.load(open(path)); random.seed(3); t0 = time.time()
    known = {(tuple(t['types']), tuple((s, tuple(c)) for s, c in t['support'])) for t in data['templates']}
    for rnd in range(1, 60):
        polys = [[(Fr(x), Fr(y)) for (x, y) in t['poly']] for t in data['templates']]
        out = []; slivers(tuple(region_polygon()), polys, 0, max_depth, out)
        print(f"round {rnd}: {len(data['templates'])} templates, {len(out)} slivers [{time.time()-t0:.0f}s]", flush=True)
        if not out: break
        new = 0
        for tri in out[:8]:
            cx = sum(p[0] for p in tri) / 3; cy = sum(p[1] for p in tri) / 3
            for rep in range(3):
                dd = float(cx) + (random.uniform(-0.0015, 0.0015) if rep else 0); cc = float(cy) + (random.uniform(-0.0015, 0.0015) if rep else 0)
                dd = min(max(dd, float(GAP) + 1e-4), 0.5 - 1e-4); cc = min(max(cc, 0.5 + 1e-4), dd + 0.5 - float(GAP) - 1e-4)
                st, info = venn_milp(fam2(dd, cc), m=None, want_solution=True, time_limit=900, intersecting=False)
                if st != 'FAILS':
                    print(f"  !! ({dd:.6f},{cc:.6f}) tau*={1+dd-cc:.4f}: {st}", flush=True)
                    if st == 'HAS': sys.exit("HAS point inside region -> raise GAP")
                    continue
                T = extract_template(dd, cc, info['cells'])
                if T is None or T in known: continue
                e = template_entry(T)
                if e is None: continue
                data['templates'].append(e); known.add(T); new += 1
                poly = [(Fr(x), Fr(y)) for (x, y) in e['poly']]
                print(f"  new template {''.join(x[0] if x in ('A1','A2') else x for x in T[0])} area={float(area(poly)):.6f} at ({dd:.5f},{cc:.5f}) contains={inside_poly(poly, Fr(dd).limit_denominator(10**6), Fr(cc).limit_denominator(10**6))}", flush=True)
                json.dump(data, open(path, 'w'), indent=1)
        if new == 0:
            max_depth += 1; print(f"  no new template; depth -> {max_depth}", flush=True)
    print("verifying final certificate ...", flush=True)
    ok = verify(path)
    print("FINAL VERDICT:", ok, flush=True)
