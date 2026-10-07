"""Erdős #644 — strategy verifier, version 2 (19 Sep 2026): sparse constraint matrix and a compact
encoding of 2-pierceability, so that scripts with 9–10 edges fit in memory.

Same API as p644_strategy: Aff, mass, cell, cellin, inpick, contains, both, notin, Script,
expand_atoms, build, solve, check_budget.

2-pierceability of a subfamily F (only maximal F, i.e. all 7-subsets when J >= 7, else F = [J]):
  for s ⊆ F nonempty:  v_s <= sum of z_a over full cells a with a ∩ F = s     (an F-cell s is present)
  for m ⊆ F:           u_m <= sum of v_t over F-cells t ⊇ m                   (some present F-cell contains m)
  p_s <= v_s, p_s <= u_{F−s},  sum_s p_s >= 1
  ⇒ some present cells a, b with (a ∩ F) ∪ (b ∩ F) = F, i.e. two points cover F.
v, u, p are continuous in [0,1]; only the cell indicators z (and pick selectors y) are binary.
"""
import itertools, time, sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import milp, LinearConstraint, Bounds

from p644_strategy import Aff, mass, cell, cellin, inpick, contains, both, notin, Script, expand_atoms


class SparseRows:
    def __init__(self):
        self.r, self.c, self.v, self.lo, self.hi, self.n = [], [], [], [], [], 0
    def add(self, coefs, lo, hi):
        acc = {}
        for j, w in coefs: acc[j] = acc.get(j, 0.0) + w
        for j, w in acc.items():
            if w != 0.0: self.r.append(self.n); self.c.append(j); self.v.append(w)
        self.lo.append(lo); self.hi.append(hi); self.n += 1
    def matrix(self, nvar):
        return coo_matrix((self.v, (self.r, self.c)), shape=(self.n, nvar)).tocsr()


def build(script, objective_aff=None, sense='min', continuous=False, eps=1e-3, subfamilies=None, objective=None):
    J, D = script.J, script.D
    atoms, pickhost = expand_atoms(script)
    aid = {a: i for i, a in enumerate(atoms)}; nA = len(atoms)
    cells = [frozenset(c) for s in range(1, J + 1) for c in itertools.combinations(range(1, J + 1), s)]
    cid = {c: i for i, c in enumerate(cells)}; nc = len(cells)
    M = float(J * D)
    # variable layout: atoms | z (cells) | y (picks) | per-F blocks (v, u, p)
    pick_names = list(pickhost.keys()); nY = len(pick_names)
    nN, nZ = nA, nc
    zvar = lambda c: nN + cid[c]
    yvar = lambda i: nN + nZ + i
    nvar = nN + nZ + nY
    if subfamilies is None:
        subfamilies = [frozenset(F) for F in itertools.combinations(range(1, J + 1), min(J, 7))]
    Fblocks = []
    for F in subfamilies:
        Fl = sorted(F); fc = [frozenset(c) for s in range(1, len(Fl) + 1) for c in itertools.combinations(Fl, s)]
        base = nvar; idx = {c: i for i, c in enumerate(fc)}
        Fblocks.append((F, fc, idx, base)); nvar += 3 * len(fc)   # v: base+i, u: base+len+i, p: base+2len+i (u indexed by nonempty m; u_∅ handled separately)
    S = SparseRows()
    placed_all = frozenset(range(1, J + 1))
    def atoms_where(pred, placed):
        return [(aid[a], 1.0) for a in atoms if pred(a[0], a[1], placed)]
    def aff_coefs(aff, placed):
        coefs = []; const = aff.const
        for pred, c in aff.terms:
            coefs += [(v, c * w) for v, w in atoms_where(pred, placed)]
        return coefs, const
    # edge sizes
    for j in range(1, J + 1):
        S.add([(aid[a], 1.0) for a in atoms if j in a[0]], D, D)
    # z linking
    for c in cells:
        A_c = [aid[a] for a in atoms if a[0] == c]
        S.add([(v, 1.0) for v in A_c] + [(zvar(c), -M)], -np.inf, 0)
        S.add([(v, 1.0) for v in A_c] + [(zvar(c), -(eps if continuous else 1.0))], 0, np.inf)
    # 2-pierceability blocks
    for (F, fc, idx, base) in Fblocks:
        L = len(fc)
        vv = lambda s: base + idx[s]; uu = lambda m: base + L + idx[m]; pp = lambda s: base + 2 * L + idx[s]
        # v_s <= sum z_a over a with a ∩ F = s
        by_s = {}
        for c in cells:
            s = c & F
            if s: by_s.setdefault(s, []).append(zvar(c))
        for s in fc:
            S.add([(vv(s), 1.0)] + [(z, -1.0) for z in by_s.get(s, [])], -np.inf, 0)
        # u_m <= sum v_t over t ⊇ m (t nonempty F-cell)
        for m in fc:
            S.add([(uu(m), 1.0)] + [(vv(t), -1.0) for t in fc if m <= t], -np.inf, 0)
        # p_s <= v_s ; p_s <= u_{F-s} (if F-s nonempty; if s = F then p_s <= v_s only, plus need any nonempty cell: trivially true)
        for s in fc:
            S.add([(pp(s), 1.0), (vv(s), -1.0)], -np.inf, 0)
            rest = F - s
            if rest: S.add([(pp(s), 1.0), (uu(rest), -1.0)], -np.inf, 0)
        S.add([(pp(s), 1.0) for s in fc], 1, np.inf)
    if script.intersecting:
        for i, j in itertools.combinations(range(1, J + 1), 2):
            S.add([(aid[a], 1.0) for a in atoms if i in a[0] and j in a[0]], (eps if continuous else 1), np.inf)
    # picks: mass(pick) = min(size, host)
    for yi, name in enumerate(pick_names):
        host, placed, size = pickhost[name]
        yv = yvar(yi)
        pick_c = atoms_where(inpick(name), placed)
        host_c = [(aid[a], 1.0) for a in atoms if host(a[0], a[1], placed)]
        if isinstance(size, Aff): sc, const = aff_coefs(size, placed)
        else: sc, const = [], float(size)
        neg_sc = [(v, -w) for v, w in sc]
        S.add(pick_c + neg_sc, -np.inf, const)                          # pick <= size
        S.add(pick_c + neg_sc + [(yv, -M)], const - M, np.inf)          # pick >= size - M(1-y)
        S.add(pick_c + [(v, -w) for v, w in host_c] + [(yv, M)], 0, np.inf)   # pick >= host - M y
        S.add(host_c + neg_sc + [(yv, -M)], -np.inf, const)             # host <= size + M y
    # avoid
    for j in range(1, J + 1):
        placed = frozenset(range(1, j)); st = script.steps.get(j, {})
        for item in st.get('avoid', []):
            pred = inpick(item) if isinstance(item, str) else item
            coefs = [(aid[a], 1.0) for a in atoms if j in a[0] and pred(a[0], a[1], placed)]
            if coefs: S.add(coefs, 0, 0)
    # hypotheses
    for hyp in script.hyps:
        aff, lo, hi = hyp[0], hyp[1], hyp[2]
        sc, const = aff_coefs(aff, placed_all)
        S.add(sc, lo - const, hi - const)
    integrality = np.zeros(nvar); lb = np.zeros(nvar); ub = np.full(nvar, np.inf)
    if not continuous: integrality[:nN] = 1
    integrality[nN:nN + nZ + nY] = 1; ub[nN:] = 1
    c = np.zeros(nvar)
    if objective == 'pierce':
        for (F, fc, idx, base) in Fblocks:
            L = len(fc)
            for s in fc: c[base + 2 * L + idx[s]] = -1.0     # maximise sum of p
    if objective_aff is not None:
        sc, const = aff_coefs(objective_aff, placed_all)
        for v, w in sc: c[v] += w if sense == 'min' else -w
    A = S.matrix(nvar)
    return dict(A=A, lbs=np.array(S.lo), ubs=np.array(S.hi), integrality=integrality, lb=lb, ub=ub, c=c,
                atoms=atoms, aid=aid, nvar=nvar, pickhost=pickhost, ncons=S.n)


