"""Erdős #644 — strategy verifier for upper-bound proofs (the budget game), atom-refined version.

Prover script, step j (j = 1..J):
   picks : list of (name, host, size) — host is a predicate on the current atoms (before A_j);
           the pick is a subset of the union of host atoms with |P| = size (affine in current masses).
   avoid : list of named picks and/or host predicates; A_j contains no point of them.
Atoms are (E, L): E = set of real edges containing the point, L = set of picks containing it.
The adversary chooses final atom masses (integers, units); every subfamily of 2..7 real edges must be
2-pierceable (two nonempty real cells whose union covers it). Infeasible => the script is a proof
for the configurations satisfying the script's hypotheses.
Soundness checks: (i) each pick size <= host mass (assumed as constraints; violations are reported
by a separate optimisation), (ii) the avoided total per step <= budget (reported likewise).
"""
import itertools, time, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

class Aff:
    """Affine function of current-atom masses: const + sum coef * mass(predicate)."""
    def __init__(self, const=0.0, terms=()):
        self.const = float(const); self.terms = list(terms)   # terms: (predicate on atom (E,L), coef)
    def __add__(self, o): return Aff(self.const + (o.const if isinstance(o, Aff) else o), self.terms + (o.terms if isinstance(o, Aff) else []))
    def __mul__(self, s): return Aff(self.const * s, [(p, c * s) for p, c in self.terms])
    __rmul__ = __mul__
    def __sub__(self, o): return self + (o * -1 if isinstance(o, Aff) else -o)

def mass(pred): return Aff(0.0, [(pred, 1.0)])
def cell(*edges):
    """predicate: atom's real-edge set restricted to edges placed so far equals exactly {edges}"""
    S = frozenset(edges)
    return lambda E, L, placed: (E & placed) == S
def cellin(base, *edges):
    """predicate: atom's real-edge set restricted to `base` equals exactly {edges}"""
    B = frozenset(base); S = frozenset(edges)
    return lambda E, L, placed: (E & B) == S
def inpick(name): return lambda E, L, placed: name in L
def contains(*edges):
    S = frozenset(edges); return lambda E, L, placed: S <= E
def both(p, q): return lambda E, L, placed: p(E, L, placed) and q(E, L, placed)
def notin(name): return lambda E, L, placed: name not in L

class Script:
    def __init__(self, J, D, budget, steps, intersecting=True, hyps=()):
        # steps[j] = {'picks': [(name, host_pred, size_aff_or_number)], 'avoid': [pred or name]}
        self.J, self.D, self.budget, self.steps, self.intersecting, self.hyps = J, D, budget, steps, intersecting, list(hyps)

def expand_atoms(script):
    """Return final atoms list and, per step, the intermediate-atom -> final-atoms mapping is implicit:
    an intermediate atom at step j (before A_j) with (E, L) corresponds to final atoms whose
    (E ∩ placed_j, L ∩ picks_before_j) equal it.  We just generate all final atoms as combinations
    of edge membership and pick membership consistent with hosts."""
    J = script.J
    atoms = [(frozenset(), frozenset())]          # fresh, no edges yet (mass free)
    pickhost = {}
    for j in range(1, J + 1):
        placed = frozenset(range(1, j))
        st = script.steps.get(j, {})
        for (name, host, size) in st.get('picks', []):
            pickhost[name] = (host, placed, size)
            new = []
            for (E, L) in atoms:
                if host(E, L, placed): new.append((E, L | {name})); new.append((E, L))
                else: new.append((E, L))
            atoms = new
        # place edge j: each atom splits into in/out; plus fresh atom {j}
        new = []
        for (E, L) in atoms:
            new.append((E | {j}, L)); new.append((E, L))
        new.append((frozenset({j}), frozenset()))
        atoms = new
    for (name, host, size) in getattr(script, 'final_picks', []):
        placed = frozenset(range(1, J + 1)); pickhost[name] = (host, placed, size)
        new = []
        for (E, L) in atoms:
            if host(E, L, placed): new.append((E, L | {name})); new.append((E, L))
            else: new.append((E, L))
        atoms = new
    # drop the all-empty fresh atom (points in no edge): irrelevant
    atoms = [a for a in atoms if a[0]]
    # dedupe
    atoms = sorted(set(atoms), key=lambda a: (sorted(a[0]), sorted(a[1])))
    return atoms, pickhost

