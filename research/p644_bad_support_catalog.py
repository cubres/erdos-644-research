"""Exact complete bad-support catalogue for seven intersecting rows.

In an intersecting bad tuple no occupied cell has size at least five. The
complements of its four-cells form an arbitrary pairwise-intersecting family
F of triples. All compatible cells lie in the support consisting of their
four-complements, the triples outside F, and all smaller cells. F must NOT be
assumed maximal: adding a four-cell can exclude a previously occupied triple.
"""
from itertools import combinations, permutations
from collections import Counter
from pathlib import Path
import json
import time


def catalogue():
    start=time.time();triples=[sum(1<<j for j in a) for a in combinations(range(7),3)]
    index={a:i for i,a in enumerate(triples)}
    neighbours=[sum(1<<j for j,b in enumerate(triples) if a!=b and a&b) for a in triples]
    families=set();counts=Counter()
    def visit(chosen,remaining,size):
        families.add(chosen);counts[size]+=1
        while remaining:
            bit=remaining&-remaining;remaining^=bit;j=bit.bit_length()-1
            visit(chosen|bit,remaining&neighbours[j],size+1)
    visit(0,(1<<35)-1,0)
    assert len(families)==sum(counts.values())==1278686
    actions=[]
    for perm in permutations(range(7)):
        actions.append([1<<index[sum(1<<perm[j] for j in range(7) if a>>j&1)] for a in triples])
    assert len(actions)==5040
    print('Enumerated',len(families),'labelled intersecting triple families.',flush=True)
    unseen=set(families);orbits=[]
    while unseen:
        rep=min(unseen);inds=[i for i in range(35) if rep>>i&1]
        images={sum(action[i] for i in inds) for action in actions}
        assert images<=families
        assert images<=unseen
        unseen.difference_update(images)
        F=[triples[i] for i in inds]
        support=[127-a for a in F]+[a for a in triples if a not in F]
        support += [sum(1<<j for j in a) for n in range(3) for a in combinations(range(7),n)]
        maximal=[a for a in support if not any(a!=b and a&b==a for b in support)]
        assert all(a|b!=127 for a in maximal for b in maximal)
        orbits.append({'triple_family':F,'orbit_size':len(images),'maximal_cells':maximal})
        if len(orbits)%100==0:print('Orbits',len(orbits),'remaining',len(unseen),'seconds',round(time.time()-start,2),flush=True)
    assert sum(q['orbit_size'] for q in orbits)==1278686
    result={'labelled_families':1278686,'counts_by_size':dict(sorted(counts.items())),
            'orbits':orbits,'number_of_orbits':len(orbits),'elapsed':time.time()-start}
    Path('logs/astra_bad_support_catalog.json').write_text(json.dumps(result,indent=2))
    print('PASS:',len(orbits),'unlabelled support types;',1278686,'labelled triple families; seconds',round(time.time()-start,2),flush=True)
    return result


if __name__=='__main__':catalogue()
