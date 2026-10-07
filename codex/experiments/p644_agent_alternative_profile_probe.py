"""Exact rational/finite support exploration of a five-row endpoint profile.

Returns infimum closed-neighborhood costs; strict endpoint losses need a
positive margin. Exceptional O(1) cells are excluded in this discovery model.
"""
from itertools import combinations


def profile(a, b, c, d, e, f, cloud=1, return_all=False, atrace=0):
    raw = [('A+', 19, 1, atrace), ('A', 19, 0, a-atrace),
           ('B+', 44, 1, b), ('B-', 44, 0, a-b)]
    for name, mask, amount in [('C',14,c),('D',21,d),('E',41,e),('F',50,f)]:
        raw.extend([(name+'+',mask,1,amount),(name+'-',mask,0,cloud-amount)])
    cells = [row for row in raw if row[3] > 0]
    n = len(cells)
    masses = [0] * (1 << n)
    for mask in range(1, 1 << n):
        low = mask & -mask
        masses[mask] = masses[mask ^ low] + cells[low.bit_length()-1][3]
    best = None
    by_rows = []
    for rows in combinations(range(6), 4):
        rowmask = sum(1 << i for i in rows)
        neighbors = [sum(1 << j for j, (_, target, present2, _) in enumerate(cells)
                         if i != j and ((source | target) & rowmask) == rowmask and (present or present2))
                     for i, (_, source, present, _) in enumerate(cells)]
        endpointmask = sum(1 << i for i in range(n) if neighbors[i])
        loss = masses[endpointmask] - 2*a
        if loss < 0:
            return {'cost': 0, 'rows': tuple(i+1 for i in rows), 'already_smaller': True}
        row_best = None
        unions = [0] * (1 << n)
        for mask in range(1, 1 << n):
            low = mask & -mask
            unions[mask] = unions[mask ^ low] | neighbors[low.bit_length()-1]
            if mask & ~endpointmask or masses[mask] <= loss:
                continue
            neighborhood = unions[mask]
            cost = masses[neighborhood] + max(0, loss-masses[mask & neighborhood])
            if row_best is None or cost < row_best['cost']:
                row_best = {'cost': cost, 'rows': tuple(i+1 for i in rows),
                            'support': [cells[i][0] for i in range(n) if mask >> i & 1],
                            'neighbor': [cells[i][0] for i in range(n) if neighborhood >> i & 1],
                            'endpoint_mass': masses[endpointmask]}
        by_rows.append(row_best)
        if row_best is not None and (best is None or row_best['cost'] < best['cost']):
            best = row_best
    return {'best': best, 'by_rows': by_rows} if return_all else best


if __name__ == '__main__':
    from fractions import Fraction as F
    for a in [F(6,5),F(3,2),F(2),F(5,2),F(3),F(4),F(5),F(6)]:
        budget=F(3,4)*(a+2)
        b=min(a,2*a-budget)
        if b < 0:
            continue
        other=max(0,min(2,a-b))
        answer=profile(a,b,F(1),other/2,F(1),other/2)
        print('a',a,'budget',budget,'b',b,'other',other,'profile',answer,flush=True)
