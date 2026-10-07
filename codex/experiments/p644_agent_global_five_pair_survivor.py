"""Exact rational survivor of the specified low-c five-pair experiment.

This certifies a local constraint state, not an Erdős-644 counterexample.
The ten-edge family has a common two-point transversal.
"""
import itertools
import json
from pathlib import Path


K = 10000
C = 2400
# old 3-bit type, G/H side (0=G), J/K side (0=J), integer cell size
CELLS = [
    ('000', 0, 0, 2495), ('000', 0, 1, 5),
    ('000', 1, 0, 2495), ('000', 1, 1, 5),
    ('011', 0, 0, 2495), ('011', 0, 1, 5),
    ('011', 1, 0, 2495), ('011', 1, 1, 5),
    ('100', 1, 1, 2400),
    ('101', 0, 1, 2500), ('101', 1, 1, 100),
    ('110', 0, 0, 10), ('110', 0, 1, 2490),
    ('110', 1, 0, 10), ('110', 1, 1, 90),
    ('111', 1, 1, 2400),
]


def main():
    atoms = []
    for old, g, j, size in CELLS:
        bits = tuple(map(int, old)) + (g, j)
        rows = frozenset(2*i+b for i,b in enumerate(bits))
        atoms.append((bits, rows, size))
    row_sizes = [sum(n for bits,rows,n in atoms if r in rows) for r in range(10)]
    assert row_sizes == [K]*10
    assert sum(n for bits,rows,n in atoms) == 2*K
    intersections = [[sum(n for _,rows,n in atoms if i in rows and j in rows)
                      for j in range(10)] for i in range(10)]
    disjoint_pairs = [(i,j) for i in range(10) for j in range(i+1,10)
                      if intersections[i][j] == 0]
    assert disjoint_pairs == [(0,1),(2,3),(4,5),(6,7),(8,9)]

    def profile(pairs):
        target = frozenset(r for p in pairs for r in (2*p,2*p+1))
        q = 0
        eligible = set()
        for i,(_,ri,ni) in enumerate(atoms):
            for j in range(i+1, len(atoms)):
                _,rj,nj = atoms[j]
                if target <= ri|rj:
                    q += ni*nj
                    eligible.update([i,j])
        # No single atom covers a disjoint row pair, so no diagonal term.
        return q, sum(atoms[i][2] for i in eligible)

    triples = []
    for pairs in itertools.combinations_with_replacement(range(5),3):
        q,p = profile(pairs)
        assert q >= C*K, (pairs,q)
        assert p >= K+2*C, (pairs,p)
        triples.append({'pairs':[p+1 for p in pairs], 'Q':q, 'P':p,
                        'Q_over_k_squared':q/(K*K), 'P_over_k':p/K})
    old_q,old_p = profile((0,1,2))
    assert (old_q,old_p) == (C*K,K+2*C)

    # The very same pair pierces all ten rows, and therefore every <=7 rows.
    piercing_atom_pair = [0,15]
    assert atoms[0][1] | atoms[15][1] == frozenset(range(10))
    seven_sets_checked = 0
    for rows in itertools.combinations(range(10),7):
        assert set(rows) <= atoms[0][1] | atoms[15][1]
        seven_sets_checked += 1

    # First response: avoid both small old cells, and 1350 fixed points
    # of each 000/011 cell that are in H. Such subsets exist in atoms 2,6.
    first_trim = 1350
    assert first_trim <= atoms[2][2] and first_trim <= atoms[6][2]
    assert 2*C+2*first_trim == 3*K//4
    assert intersections[6][0] >= 0
    for old in ('100','111'):
        assert sum(n for bits,_,n in atoms if ''.join(map(str,bits[:3]))==old
                   and bits[3]==0) == 0
    for old in ('000','011'):
        assert sum(n for bits,_,n in atoms if ''.join(map(str,bits[:3]))==old
                   and bits[3]==0) <= K//8+C

    # The second response J avoids all of 101 and one specified point
    # each of 000,011 (choose from atoms 1,5); G has no outside points.
    assert all(bits[4]==1 for bits,_,_ in atoms if bits[:3]==(1,0,1))
    assert atoms[1][2] > 0 and atoms[5][2] > 0
    assert atoms[1][0][4] == atoms[5][0][4] == 1
    second_budget = K//2-C+2
    assert second_budget <= 3*K//4

    # Unequal two-rectangle hypotheses are automatically inapplicable:
    # all actual rows lie in every designated complementary-pair union.
    for r in range(10):
        for i,j in disjoint_pairs:
            assert intersections[r][i]+intersections[r][j] == K

    out = {
        'status':'EXACT LOCAL SURVIVOR; NOT A LARGE-TAU FAMILY',
        'k':K, 'c':f'{C}/{K}', 'row_sizes':row_sizes,
        'disjoint_pairs':[[i+1,j+1] for i,j in disjoint_pairs],
        'old_Q':old_q, 'minimum_Q':min(t['Q'] for t in triples),
        'old_P':old_p, 'minimum_P':min(t['P'] for t in triples),
        'first_avoidance_size':2*C+2*first_trim,
        'second_avoidance_size':second_budget,
        'seven_subsets_checked':seven_sets_checked,
        'global_piercing_atoms':piercing_atom_pair,
        'tau_of_ten_row_family':2,
        'atoms':[{'bits':list(bits),'rows':[r+1 for r in sorted(rows)],'size':n}
                 for bits,rows,n in atoms],
        'all_triples_with_repetition':triples,
    }
    destination = Path('outputs/agent_global_five_pair_survivor.json')
    destination.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items()
                      if k not in ('atoms','all_triples_with_repetition')},indent=2))
    print('Ten distinct-pair triples:')
    for t in triples:
        if len(set(t['pairs']))==3:
            print(t)


if __name__ == '__main__':
    main()
