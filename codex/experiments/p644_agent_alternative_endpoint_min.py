"""Discovery-only minimum endpoint mass for six rows of a two-type family."""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def solve(mixed, seconds):
    caps = [11.0, 215.0]
    total = sum(caps)
    rows = []
    lo = []
    hi = []

    def add(terms, lower=-np.inf, upper=np.inf):
        rows.append(terms)
        lo.append(lower)
        hi.append(upper)

    # 128 mass variables, 64 support indicators, 64 endpoint indicators,
    # 64 endpoint masses. Only support indicators require integrality.
    nv = 320
    for part, cap in enumerate(caps):
        add({64 * part + s: 1 for s in range(64)}, cap, cap)
        for i in range(6):
            count = (8 if i < mixed else 0) if part == 0 else (120 if i < mixed else 128)
            add({64 * part + s: 1 for s in range(64) if s >> i & 1}, count, count)
    for s in range(64):
        add({s: 1, 64 + s: 1, 128 + s: -total}, upper=0)
        add({256 + s: 1, s: -1, 64 + s: -1, 192 + s: -total}, lower=-total)
    for s in range(64):
        for t in range(s, 64):
            if s | t == 63:
                d = {192 + s: 1, 128 + s: -1}
                d[128 + t] = d.get(128 + t, 0) - 1
                add(d, lower=-1)
                if t != s:
                    add({192 + t: 1, 128 + s: -1, 128 + t: -1}, lower=-1)
    matrix = lil_matrix((len(rows), nv))
    for i, row in enumerate(rows):
        for j, value in row.items():
            matrix[i, j] = value
    upper = np.r_[np.repeat(caps[0], 64), np.repeat(caps[1], 64), np.ones(128), np.repeat(total, 64)]
    integer = np.zeros(nv)
    integer[128:192] = 1
    objective = np.zeros(nv)
    objective[256:] = 1
    res = milp(objective, integrality=integer, bounds=Bounds(np.zeros(nv), upper),
               constraints=LinearConstraint(matrix.tocsr(), lo, hi),
               options={"time_limit": seconds, "mip_rel_gap": 0})
    answer = {"mixed": mixed, "status": int(res.status), "message": res.message,
              "objective": None if res.fun is None else float(res.fun),
              "dual_bound": getattr(res, "mip_dual_bound", None)}
    if res.x is not None:
        support = [s for s in range(64) if res.x[s] + res.x[64 + s] > 1e-7]
        eligible = {s for s in support if any(s | t == 63 for t in support)}
        answer["actual_endpoint_mass"] = sum(res.x[s] + res.x[64 + s] for s in eligible)
        answer["cells"] = [{"mask": s, "rows": [i + 1 for i in range(6) if s >> i & 1],
                            "a": float(res.x[s]), "b": float(res.x[64 + s]),
                            "eligible": s in eligible} for s in support]
    return answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mixed", type=int, default=5)
    parser.add_argument("--seconds", type=float, default=30)
    args = parser.parse_args()
    answer = solve(args.mixed, args.seconds)
    out = Path(__file__).resolve().parents[1] / "outputs" / f"agent_endpoint_min_{args.mixed}.json"
    out.write_text(json.dumps(answer, indent=2) + "\n")
    print(json.dumps({k: v for k, v in answer.items() if k != "cells"}))
