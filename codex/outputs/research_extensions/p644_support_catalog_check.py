"""Independent verification of the complete seven-row bad-support catalogue.

The published representatives are the hexadecimal truth-table filenames in
Testa et al.'s primary repository. Completeness is proved here by counting all
permitted pair/triple families independently and checking disjoint permutation
orbits of the supplied truth tables. No circuit or solver result is trusted.
"""
from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json
import re
import time


def check(registry, output):
    started=time.time()
    pairs=[sum(1<<i for i in a) for a in combinations(range(7),2)]
    triples=[sum(1<<i for i in a) for a in combinations(range(7),3)]
    pn=[sum(1<<j for j,b in enumerate(pairs) if a!=b and a&b) for a in pairs]
    tn=[sum(1<<j for j,b in enumerate(triples) if a!=b and a&b) for a in triples]
    @lru_cache(None)
    def clique_count(remaining):
        if not remaining:return 1
        bit=remaining&-remaining;j=bit.bit_length()-1;rest=remaining^bit
        return clique_count(rest)+clique_count(rest&tn[j])
    pair_families=[]
    def pair_visit(chosen,remaining):
        pair_families.append(chosen)
        while remaining:
            bit=remaining&-remaining;remaining^=bit;j=bit.bit_length()-1
            pair_visit(chosen|bit,remaining&pn[j])
    pair_visit(0,(1<<21)-1)
    assert len(pair_families)==456
    total=0;empty_pair_total=None
    for code in pair_families:
        edges=[pairs[i] for i in range(21) if code>>i&1]
        forced=[t for t in triples if any(t&e==e for e in edges)]
        eligible=[i for i,t in enumerate(triples) if t not in forced and all(t&e for e in edges)]
        assert all(a&b for a,b in combinations(forced,2))
        assert all(triples[i]&t for i in eligible for t in forced)
        count=clique_count(sum(1<<i for i in eligible))
        total+=count
        if not edges:empty_pair_total=count
    # Seven additional self-dual functions have a winning singleton.
    assert empty_pair_total==1278686 and total+7==1422564
    print('PASS: independent count:',total,'without winning singletons; +7 dictators =',total+7,flush=True)
    source=json.loads(Path(registry).read_text())
    paths=[q['path'] for q in source['tree']['tree'] if q['type']=='blob' and q['path'].endswith('.v')]
    assert len(paths)==715 and source['tree'].get('truncated') is False
    truths=[]
    for path in paths:
        stem=Path(path).stem;assert re.fullmatch('[0-9a-f]{32}',stem)
        value=int(stem,16);bit=lambda m:(value>>m)&1
        assert bit(0)==0 and bit(127)==1
        assert all(bit(m)+bit(m^127)==1 for m in range(128))
        assert all(bit(m)<=bit(m|1<<i) for m in range(128) for i in range(7))
        assert all(bit(1<<i)==0 for i in range(7))
        truths.append((stem,value))
    pi={m:i for i,m in enumerate(pairs)};ti={m:i for i,m in enumerate(triples)}
    actions=[]
    for perm in permutations(range(7)):
        images=[sum(1<<perm[j] for j in range(7) if m>>j&1) for m in pairs+triples]
        actions.append(([1<<pi[m] for m in images[:21]],[1<<(21+ti[m]) for m in images[21:]]))
    assert len(actions)==5040
    seen=set();rows=[];small_count=0;size_counts={}
    for n,(stem,value) in enumerate(truths):
        E=[i for i,m in enumerate(pairs) if value>>m&1]
        F=[i for i,m in enumerate(triples) if value>>m&1]
        orbit={sum(a[i] for i in E)+sum(b[i] for i in F) for a,b in actions}
        assert seen.isdisjoint(orbit),('duplicate orbit',stem)
        seen.update(orbit)
        losing=[m for m in range(128) if not value>>m&1]
        maximal=[m for m in losing if all(value>>(m|1<<i)&1 for i in range(7) if not m>>i&1)]
        assert all(a|b!=127 for a in maximal for b in maximal)
        assert all(any(m&p==m for p in maximal) for m in losing)
        assert max(bin(m).count('1') for m in maximal)<=5
        assert sum(1<<i for i in range(7) if any(m>>i&1 for m in maximal))==127
        maxsize=max(bin(m).count('1') for m in maximal)
        size_counts[maxsize]=size_counts.get(maxsize,0)+1
        if not E:small_count+=1
        rows.append({'truth_table':stem,'orbit_size':len(orbit),'winning_pairs':[pairs[i] for i in E],
                     'winning_triples':[triples[i] for i in F],'maximal_cells':maximal})
        if (n+1)%100==0:print('Verified orbits',n+1,'covered functions',len(seen),'seconds',round(time.time()-started,2),flush=True)
    assert len(seen)==total and small_count==604
    assert sum(row['orbit_size'] for row in rows if not row['winning_pairs'])==empty_pair_total
    report={'primary_paper':'https://si2.epfl.ch/demichel/publications/archive/2019/IWLS_ET.pdf',
            'primary_repository':'https://github.com/eletesta/7input_classification',
            'source_tree_sha':source['tree']['sha'],'source_response_sha256':source['response_sha256'],
            'full_self_dual_orbits_including_dictator':716,'usable_bad_support_orbits':715,
            'support_orbits_with_maximum_cell_at_most_four':604,
            'labelled_nondictatorial_families':total,'maximal_cell_size_counts':size_counts,
            'orbits':rows,'elapsed':time.time()-started}
    Path(output).write_text(json.dumps(report,indent=2))
    print('PASS: 715 complete usable bad-support orbits; 604 have maximum cell size at most four.',flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('registry');parser.add_argument('--output',default='logs/astra_full_support_catalog.json')
    args=parser.parse_args();check(args.registry,args.output)