def build(script, objective_aff=None, sense='min', continuous=False, eps=1e-3):
    J, D = script.J, script.D
    atoms, pickhost = expand_atoms(script)
    aid = {a: i for i, a in enumerate(atoms)}; nA = len(atoms)
    cells = [frozenset(c) for s in range(1, J + 1) for c in itertools.combinations(range(1, J + 1), s)]
    cid = {c: i for i, c in enumerate(cells)}; nc = len(cells)
    pairs = [(a, b) for a in range(nc) for b in range(a, nc)]
    nN, nZ, nW = nA, nc, len(pairs); nvar = nN + nZ + nW
    M = float(J * D)
    rows, lbs, ubs = [], [], []
    def add(coefs, lo, hi):
        row = np.zeros(nvar_ref[0])
        for j, v in coefs: row[j] += v
        rows.append(row); lbs.append(lo); ubs.append(hi)
    nvar_ref = [nvar]
    def atoms_where(pred, placed):
        return [(aid[a], 1.0) for a in atoms if pred(a[0], a[1], placed)]
    def aff_coefs(aff, placed):
        coefs = []; const = aff.const
        for pred, c in aff.terms:
            coefs += [(v, c * w) for v, w in atoms_where(pred, placed)]
        return coefs, const
    # edge sizes
    for j in range(1, J + 1):
        add([(aid[a], 1.0) for a in atoms if j in a[0]], D, D)
    # cell z linking: z_c = 1 iff some atom with E == c has mass
    for c in cells:
        i = cid[c]; A_c = [aid[a] for a in atoms if a[0] == c]
        add([(v, 1.0) for v in A_c] + [(nN + i, -M)], -np.inf, 0)
        add([(v, 1.0) for v in A_c] + [(nN + i, -(eps if continuous else 1.0))], 0, np.inf)
    for k, (a, b) in enumerate(pairs):
        add([(nN + nZ + k, 1.0), (nN + a, -1.0)], -np.inf, 0)
        add([(nN + nZ + k, 1.0), (nN + b, -1.0)], -np.inf, 0)
    for size in range(2, min(J, 7) + 1):
        for F in itertools.combinations(range(1, J + 1), size):
            Fs = frozenset(F); covering = [k for k, (a, b) in enumerate(pairs) if Fs <= (cells[a] | cells[b])]
            add([(nN + nZ + k, 1.0) for k in covering], 1, np.inf)
    if script.intersecting:
        for i, j in itertools.combinations(range(1, J + 1), 2):
            add([(aid[a], 1.0) for a in atoms if i in a[0] and j in a[0]], (eps if continuous else 1), np.inf)
    # picks: mass(pick) = min(size, mass(host)).  Binary y per pick: y=1 -> mass(pick)=size and host>=size;
    # y=0 -> pick = whole host (mass(pick)=host) and host<=size.  Sound: the prover never avoids more than size.
    pick_names = list(pickhost.keys())
    nY = len(pick_names)
    # extend variable space
    nvar_old = nvar; nvar = nvar + nY; nvar_ref[0] = nvar
    for r_ in rows:
        pass
    rows2 = [np.concatenate([row, np.zeros(nY)]) for row in rows]; rows[:] = rows2
    def add2(coefs, lo, hi):
        row = np.zeros(nvar)
        for j, v in coefs: row[j] += v
        rows.append(row); lbs.append(lo); ubs.append(hi)
    for yi, name in enumerate(pick_names):
        host, placed, size = pickhost[name]
        yv = nvar_old + yi
        pick_c = atoms_where(inpick(name), placed)
        host_c = [(aid[a], 1.0) for a in atoms if host(a[0], a[1], placed)]
        if isinstance(size, Aff): sc, const = aff_coefs(size, placed)
        else: sc, const = [], float(size)
        neg_sc = [(v, -w) for v, w in sc]
        # (1) mass(pick) <= size            : pick - size <= 0
        add2(pick_c + neg_sc, -np.inf, const)
        # (2) mass(pick) >= size - M(1-y)   : pick - size_terms - M y >= const - M
        #     (fixed 18 Sep 2026: the bound was -M-const, which made this row vacuous and let the adversary
        #      shrink a pick to 0; sound for plain avoids, but it inflated check_budget for notin() avoids)
        add2(pick_c + neg_sc + [(yv, -M)], const - M, np.inf)
        # (3) mass(pick) >= host - M y      : pick - host + M y >= 0
        add2(pick_c + [(v, -w) for v, w in host_c] + [(yv, M)], 0, np.inf)
        # (4) host <= size + M y  (if y=0 the host is smaller than size): host - size - M y <= 0
        add2(host_c + neg_sc + [(yv, -M)], -np.inf, const)
    # avoid
    for j in range(1, J + 1):
        placed = frozenset(range(1, j)); st = script.steps.get(j, {})
        for item in st.get('avoid', []):
            pred = inpick(item) if isinstance(item, str) else item
            coefs = [(aid[a], 1.0) for a in atoms if j in a[0] and pred(a[0], a[1], placed)]
            if coefs: add(coefs, 0, 0)
    # hypotheses: (Aff over final atoms with placed = all, lo, hi)
    for hyp in script.hyps:
        aff, lo, hi = hyp[0], hyp[1], hyp[2]
        sc, const = aff_coefs(aff, frozenset(range(1, J + 1)))
        add(sc, lo - const, hi - const)
    integrality = np.ones(nvar); lb = np.zeros(nvar); ub = np.full(nvar, np.inf); ub[nN:] = 1
    if continuous: integrality[:nN] = 0
    c = np.zeros(nvar)
    if objective_aff is not None:
        sc, const = aff_coefs(objective_aff, frozenset(range(1, J + 1)))
        for v, w in sc: c[v] += w if sense == 'min' else -w
    A = np.array(rows)
    return dict(A=A, lbs=np.array(lbs), ubs=np.array(ubs), integrality=integrality, lb=lb, ub=ub, c=c, atoms=atoms, aid=aid, nvar=nvar, pickhost=pickhost)

