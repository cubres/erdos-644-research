#!/usr/bin/env python3
"""Discovery relaxation for the paired 168-downset profile.

No positive occupancy cutoff is imposed. Zero-mass active cells are permitted,
so a feasible result needs a separate support check; infeasibility would still
need an exact certificate. This script does not certify a new theorem.
"""
from __future__ import annotations
import argparse
import itertools as it
import json
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


class Model:
    def __init__(self):
        self.names, self.lo, self.hi, self.integer, self.obj = [], [], [], [], []
        self.rows, self.lower, self.upper = [], [], []

    def var(self, name, lo=0., hi=1., binary=False, objective=0.):
        j = len(self.names)
        self.names.append(name)
        self.lo.append(lo); self.hi.append(hi)
        self.integer.append(int(binary)); self.obj.append(objective)
        return j

    def add(self, terms, lo=-np.inf, hi=np.inf):
        row = {}
        for j, v in terms:
            row[j] = row.get(j, 0.) + float(v)
        self.rows.append({j: v for j, v in row.items() if v})
        self.lower.append(lo); self.upper.append(hi)

    def solve(self, seconds):
        ii, jj, vv = [], [], []
        for i, row in enumerate(self.rows):
            for j, v in row.items():
                ii.append(i); jj.append(j); vv.append(v)
        mat = coo_matrix((vv, (ii, jj)), shape=(len(self.rows), len(self.names))).tocsc()
        return milp(np.array(self.obj), integrality=np.array(self.integer),
                    bounds=Bounds(self.lo, self.hi),
                    constraints=LinearConstraint(mat, self.lower, self.upper),
                    options={"time_limit": seconds, "mip_rel_gap": 1e-7})


def downsets():
    ans = []
    for mask in range(1 << 16):
        if all(not (mask >> p & 1) or all(mask >> (p ^ (1 << i)) & 1
               for i in range(4) if p >> i & 1) for p in range(16)):
            ans.append({p for p in range(16) if mask >> p & 1})
    assert len(ans) == 168
    return ans


def proj(mask, rows):
    return sum(((mask >> r) & 1) << i for i, r in enumerate(rows))


