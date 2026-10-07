"""Second phase of the coverage proof: load the saved templates, find uncovered slivers by adaptive
triangulation, sample the MILP at their centroids (with small perturbations), add the new templates,
and repeat until the region is exactly covered (or a HAS point is found inside the region)."""
import json, sys, time, random
from fractions import Fraction as Fr
from multiprocessing import Pool
from p644_nu2_pattern_thm import (area, intersect_polys, union_area, inside_poly, region_polygon, GAP,
                                  fam2, extract_template, template_polygon, in_region)
from p644_patterns import venn_milp
from p644_cover_check import tri_inside, bbox_overlap

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

def sample(args):
    d, c, tl = args
    st, info = venn_milp(fam2(d, c), m=None, want_solution=True, time_limit=tl, intersecting=False)
    if st != 'FAILS': return ('status', st, d, c)
    return ('tmpl', extract_template(d, c, info['cells']), d, c)

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'logs/nu2_pattern_thm.json'
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    tl = int(sys.argv[3]) if len(sys.argv) > 3 else 600
    data = json.load(open(path))
    templates = {}
    for t in data['templates']:
        T = (tuple(t['types']), tuple((s, tuple(c)) for s, c in t['support']))
        poly = [(Fr(x), Fr(y)) for (x, y) in t['poly']]
        if len(poly) >= 3 and area(poly) > 0: templates[T] = poly
    log = open('logs/nu2_cover_refine.log', 'a')
    def say(m): print(m, flush=True); log.write(m + '\n'); log.flush()
    R = tuple(region_polygon()); t0 = time.time(); random.seed(7)
    has_points = []
    with Pool(4) as pool:
        for rnd in range(1, 200):
            out = []
            slivers(R, list(templates.values()), 0, max_depth, out)
            say(f"round {rnd}: {len(templates)} templates, {len(out)} uncovered slivers [{time.time()-t0:.0f}s]")
            if not out: break
            jobs = []
            for tri in out[:16]:
                cx = float(sum(p[0] for p in tri) / 3); cy = float(sum(p[1] for p in tri) / 3)
                for rep in range(2):
                    dd = cx + random.uniform(-0.002, 0.002) * rep; cc = cy + random.uniform(-0.002, 0.002) * rep
                    # clamp into the region c <= d + 1/2 - GAP (and the other boundaries)
                    dd = min(max(dd, float(GAP) + 1e-4), 0.5 - 1e-4); cc = min(max(cc, 0.5 + 1e-4), dd + 0.5 - float(GAP) - 1e-4)
                    jobs.append((round(dd, 6), round(cc, 6), tl))
            new = 0
            for res in pool.imap_unordered(sample, jobs):
                if res[0] == 'status':
                    say(f"  !! ({res[2]},{res[3]}) tau*={1+res[2]-res[3]:.4f}: {res[1]}")
                    if res[1] == 'HAS' and in_region(Fr(res[2]), Fr(res[3])): has_points.append((res[2], res[3]))
                    continue
                T, dd, cc = res[1], res[2], res[3]
                if T is None or T in templates: continue
                poly, _ = template_polygon(T)
                if area(poly) == 0: continue
                templates[T] = poly; new += 1
                say(f"  new template {''.join(x[0] if x in ('A1','A2') else x for x in T[0])} |supp|={len(T[1])} area={float(area(poly)):.6f} at ({dd},{cc}) contains={inside_poly(poly, Fr(dd), Fr(cc))}")
            json.dump({'delta': data['delta'], 'gap': str(GAP), 'templates': [{'types': T[0], 'support': [(s_, list(c_)) for s_, c_ in T[1]], 'poly': [(str(x), str(y)) for x, y in p]} for T, p in templates.items()]},
                      open(path, 'w'), indent=1)
            if new == 0 and not has_points:
                say("  no new templates from sliver centroids; increasing depth")
                max_depth += 1
            if has_points: say(f"HAS points inside the region: {has_points}"); break
    say(f"DONE: {len(templates)} templates; uncovered slivers: {len(out)}; HAS inside region: {has_points} [{time.time()-t0:.0f}s]")
