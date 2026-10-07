"""Exact full-neighborhood certificate at the fixed ratio a=33b.

Enumerates all supports of the 17 positive five-row membership types.
Within each support, continuous selected masses are optimized analytically.
No optimizer, floating point, or external certificate file is needed.
"""
from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path


def instance():
    lines = [frozenset(t) for t in combinations(range(7), 3)
             if (t[0] + 1) ^ (t[1] + 1) ^ (t[2] + 1) == 0]
    types = [(line, 33) for line in lines]
    types += [(line | {h}, 1) for line in lines
              for h in set(range(7)) - line]
    cells = defaultdict(int)
    for typ, weight in types:
        mask = sum(1 << (j - 2) for j in range(2, 7) if j not in typ)
        cells[mask] += weight
    masks = sorted(s for s in cells if any(s | t == 31 for t in cells))
    weights = [cells[s] for s in masks]
    neighbors = [sum(1 << j for j, t in enumerate(masks) if s | t == 31)
                 for s in masks]
    assert len(masks) == 17
    assert all(not (neighbors[i] & (1 << i)) for i in range(17))
    assert sum(weights) == 185
    return masks, weights, neighbors


def main():
    masks, weights, neighbors = instance()
    size = 1 << len(masks)
    mass = [0] * size
    open_neighbors = [0] * size
    for z in range(1, size):
        bit = z & -z
        i = bit.bit_length() - 1
        old = z ^ bit
        mass[z] = mass[old] + weights[i]
        open_neighbors[z] = open_neighbors[old] | neighbors[i]

    threshold, p = 74, 111
    weak_min = None
    weak_supports = 0
    strict_supports = 0
    for z in range(size):
        nz = open_neighbors[z]
        n_mass = mass[nz]
        overlap_mass = mass[z & nz]
        if mass[z] >= threshold:
            # Select threshold mass, using Z intersect N(Z) first.
            # If selected support is smaller than Z, the declared
            # neighborhood only overcounts; every actual support is
            # also enumerated, giving the exact global minimum.
            value = n_mass + max(0, threshold - overlap_mass)
            weak_min = value if weak_min is None else min(weak_min, value)
            weak_supports += 1
            assert value >= p
        if mass[z] >= threshold + 1:
            strict_supports += 1
            # Actual cell masses are weights*b, threshold 74b+1.
            # Capacity is feasible precisely when mass[z]>=75.
            # These two coefficient inequalities prove >=111b+1
            # for every integer b>=1, without fixing b numerically.
            if overlap_mass <= threshold:
                assert n_mass + threshold - overlap_mass >= p
            else:
                assert n_mass >= p + 1
    assert weak_min == p

    # An actual rational/continuous weak witness, and an integer
    # strict witness valid for all b>=1. Pairs record cb+d points.
    selected = {
        0b11001: (34, 0), 0b00111: (34, 0),
        0b11000: (1, 0), 0b00110: (1, 0),
        0b10001: (1, 0), 0b00101: (1, 0),
        0b01001: (1, 0), 0b00011: (1, 1),
    }
    support = sum(1 << i for i, mask in enumerate(masks) if mask in selected)
    nz = open_neighbors[support]
    selected_total = [0, 0]
    closed_total = [0, 0]
    weak_closed = []
    for i, mask in enumerate(masks):
        c, d = selected.get(mask, (0, 0))
        assert c >= 0 and d >= 0 and c + d <= weights[i]
        selected_total[0] += c
        selected_total[1] += d
        if nz & (1 << i):
            closed_total[0] += weights[i]
            weak_closed.append(weights[i])
        else:
            closed_total[0] += c
            closed_total[1] += d
            weak_closed.append(c)
    assert selected_total == [74, 1]
    assert closed_total == [111, 1]

    # At the weak threshold, set the extra +1 to zero. Determine
    # the endpoints and pairs left by the stronger K_D criterion.
    residual_endpoint = 0
    residual_pairs = 0
    for i in range(len(masks)):
        js = [j for j in range(len(masks)) if neighbors[i] & (1 << j)]
        outside_neighbor = any(weights[j] > weak_closed[j] for j in js)
        residual_endpoint += weights[i] if outside_neighbor else weights[i] - weak_closed[i]
        for j in js:
            if i < j:
                residual_pairs += weights[i] * weights[j] - weak_closed[i] * weak_closed[j]
    result = {
        'status': 'EXACT_PASS', 'a_over_b': 33,
        'positive_types': len(masks), 'supports_checked': size,
        'weak_feasible_supports': weak_supports,
        'strict_feasible_supports': strict_supports,
        'five_row_endpoint_coefficient': 185,
        'six_row_endpoint_coefficient': p,
        'weak_threshold_coefficient': threshold,
        'weak_optimum_coefficient': weak_min,
        'strict_threshold': '74b+1', 'strict_optimum': '111b+1',
        'weak_witness_KD_endpoint_coefficient': residual_endpoint,
        'weak_witness_KD_pair_coefficient': residual_pairs,
        'old_pair_coefficient': 3669,
        'cells': [{'mask': format(mask, '05b'), 'weight_over_b': weight,
                   'strict_selected_cb_plus_d': selected.get(mask, (0, 0))}
                  for mask, weight in zip(masks, weights)],
    }
    Path('outputs/agent_near_fano_neighborhood_exact.json').write_text(json.dumps(result, indent=2))
    print(json.dumps({k: v for k, v in result.items() if k != 'cells'}, indent=2))


if __name__ == '__main__':
    main()
