"""Exact one-response consequences of fixed-anchor V4 constructions.

No floating-point arithmetic or optimization dependency. Every forbidden box
comes directly from the proved six-facet V4 lemma. Its complement is an
upward-orthant union with explicit strict lower bounds. Intersecting with the
unit-rank slice discards orthants whose lower mass is already at least one.
This is a diagnostic/terminal-rule generator, not a general theorem proof.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys


def v4_cap(x, d, a, b):
    return tuple(min(x[i], 2*x[i]-a[i]-b[i],
                     2*x[i]-2*d[i]-b[i],
                     4*x[i]-4*d[i]-a[i]-b[i]) for i in range(len(x)))


def maximal_boxes(boxes):
    """Retain maximal closed boxes, each with its generating anchor roles."""
    kept = []
    for cap, roles in sorted(boxes.items(), key=lambda kv: -sum(kv[0])):
        if not any(all(c <= t for c, t in zip(cap, old)) for old, _ in kept):
            kept.append((cap, roles))
    return kept


def dominates(a, b):
    """The orthant with lower point/strict flags a contains that for b."""
    return all(v < w or (v == w and (not s or t))
               for (v, s), (w, t) in zip(a, b))


def escape_orthants(x, boxes):
    corners = [tuple((F(0), False) for _ in x)]
    for cap, _ in boxes:
        nxt = set()
        for corner in corners:
            if any(v > h or (v == h and s)
                   for (v, s), h in zip(corner, cap)):
                nxt.add(corner)
                continue
            for i, h in enumerate(cap):
                if h >= x[i]:
                    continue
                cc = list(corner)
                cc[i] = (h, True)
                cc = tuple(cc)
                if sum(v for v, _ in cc) >= 1:
                    continue  # at least the newly raised coordinate is strict
                nxt.add(cc)
        corners = []
        for cc in sorted(nxt, key=lambda c: (sum(v for v, _ in c), sum(s for _, s in c))):
            if not any(dominates(old, cc) for old in corners):
                corners.append(cc)
    return corners


def best_free_box(x, corners):
    """Exact supremum; a non-strict corner coordinate needs an epsilon cut.

    For rank one, a retained box of mass >=1 meets an escaped orthant iff
    its top satisfies every lower bound (strict where flagged). Thus all
    extremal coordinate cut levels belong to the finite corner list.
    We report the infimal cost; strict epsilon distinctions are separate.
    """
    assert len(x) == 3
    levels = [sorted({x[i]} | {cc[i][0] for cc in corners}, reverse=True)
              for i in range(3)]
    best = (sum(x), (F(0),)*3, False)
    def kills_inf(v, bound):
        low, strict = bound
        return v < low or (v == low and (strict or low > 0))
    for a, b in product(levels[0], levels[1]):
        active = [cc for cc in corners if not kills_inf(a, cc[0])
                  and not kills_inf(b, cc[1])]
        if any(cc[2] == (0, False) for cc in active):
            continue  # a nonnegative retained coordinate cannot cut below zero
        c = min([x[2]] + [cc[2][0] for cc in active])
        u = (a, b, c)
        cost = sum(x) - sum(u)
        if cost < best[0]:
            # Check actual closed box; otherwise arbitrarily small reductions
            # of coordinates selected at non-strict lower endpoints suffice.
            strict_ok = all(any(v < low or (v == low and s)
                                for v, (low, s) in zip(u, cc)) for cc in corners)
            best = (cost, u, strict_ok)
    return best


def analyse(x, types):
    candidates = {}
    for roles in product(range(len(types)), repeat=3):
        cap = v4_cap(x, *(types[i] for i in roles))
        if min(cap) >= 0 and sum(cap) >= 1:
            candidates.setdefault(cap, roles)
    boxes = maximal_boxes(candidates)
    corners = escape_orthants(x, boxes)
    cost, u, attained = best_free_box(x, corners)
    return {"capacities": x, "types": types, "boxes": boxes,
            "escape_corners": corners, "request_cost": cost,
            "retained_box": u, "closed_box_free": attained}


def check_result(result):
    x, types = result["capacities"], result["types"]
    assert all(sum(a) == 1 and all(0 <= ai <= xi for ai, xi in zip(a, x))
               for a in types)
    for cap, roles in result["boxes"]:
        assert cap == v4_cap(x, *(types[i] for i in roles))
    assert result["escape_corners"] == escape_orthants(x, result["boxes"])
    u = result["retained_box"]
    assert result["request_cost"] == sum(x)-sum(u)
    assert all(any(v <= low for v, (low, _) in zip(u, cc))
               for cc in result["escape_corners"])


if __name__ == "__main__":
    path = Path(sys.argv[1])
    data = json.loads(path.read_text())
    result = analyse(tuple(map(F, data["capacities"])),
                     [tuple(map(F, row)) for row in data["types"]])
    check_result(result)
    out = path.with_name(path.stem + ".v4_escape.json")
    out.write_text(json.dumps(result, default=str, indent=2) + "\n")
    print("Exact V4 terminal rule:", len(result["boxes"]), "maximal forbidden boxes,",
          len(result["escape_corners"]), "escape orthants")
    print("Infimal request cost:", result["request_cost"], float(result["request_cost"]))
    print("Retained box:", list(map(str, result["retained_box"])),
          "closed box free:", result["closed_box_free"])
    print(out)
