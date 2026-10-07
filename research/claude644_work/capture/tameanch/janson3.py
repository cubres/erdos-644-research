# Generic TYPED-JANSON maximin engine for sparsified TYPE-CLOSED families (several parts), with optional
# fixed (deterministic) rows.  H_0 = all k-sets whose profile is in a type set T0 over parts with capacities x_i
# (per k); H_c = each edge of H_0 kept independently w.p. exp(-c k).
# A configuration = random rows R (each of a given type u^l in T0) + fixed rows (e.g. the anchor E0),
# with cells (block, trace on R).  Blocks = (part i, inside/outside the fixed rows); cap(block) given.
# For nonempty J subset R: exponent_J(m) = sum_B [cap_B ln cap_B - sum_{g} m_g ln m_g] - |J| c,
# where g runs over groups of cells of block B with equal trace on J (m_g = sum of their masses).
# (Lemma TJ of notes_randomside, generalised: symmetry group prod_i Sym(P_i); Ext depends only on the marginal type.)
# max_m min_J exponent_J > 0  =>  H_c contains the configuration whp (a bad 7-tuple after the deterministic rows/oracle).
import numpy as np, itertools, warnings
from scipy.optimize import minimize
warnings.filterwarnings("ignore")

def xlnx(v):
    v = np.maximum(v, 1e-300); return v*np.log(v)

class Config:
    def __init__(self, rows, blocks, cells, row_profiles, extra_ineq=(), extra_eq=()):
        # rows: list of random row names; blocks: dict name -> (cap, part); cells: list of (block, trace(frozenset), tag)
        # row_profiles: dict row -> dict part -> mass (profile u^l_i); extra_ineq: list of (coef dict cell-index->coef, rhs)
        # meaning coef.m <= rhs; extra_eq similar with equality.
        self.rows = list(rows); self.blocks = blocks; self.cells = cells; self.nc = len(cells)
        self.parts = sorted({b[1] for b in blocks.values()})
        self.Js = [J for r in range(1, len(rows)+1) for J in itertools.combinations(self.rows, r)]
        # equality matrix
        A = []; b = []
        for l in self.rows:
            for p in self.parts:
                A.append([1.0 if (l in c[1] and blocks[c[0]][1] == p) else 0.0 for c in cells]); b.append(row_profiles[l].get(p, 0.0))
        for bn, (cap, p) in blocks.items():
            A.append([1.0 if c[0] == bn else 0.0 for c in cells]); b.append(cap)
        for coef, rhs in extra_eq:
            A.append([coef.get(i, 0.0) for i in range(self.nc)]); b.append(rhs)
        self.Aeq = np.array(A); self.beq = np.array(b)
        self.ineq = [(np.array([coef.get(i, 0.0) for i in range(self.nc)]), rhs) for coef, rhs in extra_ineq]
        # marginal matrices per J and block
        self.MM = {}
        for J in self.Js:
            Jset = set(J); keys = {}
            for i, c in enumerate(cells):
                key = (c[0], frozenset(c[1] & Jset)); keys.setdefault(key, []).append(i)
            M = np.zeros((len(keys), self.nc))
            for r, (key, cs) in enumerate(keys.items()): M[r, cs] = 1.0
            self.MM[J] = M
        self.capterm = sum(cap*np.log(cap) for cap, p in blocks.values() if cap > 0)
    def expJ(self, m, J, c):
        g = self.MM[J] @ m
        return self.capterm - np.sum(xlnx(g)) - len(J)*c
    def gradJ(self, m, J):
        g = self.MM[J] @ m; g = np.maximum(g, 1e-300)
        return -(self.MM[J].T @ (np.log(g) + 1.0))
    def solve(self, c, tries=8, seed=0, maxiter=2000, verbose=False):
        rng = np.random.default_rng(seed); best = None
        cons = [{'type': 'eq', 'fun': lambda z: self.Aeq @ z[:-1] - self.beq, 'jac': lambda z: np.hstack([self.Aeq, np.zeros((len(self.beq), 1))])}]
        for a, rhs in self.ineq:
            cons.append({'type': 'ineq', 'fun': lambda z, a=a, rhs=rhs: rhs - a @ z[:-1], 'jac': lambda z, a=a: np.concatenate([-a, [0.0]])})
        for J in self.Js:
            cons.append({'type': 'ineq', 'fun': lambda z, J=J: self.expJ(z[:-1], J, c) - z[-1],
                         'jac': lambda z, J=J: np.concatenate([self.gradJ(z[:-1], J), [-1.0]])})
        bounds = [(1e-10, None)]*self.nc + [(None, None)]
        for t in range(tries):
            m0 = rng.random(self.nc) + 0.05
            # least-squares projection onto the equalities (then clip)
            try:
                sol, *_ = np.linalg.lstsq(self.Aeq, self.beq - self.Aeq @ m0, rcond=None); m0 = np.maximum(m0 + sol, 1e-6)
            except Exception: pass
            z0 = np.concatenate([m0, [-5.0]])
            r = minimize(lambda z: -z[-1], z0, jac=lambda z: np.concatenate([np.zeros(self.nc), [-1.0]]), constraints=cons, bounds=bounds,
                         method='SLSQP', options={'maxiter': maxiter, 'ftol': 1e-12})
            m = r.x[:-1]
            feas = np.max(np.abs(self.Aeq @ m - self.beq)) < 1e-6 and all(a @ m <= rhs + 1e-6 for a, rhs in self.ineq) and np.min(m) > -1e-9
            if not feas:
                if verbose: print('  try', t, 'infeasible', r.message)
                continue
            val = min(self.expJ(m, J, c) for J in self.Js)
            if best is None or val > best[0]: best = (val, m)
        return best
    def worstJ(self, m, c):
        return min(self.Js, key=lambda J: self.expJ(m, J, c))

