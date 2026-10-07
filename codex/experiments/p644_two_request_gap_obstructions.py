"""Exact new repair-support data around the two 115b six-tuples.

No solver and no input certificate. Weights are integer coefficients of b.
This records the new gap-adjusted repair-cover barrier, not the old
neighborhood optimization and not a high-transversal counterexample.
"""
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
    def trace(omit,rows):
        return sum(1<<j for j,r in enumerate(rows) if r not in omit)
    D1={i for i,(omit,w) in enumerate(types)
        if trace(omit,(2,4,5,6)) in {2,6,9,11,13}}
    P={i for i,(omit,w) in enumerate(types)
       if any(0 in line and line<=omit for line in lines)}
    C={i for i,(omit,w) in enumerate(types)
       if omit in [frozenset(v) for v in [(0,1,2,5),(0,1,2,6),
                                        (0,1,5,6),(0,2,5,6)]]}
    points=[]
    for i,(omit,w) in enumerate(types):
        g=int(i not in D1); h=int(i not in P or i in C)
        if omit==frozenset((2,4,5)):
            points.append({'omit':sorted(omit),'weight':25,'g':1,'h':1,'part':'retained'})
            points.append({'omit':sorted(omit),'weight':8,'g':0,'h':0,'part':'R'})
        else:
            points.append({'omit':sorted(omit),'weight':w,'g':g,'h':h})
    points.append({'omit':list(range(7)),'weight':1,'g':1,'h':0,'part':'Y'})
    for v in points:
        v['mask']=sum(1<<r for r in range(1,7) if r not in v['omit'])
        v['mask']|=v['g']<<7|v['h']<<8
    assert sum(v['weight'] for v in points if v['g'])==144
    assert sum(v['weight'] for v in points if v['h'])==144
    assert sum(v['weight'] for v in points if v['g'] and v['h'])==71
    results=[]
    for rows in [(1,2,3,5,6,8),(1,2,4,5,6,8)]:
        full=sum(1<<r for r in rows)
        adj=[{j for j,v in enumerate(points) if (v['mask']|u['mask'])&full==full}
             for u in points]
        endpoints={i for i,a in enumerate(adj) if a}
        assert sum(points[i]['weight'] for i in endpoints)==115
        for r in rows:
            sub=full^(1<<r)
            assert not any(v['mask']&sub==sub for v in points), 'common point would require ambient outside types'
            adj5=[{j for j,v in enumerate(points) if(v['mask']|u['mask'])&sub==sub}
                  for u in points]
            W={i for i in range(len(points)) if adj5[i]-adj[i]}
            mass=sum(points[i]['weight'] for i in W)
            expected=107 if rows==(1,2,4,5,6,8) and r==8 else 115 if r==8 else 113 if r in (3,4) else 114
            assert mass==expected
            external=[]
            if mass==107:
                for i in sorted(W&endpoints):
                    nb=adj[i]-W
                    ext=sum(points[j]['weight'] for j in nb)
                    external.append({'point_type':points[i], 'outside_neighbor_weight':ext})
                assert sorted(v['outside_neighbor_weight'] for v in external)==[36,36,36,36,76]
            results.append({'rows':list(rows),'removed':r,'repair_weight':mass,
                            'repair_types':[points[i] for i in sorted(W)],
                            'external_neighbors_of_old_endpoints':external})
    out={'status':'EXACT_PASS','valid_for':'all integer b>=1',
         'G_rank':144,'H_rank':144,'G_intersect_H_weight':71,
         'types':points,'repair_data':results}
    Path('outputs/agent_two_request_gap_obstructions.json').write_text(json.dumps(out,indent=2))
    print('EXACT_PASS: |G|=|H|=144b, |G intersect H|=71b')
    for v in results: print('tuple',v['rows'],'drop',v['removed'],'|W|=',v['repair_weight'],'b')
    print('EXACT_PASS: the unique107b repair support has external-neighbor weights36b,36b,36b,36b,76b')


if __name__=='__main__':main()