def build(tau_min, all_four=False, fixed_zero=False):
    M = Model()
    tau = M.var("tau", tau_min, 1., objective=-1.)
    mass = [M.var(f"x_{s:06b}", hi=4. if s == 0 else 1.) for s in range(64)]
    occ = [M.var(f"z_{s:06b}", binary=True) for s in range(64)]
    for s in range(64):
        M.add([(mass[s], 1), (occ[s], -(4 if s == 0 else 1))], hi=0)
    if fixed_zero:
        M.hi[mass[0]] = 0
        M.hi[occ[0]] = 0
    for i in range(6):
        M.add([(mass[s], 1) for s in range(64) if s >> i & 1], lo=1, hi=1)

    pairs = list(it.combinations(range(6), 2))
    matching = {(0, 1), (2, 3), (4, 5)}
    high = {}
    for i, j in pairs:
        h = high[i, j] = M.var(f"high_{i}{j}", binary=True)
        if (i, j) in matching:
            M.hi[h] = 0
        trace = [(mass[s], 1) for s in range(64) if s >> i & 1 and s >> j & 1]
        M.add(trace + [(h, -1)], hi=.25)
        M.add(trace + [(h, -1)], lo=-.75)
    for triple in it.combinations(range(6), 3):
        M.add([(high[p], 1) for p in it.combinations(triple, 2)], lo=1)

    def endpoint_vars(rows, label):
        full = (1 << len(rows)) - 1
        groups = [[s for s in range(64) if proj(s, rows) == p]
                  for p in range(full + 1)]
        elig, weighted = [], []
        for p, group in enumerate(groups):
            e = M.var(f"e_{label}_{p}", binary=True)
            elig.append(e)
            partners = [s for s in range(64) if proj(s, rows) | p == full]
            for s in partners:
                M.add([(e, 1), (occ[s], -1)], lo=0)
            M.add([(e, 1)] + [(occ[s], -1) for s in partners], hi=0)
            cap = 6 if p == 0 else 1
            v = M.var(f"v_{label}_{p}", hi=cap)
            weighted.append(v)
            M.add([(v, 1), (e, -cap)], hi=0)
            M.add([(v, 1)] + [(mass[s], -1) for s in group], hi=0)
            M.add([(v, 1), (e, -cap)] + [(mass[s], -1) for s in group], lo=-cap)
        return groups, weighted

    groups6, v6 = endpoint_vars(tuple(range(6)), "six")
    m = M.var("m", hi=3.)
    M.add([(m, 1)] + [(v, -1) for v in v6], lo=0, hi=0)
    M.add([(m, 1), (tau, -1)], lo=0)
    ds = downsets()
    records = []
    choices = list(it.combinations(range(6), 4)) if all_four else [
        (0, 1, 2, 3), (0, 1, 4, 5), (2, 3, 4, 5)]
    for rows in choices:
        label = "".join(map(str, rows))
        groups, weighted = endpoint_vars(rows, label)
        pvar = M.var(f"p_{label}", hi=10.)
        M.add([(pvar, 1)] + [(v, -1) for v in weighted], lo=0, hi=0)
        matchings = [((rows[0], rows[1]), (rows[2], rows[3])),
                     ((rows[0], rows[2]), (rows[1], rows[3])),
                     ((rows[0], rows[3]), (rows[1], rows[2]))]
        if not all_four:
            matchings = [next(q for q in matchings if all(p in matching for p in q))]
        for mi, mt in enumerate(matchings):
            gates = [high[tuple(sorted(p))] for p in mt]
            for di, D in enumerate(ds[:-1]):  # Full downset only gives the whole ground.
                U = {q for q in range(16) if any(p | q == 15 for p in D)}
                A = [(weighted[p], 1) for p in D]
                B = [(weighted[p], 1) for p in D & U]
                uterms = [(mass[s], 1) for p in U for s in groups[p]]
                ys = [M.var(f"mode_{label}_{mi}_{di}_{r}", binary=True) for r in range(3)]
                M.add([(y, 1) for y in ys] + [(g, 1) for g in gates], lo=1)
                big = 30.
                # A <= p-m OR U >= tau OR U+p-m-B >= tau.
                M.add(A + [(pvar, -1), (m, 1), (ys[0], big)], hi=big)
                M.add([(j, -v) for j, v in uterms] + [(tau, 1), (ys[1], big)], hi=big)
                M.add([(j, -v) for j, v in uterms] + [(pvar, -1), (m, 1)] +
                      B + [(tau, 1), (ys[2], big)], hi=big)
                records.append((rows, mi, di, sorted(D), sorted(U)))
    return M, mass, occ, tau, m, records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=60.)
    ap.add_argument("--tau-min", type=float, default=.751)
    ap.add_argument("--all-four", action="store_true")
    ap.add_argument("--zero-outside", action="store_true")
    ap.add_argument("--support-from", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    M, mass, occ, tau, m, records = build(args.tau_min, args.all_four, args.zero_outside)
    slack = None
    if args.support_from:
        support = {c["mask"] for c in json.loads(args.support_from.read_text())["cells"] if c["active"]}
        M.obj[tau] = 0
        slack = M.var("positive_slack", hi=.1, objective=-1.)
        for s in range(64):
            M.lo[occ[s]] = M.hi[occ[s]] = int(s in support)
            if s in support:
                M.add([(mass[s], 1), (slack, -1)], lo=0)
        for j, name in enumerate(M.names):
            if name.startswith("high_"):
                p, q = map(int, name[5:])
                trace = [(mass[s], 1) for s in range(64) if s >> p & 1 and s >> q & 1]
                M.add(trace + [(j, -1), (slack, -1)], lo=-.75)
    print(f"model variables={len(M.names)} constraints={len(M.rows)} modes={len(records)}", flush=True)
    sol = M.solve(args.seconds)
    out = {"status": int(sol.status), "message": sol.message,
           "mip_gap": getattr(sol, "mip_gap", None),
           "mip_node_count": getattr(sol, "mip_node_count", None),
           "mip_dual_bound": getattr(sol, "mip_dual_bound", None),
           "variables": len(M.names), "constraints": len(M.rows),
           "all_four": args.all_four, "zero_outside": args.zero_outside}
    if sol.x is not None:
        out["tau"] = float(sol.x[tau]); out["m"] = float(sol.x[m])
        out["cells"] = [{"mask": s, "mass": float(sol.x[mass[s]]),
                         "active": bool(sol.x[occ[s]] > .5)} for s in range(64)
                        if sol.x[mass[s]] > 1e-8 or sol.x[occ[s]] > .5]
        out["ghosts"] = [s for s in range(64) if sol.x[occ[s]] > .5 and sol.x[mass[s]] < 1e-8]
        if slack is not None:
            out["positive_slack"] = float(sol.x[slack])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "cells"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