# ---------- Fano geometry ----------
LINES = [frozenset(s) for s in [(0,1,3),(1,2,4),(2,3,5),(3,4,6),(4,5,0),(5,6,1),(6,0,2)]]
POINTS = range(7)
def safe(S):  # S: set of line indices; safe iff some point lies on none of them
    covered = set().union(*[LINES[l] for l in S]) if S else set()
    return len(covered) < 7
SAFE = [frozenset(S) for r in range(0, 8) for S in itertools.combinations(range(7), r) if safe(S)]
assert len(SAFE) == 64

def fano_static(caps, types, c_dummy=None):
    """7 random rows = lines 0..6 with types[l] (dict part->mass); cells = all 64 safe traces per part."""
    rows = list(range(7)); blocks = {('P', p): (caps[p], p) for p in caps}
    cells = [(('P', p), S, None) for p in caps for S in SAFE]
    return Config(rows, blocks, cells, {l: types[l] for l in rows})

def fano_anchored(caps, e_prof, types, L0=0):
    """Anchor E0 = row L0 fixed with profile e_prof; 6 random rows; cells: safe S containing L0 -> E0-block, else O-block."""
    rows = [l for l in range(7) if l != L0]
    blocks = {}
    for p in caps:
        if e_prof.get(p, 0) > 0: blocks[('E', p)] = (e_prof[p], p)
        if caps[p] - e_prof.get(p, 0) > 0: blocks[('O', p)] = (caps[p] - e_prof.get(p, 0), p)
    cells = []
    for p in caps:
        for S in SAFE:
            tr = frozenset(S - {L0})
            if L0 in S:
                if ('E', p) in blocks: cells.append((('E', p), tr, None))
            else:
                if ('O', p) in blocks: cells.append((('O', p), tr, None))
    return Config(rows, blocks, cells, {l: types[l] for l in rows})

def tc_anchored(caps, e_prof, types, taup):
    """TC at E0: random rows B1,B2,C1,C2 with types; g1,g2 by the oracle. Cells: O-block: all 16 traces;
    E0-block: traces not containing {B1,B2} nor {C1,C2}, split by quarter where ambiguous. Constraint:
    q + max(E1+E4, E2+E3) <= taup  (two linear inequalities)."""
    R = ['B1', 'B2', 'C1', 'C2']; rows = R
    blocks = {}
    for p in caps:
        if e_prof.get(p, 0) > 0: blocks[('E', p)] = (e_prof[p], p)
        if caps[p] - e_prof.get(p, 0) > 0: blocks[('O', p)] = (caps[p] - e_prof.get(p, 0), p)
    # quarter admissibility: quarter r1 <-> lines through r1 = B1,C1,g1 -> allowed traces subset {B2,C2}; r2: {B2,C1}; r3: {B1,C2}; r4: {B1,C1}
    allowed = {1: {'B2', 'C2'}, 2: {'B2', 'C1'}, 3: {'B1', 'C2'}, 4: {'B1', 'C1'}}
    cells = []
    for p in caps:
        if ('O', p) in blocks:
            for r in range(0, 5):
                for S in itertools.combinations(R, r): cells.append((('O', p), frozenset(S), None))
        if ('E', p) in blocks:
            for r in range(0, 3):
                for S in itertools.combinations(R, r):
                    S = frozenset(S)
                    for q in range(1, 5):
                        if S <= allowed[q]: cells.append((('E', p), S, q))
    types_d = {l: types[l] for l in R}
    # constraint coefficients
    def isX(tr): return (('B1' in tr) or ('B2' in tr)) and (('C1' in tr) or ('C2' in tr))
    coef14 = {}; coef23 = {}
    for i, (b, tr, q) in enumerate(cells):
        if b[0] == 'O' and isX(tr): coef14[i] = 1.0; coef23[i] = 1.0
        if b[0] == 'E':
            if q in (1, 4): coef14[i] = 1.0
            if q in (2, 3): coef23[i] = 1.0
    return Config(rows, blocks, cells, types_d, extra_ineq=[(coef14, taup), (coef23, taup)])
