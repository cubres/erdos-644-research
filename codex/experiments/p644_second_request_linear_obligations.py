"""Whole-cell second-request obligations after the fixed near-Fano D1.

The endpoint bounds are valid without assuming that every allowed G-cell
is occupied: allowing each such partner only enlarges endpoint sets.
Integer support enumeration and the final feasible vector are exact.
"""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import json


def main():
    lines=[frozenset(t) for t in combinations(range(7),3)
           if (t[0]+1)^(t[1]+1)^(t[2]+1)==0]
    types=[]
    for line in lines:
        types.append((line,33))
        types.extend((line|{h},1) for h in set(range(7))-line)
    def mask(omit,rows):
        return sum(1<<j for j,r in enumerate(rows) if r not in omit)
    firstrows=(2,4,5,6)
    D1={i for i,(omit,w) in enumerate(types)
        if mask(omit,firstrows) in {2,6,9,11,13}}
    allowed=[i for i in range(len(types)) if i not in D1]
    assert sum(types[i][1] for i in D1)==108
    obligations={}
    counts=[]
    for rows in combinations(range(1,7),4):
        group=defaultdict(list)
        for i,(omit,w) in enumerate(types): group[mask(omit,rows)].append(i)
        if 15 in group: continue
        ss=sorted(group); nn=len(ss)
        weights=[sum(types[i][1] for i in group[s]) for s in ss]
        available=sum(1<<j for j,s in enumerate(ss)
                      if any(i not in D1 for i in group[s]))
        neighbors=[sum(1<<q for q,v in enumerate(ss) if s|v==15) for s in ss]
        cost=[0]*(1<<nn); tested=positive=0
        for bits in range(1<<nn):
            if bits:
                low=bits&-bits
                cost[bits]=cost[bits^low]+weights[low.bit_length()-1]
            if cost[bits]>108: continue
            tested+=1; base=0; on=[]
            for j,s in enumerate(ss):
                possible=neighbors[j]
                if bits>>j&1: possible &= ~bits
                if possible & available:
                    base+=weights[j]
                elif possible:
                    on.extend(i for i in group[s] if i not in D1)
            rhs=111-base
            if rhs<=0: continue
            positive+=1; key=tuple(sorted(on))
            if rhs>obligations.get(key,{}).get('rhs',-1):
                obligations[key]={'rhs':rhs,'rows':list(rows),
                    'D2_masks':[format(s,'04b') for j,s in enumerate(ss) if bits>>j&1],
                    'cost':cost[bits],'always_endpoint_mass':base}
        counts.append({'rows':list(rows),'tested':tested,'positive':positive})
    constraints=list(obligations)
    assert len(counts)==12
    assert sum(v['tested'] for v in counts)==51264
    assert len(constraints)==2
    assert all(obligations[key]['rhs']==1 for key in constraints)
    assert set.intersection(*(set(key) for key in constraints))=={28}
    # This realizes the linear obligations, not the whole actual-family
    # normalization. One positive RHS also proves its total mass minimal.
    witness={i:int(i==28) for i in allowed}
    assert all(0<=witness[i]<=types[i][1] for i in allowed)
    assert all(sum(witness[i] for i in key)>=obligations[key]['rhs']
               for key in constraints)
    out={'counts':counts,'allowed':allowed,'types':[
        {'omitted':sorted(omit),'weight':w} for omit,w in types],
        'D1':sorted(D1),'obligations':[
            {'G_type_indices':list(key),**obligations[key]} for key in constraints],
        'exact_minimum_mass_in_linear_relaxation':sum(witness.values()),
        'exact_integer_G_masses':[witness[i] for i in allowed]}
    path=Path('outputs/agent_second_request_linear_obligations.json')
    path.write_text(json.dumps(out,indent=2))
    print(json.dumps({'four_row_sets':len(counts),'obligations':len(obligations),
          'status':'EXACT_PASS',
          'exact_minimum_mass_in_linear_relaxation':sum(witness.values())}))
    for key in constraints:
        print('NEED',obligations[key]['rhs'],'G mass on',key,
              'via rows',obligations[key]['rows'],'request',obligations[key]['D2_masks'])


if __name__=='__main__':main()
