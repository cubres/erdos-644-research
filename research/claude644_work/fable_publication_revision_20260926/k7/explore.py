"""Interactive explorer for the k=7 game: states with named edges, requests, all responses,
static-closure verdicts (exact SAT).  Subfamily selection allowed (edges may be discarded)."""
import itertools, sys
from game import canon, static_closure, static_solution, enum_responses, apply_response, popcount, K, T, MAXEDGES

def cells_from_named(edges):
    """edges: dict name -> set of point labels. returns (names, cells dict mask->count, pointmap)."""
    names = sorted(edges)
    pts = set().union(*edges.values())
    cells = {}
    for p in pts:
        m = 0
        for i, n in enumerate(names):
            if p in edges[n]:
                m |= 1 << i
        cells[m] = cells.get(m, 0) + 1
    return names, cells

def show(names, cells):
    parts = []
    for m, c in sorted(cells.items(), key=lambda t: (-popcount(t[0]), t[0])):
        if c:
            parts.append(''.join(names[i] for i in range(len(names)) if m >> i & 1) + ':' + str(c))
    return ' '.join(parts)

def sub_state(names, cells, keep):
    """restrict to the edges in keep (list of names); returns (names2, cells2)."""
    idx = [names.index(n) for n in keep]
    new = {}
    for m, c in cells.items():
        nm = 0
        for j, i in enumerate(idx):
            if m >> i & 1:
                nm |= 1 << j
        if nm:
            new[nm] = new.get(nm, 0) + c
    return list(keep), new

def closes(names, cells, maxdrop=2):
    """Is there a subfamily (dropping at most maxdrop edges) with |F|<=7 that closes statically?
    returns the list of kept names or None."""
    e = len(names)
    for drop in range(0, maxdrop + 1):
        for keep in itertools.combinations(names, e - drop):
            if len(keep) > MAXEDGES:
                continue
            n2, c2 = sub_state(names, cells, list(keep))
            if static_closure(canon(len(n2), c2)):
                return list(keep)
    return None

def responses(names, cells, req, newname, maxdrop=2, quiet=False):
    """req: dict cellstring->count, e.g. {'AB':4,'AC':1}. Lists all responses and verdicts.
    Returns list of (h, names2, cells2, verdict)."""
    e = len(names)
    d = {}
    for cs, k in req.items():
        m = 0
        for ch in cs:
            m |= 1 << names.index(ch)
        d[m] = k
    assert sum(d.values()) <= T, 'request too big'
    for m, k in d.items():
        assert cells.get(m, 0) >= k, 'request exceeds cell %s' % cs
    out = []
    for h in enum_responses(e, cells, d):
        e2, c2 = apply_response(e, cells, h)
        n2 = names + [newname]
        v = closes(n2, c2, maxdrop)
        out.append((h, n2, c2, v))
    # group by canonical form
    seen = {}
    for h, n2, c2, v in out:
        key = canon(len(n2), c2)
        seen.setdefault(key, []).append((h, n2, c2, v))
    if not quiet:
        nopen = 0
        for key, lst in seen.items():
            h, n2, c2, v = lst[0]
            tag = 'closed(keep %s)' % ''.join(v) if v else 'OPEN'
            if not v: nopen += 1
            print('  [%s] %s   <- %s' % (tag, show(n2, c2), fmt_h(names, h)))
        print('  total responses %d, classes %d, open %d' % (len(out), len(seen), nopen))
    return [lst[0] for lst in seen.values()]

def fmt_h(names, h):
    return ' '.join(''.join(names[i] for i in range(len(names)) if m >> i & 1) + ':' + str(k) for m, k in sorted(h.items()))

def parse_req(names, s):
    """'AB:4 AC:1 BC:1' -> dict"""
    req = {}
    for tok in s.split():
        cs, k = tok.split(':')
        req[cs] = int(k)
    return req