def solve(script, time_limit=600, want=False, continuous=False, verbose=False, objective=None):
    t0 = time.time()
    m = build(script, continuous=continuous, objective=objective)
    if verbose: print(f"   model: {len(m['atoms'])} atoms, {m['nvar']} vars, {m['ncons']} cons [{time.time()-t0:.0f}s]", flush=True)
    res = milp(c=m['c'], constraints=LinearConstraint(m['A'], m['lbs'], m['ubs']), integrality=m['integrality'],
               bounds=Bounds(m['lb'], m['ub']), options={'time_limit': time_limit, 'disp': False})
    if res.status == 0: st = 'ADVERSARY SURVIVES'
    elif res.status == 2: st = 'PROVER WINS (infeasible)'
    else: st = 'UNKNOWN: ' + res.message
    out = {'status': st, 'n_atoms': len(m['atoms']), 'nvar': m['nvar'], 'ncons': m['ncons'], 'obj': (None if res.status != 0 else -res.fun)}
    if res.status == 0 and want:
        out['atoms'] = {(tuple(sorted(a[0])), tuple(sorted(a[1]))): (round(float(res.x[m['aid'][a]]), 3) if continuous else int(round(res.x[m['aid'][a]])))
                        for a in m['atoms'] if res.x[m['aid'][a]] > (1e-6 if continuous else 0.5)}
    return out


def check_budget(script, time_limit=300, continuous=False):
    """For each step j with an avoid list: maximise the avoided total over adversary configurations of the
    PREFIX.  Returns {j: max_avoided or None}; None means the prefix itself is infeasible."""
    J = script.J; report = {}
    for j in range(2, J + 1):
        st = script.steps.get(j, {})
        if not st.get('avoid'): continue
        placed = frozenset(range(1, j))
        pre_hyps = [h for h in script.hyps if len(h) >= 4 and frozenset(h[3]) <= placed]
        pre = Script(j - 1, script.D, script.budget, {i: script.steps[i] for i in script.steps if i < j},
                     intersecting=script.intersecting, hyps=pre_hyps)
        pre.final_picks = st.get('picks', [])
        aff = Aff()
        for item in st['avoid']:
            pred = inpick(item) if isinstance(item, str) else item
            aff = aff + mass(lambda E, L, pl, p=pred: p(E, L, placed))
        m = build(pre, objective_aff=aff, sense='max', continuous=continuous)
        res = milp(c=m['c'], constraints=LinearConstraint(m['A'], m['lbs'], m['ubs']), integrality=m['integrality'],
                   bounds=Bounds(m['lb'], m['ub']), options={'time_limit': time_limit, 'disp': False})
        report[j] = None if res.status != 0 else -res.fun
    return report
