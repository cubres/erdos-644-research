"""Exact coverage check of a region (triangle) by a union of convex polygons, by adaptive triangulation.

A triangle is COVERED if it lies inside one polygon (exact vertex test), or, after subdivision,
all of its pieces are.  Slivers that straddle polygon boundaries are subdivided down to a depth
limit and the remaining ones are checked by inclusion-exclusion over the few polygons meeting them.
Everything is exact rational arithmetic; a True answer is a proof that the closed region is covered
(polygons are closed; the region is the closure of its interior).
"""
import json, sys, time
from fractions import Fraction as Fr
from p644_nu2_pattern_thm import area, intersect_polys, union_area, inside_poly, region_polygon

def tri_inside(tri, poly):
    return all(inside_poly(poly, x, y) for (x, y) in tri)

def bbox_overlap(tri, poly):
    tx = [p[0] for p in tri]; ty = [p[1] for p in tri]; px = [p[0] for p in poly]; py = [p[1] for p in poly]
    return not (max(tx) < min(px) or min(tx) > max(px) or max(ty) < min(py) or min(ty) > max(py))

def covered(tri, polys, depth, max_depth, stats):
    cand = [p for p in polys if bbox_overlap(tri, p)]
    for p in cand:
        if tri_inside(tri, p): stats['leaf'] += 1; return True
    if depth >= max_depth:
        # exact inclusion-exclusion over the candidates meeting this sliver
        cand2 = [q for q in cand if area(intersect_polys(tri, q)) > 0]
        stats['ie'] += 1
        return union_area(cand2, tri) == area(tri)
    # subdivide into 4 (midpoints)
    (a, b, c) = tri
    mab = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2); mbc = ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2); mca = ((c[0] + a[0]) / 2, (c[1] + a[1]) / 2)
    for t in [(a, mab, mca), (mab, b, mbc), (mca, mbc, c), (mab, mbc, mca)]:
        if not covered(t, cand, depth + 1, max_depth, stats): return False
    return True

def load_polys(path):
    data = json.load(open(path))
    polys = [[(Fr(x), Fr(y)) for (x, y) in t['poly']] for t in data['templates']]
    return [p for p in polys if len(p) >= 3 and area(p) > 0], data

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'logs/nu2_pattern_thm.json'
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    polys, data = load_polys(path)
    R = region_polygon()
    t0 = time.time(); stats = {'leaf': 0, 'ie': 0}
    ok = covered(tuple(R), polys, 0, max_depth, stats)
    print(f"{len(polys)} polygons; region {R}; COVERED = {ok}; leaves {stats['leaf']}, inclusion-exclusion slivers {stats['ie']} [{time.time()-t0:.0f}s]")
