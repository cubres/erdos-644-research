"""Discovery probe for cardinality consequences of minimum-(P,Q) exchange.

This is not a certificate or a model of the full hypergraph. A feasible high
value only obstructs these particular necessary inequalities.
"""
import argparse
import itertools
import json
import random
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def inequalities(support):
    supp = set(support)
    neighbors = {s: {u for u in supp if s | u == 63} for s in supp}
    eligible = {s for s in supp if neighbors[s]}
    if not eligible:
        return None
    bounds = [("P", eligible)]
    ws = []
    qs = []
    for i in range(6):
        ws.append(set())
        qs.append(set())
        for s in supp:
            for u in supp:
                if s | u == 63 ^ (1 << i):
                    ws[-1].update((s, u))
                    if s not in eligible or u not in eligible:
                        qs[-1].update((s, u))
        bounds.append((f"W{i}", ws[-1]))
        for s in eligible:
            if s >> i & 1:
                bounds.append((f"D{i}:{s}", neighbors[s] | qs[-1]))
    return bounds


def solve(support):
    support = sorted(support)
    bounds = inequalities(support)
    if bounds is None:
        return None
    n = len(support)
    matrix = []
    rhs = []
    for i in range(6):
        matrix.append([float(s >> i & 1) for s in support] + [0])
        rhs.append(1)
    for _, subset in bounds:
        matrix.append([-float(s in subset) for s in support] + [1])
        rhs.append(0)
    result = linprog([0] * n + [-1], A_ub=matrix, b_ub=rhs,
                     bounds=[(1e-7, None)] * n + [(0, None)], method="highs")
    if not result.success:
        return None
    return {"t": float(result.x[-1]),
            "cells": [{"mask": s, "weight": float(result.x[j])} for j, s in enumerate(support)],
            "active_bounds": [label for (label, _), slack in zip(bounds, result.ineqlin.residual[6:]) if slack < 1e-7]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--degrees", default="3")
    parser.add_argument("--seed", type=int, default=20260922)
    args = parser.parse_args()
    degrees = {int(x) for x in args.degrees.split(",")}
    universe = [s for s in range(0, 63) if bin(s).count("1") in degrees]
    rng = random.Random(args.seed)
    best = None
    for j in range(args.trials):
        probability = rng.uniform(0.15, 0.95)
        supp = [s for s in universe if rng.random() < probability]
        result = solve(supp)
        if result is not None and (best is None or result["t"] > best["t"] + 1e-8):
            best = result
            print(json.dumps({"trial": j, "t": best["t"], "support_size": len(supp)}), flush=True)
    out = Path(__file__).resolve().parents[1] / "outputs" / ("agent_lex_support_" + args.degrees.replace(",", "_") + ".json")
    out.write_text(json.dumps(best, indent=2) + "\n")
    print(str(out), flush=True)
