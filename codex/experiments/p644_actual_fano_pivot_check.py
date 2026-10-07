"""Exact support check for the new actual Fano witness pivot.

Checks the endpoint formula and closure of the containing Fano types.
This does not prove the general 3/4 bound.
"""
from itertools import product


def mask(labels):
    return sum(1 << (int(i)-1) for i in labels)


stars = ('235', '246', '145', '136')
cycles = ('1234', '1256', '3456')
new_stars = tuple(map(mask, ('145', '136', '234', '256')))
new_cycles = tuple(map(mask, ('1235', '1246', '3456')))
a, b = 3, 2
c = a+4*b
old_p, old_n = 3*a+12*b, 7*a+28*b
checked = 0

for traces in product((0, 1, c), repeat=4):
    for x, y in product((0, 1, b), repeat=2):
        if not x+y:
            continue
        for outside in (0, 1):
            cells = []

            def add_piece(labels, weight, in_response, group):
                if not weight:
                    return
                old = mask(labels)
                new = (old & ~1) | int(in_response)
                assert any(new & ~host == 0 for host in new_stars+new_cycles)
                cells.append((new, weight, group))

            for j, (star, g) in enumerate(zip(stars, traces)):
                group = j if j < 2 else None
                add_piece(star, g, True, group)
                add_piece(star, c-g, False, group)
            for cycle in cycles:
                group = 2 if cycle == '3456' else None
                add_piece(cycle, a, False, group)
                for removed in cycle:
                    labels = cycle.replace(removed, '')
                    g = x if labels == '123' else y if labels == '124' else 0
                    selected_group = 0 if labels == '123' else 1
                    add_piece(labels, g, True, selected_group)
                    add_piece(labels, b-g, False, group)
            if outside:
                cells.append((1, outside, None))
            assert sum(weight for _, weight, _ in cells) == old_n+outside
            assert not any(m == 63 for m, _, _ in cells)
            eligible = {i for i, (m, _, _) in enumerate(cells)
                        if any(m | n == 63 for n, _, _ in cells)}
            actual = sum(cells[i][1] for i in eligible)
            u, v = traces[:2]
            predicted = ((c if v else u)+(c if u else v)+x+y+a
                         + b*((u+x > 0)+(v+y > 0)+(u > 0)+(v > 0)))
            assert actual == predicted, (traces, x, y, outside, actual, predicted)
            if u and v:
                assert actual == old_p+x+y
                assert eligible == {i for i, (_, _, group) in enumerate(cells)
                                    if group is not None}
                masses = [sum(w for _, w, group in cells if group == j)
                          for j in range(3)]
                assert masses == [c+x, c+y, c]
                for i in eligible:
                    m, _, group = cells[i]
                    assert m & ~new_cycles[group] == 0
                for i, (m, _, _) in enumerate(cells):
                    if i not in eligible:
                        assert any(m & ~host == 0 for host in new_stars)
                change = (3*(old_n+outside)-actual)-(3*old_n-old_p)
                assert change == 3*outside-x-y
            checked += 1

print('PASS:', checked, 'exact support cases; degenerate endpoint formula,')
print('      full Fano-containing closure, eligible masses (c+x,c+y,c),')
print('      and nondegenerate potential change 3o-s.')
