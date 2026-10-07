"""Independent exact replay of the expanded maximum-small-intersection menu.

No discovery module or numerical package is imported. A PARTIAL result proves
only the covered slabs and a hole in the finite menu, never a general bound.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json
from p644_astra_global_bound_check import static_region,adaptive_regions,unbalanced_regions,triangular_region,response_choice_regions,boxes,check_tree
from p644_astra_frontier_check import conditional_regions,dominant_regions


def affine(fun):
    zero=fun(F(0),F(0),F(0))
    return (zero,fun(F(1),F(0),F(0))-zero,fun(F(0),F(1),F(0))-zero,fun(F(0),F(0),F(1))-zero)


def permute(forms,order):
    out=[]
    for f in forms:
        row=[f[0],F(0),F(0),F(0)]
        for j,k in enumerate(order):row[k+1]=f[j+1]
        out.append(tuple(row))
    return out


def partial_regions():
    # The nine inequalities in the hand proof of Lemma 7.31, with r=1.
    fs=[affine(f) for f in [lambda x,y,z:x+y,lambda x,y,z:F(1,2)+x,lambda x,y,z:F(1,2)+y,
      lambda x,y,z:1+x-y-z,lambda x,y,z:1-x+y-z,lambda x,y,z:1-(x+y+z)/3,
      lambda x,y,z:(3+x+y+z)/5,lambda x,y,z:(1+x+y+2*z)/3,lambda x,y,z:(2+3*z)/4]]
    return [permute(fs,[j for j in range(3) if j!=z]+[z]) for z in range(3)]


def padded_regions():
    fs=[affine(f) for f in [lambda x,y,z:x+y+z,lambda x,y,z:F(1,2)+y,
       lambda x,y,z:(1+2*x-y+z)/2,lambda x,y,z:(1+2*x+y+3*z)/3]]
    return [permute(fs,p) for p in permutations(range(3))]


def padded_dominant_regions():
    fs=[affine(f) for f in [lambda x,y,z:x+y+z,lambda x,y,z:F(1,3)+x,
       lambda x,y,z:1-x+z,lambda x,y,z:(1+2*x+3*y+z)/3]]
    return [permute(fs,p) for p in permutations(range(3))]


def main():
    d=json.loads((Path(__file__).parent/'logs/astra_maxsmall_padded_dominant_31_36.json').read_text())
    beta=F(d['budget']);assert beta==F(31,36)
    rs=[static_region(t) for t in d['static_templates']]
    rs+=adaptive_regions()+unbalanced_regions()+[triangular_region()]+response_choice_regions()+conditional_regions()+dominant_regions()+partial_regions()+padded_regions()+padded_dominant_regions()
    end=F(27,100);nodes=0
    for s in d['slabs']:
        a,b=map(F,s['interval']);cap=F(s['cap'])
        assert a==end and a<b<=F(1,2);end=b
        assert cap==min(b,(2-beta-a)/2)
        nodes+=check_tree(s['proof'],boxes((a,F(0),F(0)),(b,cap,cap)),rs,beta)
    assert d['status']=='PARTIAL' and len(d['failures'])==1
    failure=d['failures'][0];a,b=map(F,failure['interval']);assert a==end and a<b<=F(1,2)
    f=failure['failure'];assert f['status']=='UNCOVERED';p=tuple(map(F,f['point']));m=p[0]
    assert a<=m<=b and all(0<=x<=min(m,(2-beta-m)/2) for x in p[1:])
    costs=[max(g[0]+sum(a*b for a,b in zip(g[1:],p)) for g in r) for r in rs]
    assert min(costs)==F(f['cost'])>beta
    print('PASS:',len(d['static_templates']),'static templates;',len(rs),'regions;',nodes,'exact cover nodes')
    print('PASS: covered maximum-small parameter slabs from 27/100 through',str(end))
    print('PASS: exact remaining finite-menu hole',list(map(str,p)),'cost',str(min(costs)))
    print('LIMITATION: the uncovered menu does not imply that other strategies or the general problem are obstructed')


if __name__=='__main__':main()