def solve(script, time_limit=600, want=False, continuous=False):
    m = build(script, continuous=continuous)
    res = milp(c=m['c'], constraints=LinearConstraint(m['A'], m['lbs'], m['ubs']), integrality=m['integrality'],
               bounds=Bounds(m['lb'], m['ub']), options={'time_limit': time_limit, 'disp': False})
    if res.status == 0: st = 'ADVERSARY SURVIVES'
    elif res.status == 2: st = 'PROVER WINS (infeasible)'
    else: st = 'UNKNOWN: ' + res.message
    out = {'status': st, 'n_atoms': len(m['atoms'])}
    if res.status == 0 and want:
        out['atoms'] = {(tuple(sorted(a[0])), tuple(sorted(a[1]))): int(round(res.x[m['aid'][a]])) for a in m['atoms'] if res.x[m['aid'][a]] > 0.5}
    return out

def check_budget(script, time_limit=300):
    """For each step j with an avoid list: maximise the avoided total over adversary configurations of the
    PREFIX (edges < j, all earlier moves, all <=7-subfamily constraints among them, step-j picks applied).
    Returns {j: max_avoided or None}; None means the prefix itself is infeasible (prover already won)."""
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
        m = build(pre, objective_aff=aff, sense='max')
        res = milp(c=m['c'], constraints=LinearConstraint(m['A'], m['lbs'], m['ubs']), integrality=m['integrality'],
                   bounds=Bounds(m['lb'], m['ub']), options={'time_limit': time_limit, 'disp': False})
        report[j] = None if res.status != 0 else -res.fun
    return report
