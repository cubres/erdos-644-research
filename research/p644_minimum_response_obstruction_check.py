"""Independent exact lower bounds for three first-request response examples.

Enumerates every nonempty minimal three-request label family directly; no
discovery imports or solver. Ten rational request-price choices supply valid
lower bounds, so their completeness as an LP arrangement is not assumed.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import gcd
import json
from pathlib import Path


def antichains():
    out=[]
    for bits in range(1,128):
        family=tuple(i+1 for i in range(7) if bits>>i&1)
        if all(a&b!=a and a&b!=b for a,b in combinations(family,2)):
            out.append(family)
    assert len(out)==18
    return out


def check(gaps=False):
    ants=antichains();idx={a:i for i,a in enumerate(ants)}
    blocks=[]
    for a in ants:
        hitting=[m for m in range(1,8) if all(m&n for n in a)]
        minimal=tuple(m for m in hitting if not any(q!=m and q&m==q for q in hitting))
        blocks.append(idx[minimal])
    compat=[[j for j,b in enumerate(ants) if all(m&n for m in a for n in b)] for a in ants]
    prices=sorted(set(permutations((12,0,0)))|set(permutations((6,6,0)))|
                  set(permutations((6,3,3)))|{(4,4,4)})
    assert len(prices)==10 and all(min(q)>=0 and sum(q)==12 for q in prices)
    cost=[[min(sum(q[j] for j in range(3) if m>>j&1) for m in a) for q in prices] for a in ants]
    examples=[([200,43,186],[F(1),F(2893,12),F(347,12),F(229)]),
              ([43,200,186],[F(1),F(2893,12),F(3095,12)-F(1,100),F(1,100)]),
              ([186,200,43],[F(1),F(347,12),F(2725,12),F(243)])]
    if gaps:
        examples=[([200,43,186],[F(1),F(2893,12),F(239,12),F(238)]),
                  ([43,200,186],[F(1),F(2893,12),F(237),F(251,12)]),
                  ([186,200,43],[F(1),F(19),F(237),F(243)])]
    report=[]
    for triple,point in examples:
        x,y,z=triple;p,e,f,g=point;caps=[500-x-y,500-x-z,500-y-z]
        assert p==1 and 0<=e<=caps[0] and 0<=f<=caps[1] and 0<=g<=caps[2]
        assert p+e+f+g<=500 and p+e+g>=x+z and p+f+g>=x+y
        weights=[p,x-p,F(y),F(z),e,f,g,caps[2]-g]
        masks=[11,3,5,6,9,10,12,4]
        assert all(q>0 for q in weights)
        cells=list(zip(masks,weights))+[(1,caps[0]-e),(2,caps[1]-f),(8,500-p-e-f-g)]
        assert all(q>=0 for m,q in cells)
        assert all(sum(q for m,q in cells if m>>j&1)==500 for j in range(4))
        pairs={(i,j):sum(q for m,q in cells if m>>i&1 and m>>j&1) for i,j in combinations(range(4),2)}
        if gaps:
            assert all(v<lo or v>hi for v in pairs.values() for lo,hi in ((98,106),(F(267,2),178),(216,237)))
        good=[]
        for tri in combinations(range(4),3):
            if sum(q for m,q in cells if all(m>>j&1 for j in tri))==0:
                total=sum(pairs[i,j] for i,j in combinations(tri,2));assert total>=429;good.append(str(total))
        assert pairs[0,1]==x and pairs[0,2]==y and pairs[1,2]==z
        assert x+y+z-1==428
        edges=[(i,j) for i,j in combinations(range(8),2) if masks[i]|masks[j]==15]
        assert set(edges)=={(0,2),(0,3),(0,6),(0,7),(1,6),(2,5),(3,4)}
        den=1
        for q in weights:den=den*q.denominator//gcd(den,q.denominator)
        integer_weights=[int(q*den) for q in weights]
        lower=None;count=0
        for c in range(18):
            for a,b,d in product(compat[c],repeat=3):
                labs=[c,blocks[d],a,b,blocks[b],blocks[a],d,blocks[c]]
                value=max(sum(w*cost[t][q] for w,t in zip(integer_weights,labs)) for q in range(10))
                assert value>428*12*den
                lower=value if lower is None else min(lower,value);count+=1
        assert count==16527
        bound=F(lower,12*den)
        report.append({'triple':triple,'response':list(map(str,point)),
                       'templates':count,'certified_lower_bound':str(bound),
                       'good_triple_sums':good})
        print('PASS:',triple,'all 16527 label templates; lower bound',bound,'> 428; all relevant cells positive.',flush=True)
    return report


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--gaps',action='store_true');args=parser.parse_args()
    result=check(args.gaps)
    Path('logs/astra_minimum_response_obstructions%s.json'%('_gaps' if args.gaps else '')).write_text(json.dumps(result,indent=2))
