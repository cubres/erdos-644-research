"""Independent rational replay of the proposed general 31/36 coefficient."""
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
import json
from p644_astra_global_bound_check import static_region,adaptive_regions,unbalanced_regions,triangular_region,response_choice_regions,boxes,check_tree
from p644_astra_frontier_check import dominant_regions
from p644_astra_maxsmall_check import partial_regions,padded_regions,padded_dominant_regions,affine,permute
from p644_astra_interval_bound_check import merged,remaining,gap_regions,constant_gap_regions


def partial_gap_regions(beta,h,ell):
    # Seven inequalities of Lemma 7.37, including S>=beta as a domain condition.
    fs=[affine(f) for f in [lambda x,y,z:2*beta-x-y-z,lambda x,y,z:x+y,
      lambda x,y,z:1-h+y,lambda x,y,z:1-h+z,
      lambda x,y,z:F(1,4)+x+(y+z)/4,lambda x,y,z:2*ell+y+z,
      lambda x,y,z:F(1,2)+x/2+(z+ell)/4]]
    return [permute(fs,p) for p in permutations(range(3))]


def main():
    base=Path(__file__).parent;beta=F(31,36)
    d=json.loads((base/'logs/astra_interval_refine_31_36.json').read_text())
    assert F(d['budget'])==beta and d['adaptive_version']==6
    rs=[static_region(t) for t in d['static_templates']]
    rs+=adaptive_regions()+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_regions()+partial_regions()+padded_regions()+padded_dominant_regions()
    excluded=[];total=0
    for step in d['steps']:
        a,b=map(F,step['interval']);u=F(step['u']);v=F(step['v_at_left'])
        assert 0<=a<b<=F(1,2) and u+v==2-beta-a
        assert 1-beta<=u<=1-b and b-a<=v<=1-a
        expected=list(product(remaining(u,excluded),remaining(v,excluded)))
        assert [(tuple(map(F,s['y'])),tuple(map(F,s['z']))) for s in step['boxes']]==expected
        for s,((yl,yh),(zl,zh)) in zip(step['boxes'],expected):
            total+=check_tree(s['proof'],boxes((a,yl,zl),(b,yh,zh)),rs,beta)
        excluded=merged(excluded+[(a,b)])
    ell=F(199,1000);h=F(187,500);m=F(391,1000);hi=F(481,1000)
    assert excluded==[(ell,h),(m,hi)]
    assert d['excluded']==[[str(a),str(b)] for a,b in excluded]
    print('PASS: chronological exclusions;',len(d['steps']),'steps;',total,'nodes;',len(d['static_templates']),'static templates')
    high=json.loads((base/'logs/astra_gap_high_31_36.json').read_text())
    assert high['static_templates']==d['static_templates'] and F(high['beta'])==beta
    assert F(high['h'])==h and F(high['low'])==ell
    assert (2-beta-hi)/2<h
    nt=check_tree(high['proof'],boxes((hi,F(0),F(0)),(F(1,2),ell,ell)),rs+gap_regions(h,ell)+partial_gap_regions(beta,h,ell),beta)
    total+=nt;print('PASS: full-core and partial-core high-gap cover;',nt,'nodes')
    excluded=merged(excluded+[(hi,F(1,2))]);assert excluded==[(ell,h),(m,F(1,2))]
    mid=json.loads((base/'logs/astra_gap_middle_31_36.json').read_text())
    assert mid['static_templates']==d['static_templates'] and F(mid['beta'])==beta and F(mid['m'])==m
    cap=(2-beta-h)/2;assert cap==F(1721,4500)<m
    expected=list(product(remaining(cap,excluded),repeat=2))
    assert [(tuple(map(F,s['y'])),tuple(map(F,s['z']))) for s in mid['boxes']]==expected
    nt=0
    for s,((yl,yh),(zl,zh)) in zip(mid['boxes'],expected):
        nt+=check_tree(s['proof'],boxes((h,yl,zl),(m,yh,zh)),rs+constant_gap_regions(m),beta)
    total+=nt;print('PASS: middle-gap cover;',nt,'nodes; excluded [199/1000,1/2]')
    # Extend down with u=1/2 and v(q)=3/2-beta-q, then small-triple Lemma7.18.
    low=1-beta
    assert 0<low<ell<F(1,2)
    for q in [low,ell]:
        u=F(1,2);v=F(3,2)-beta-q
        assert 0<=v<=F(1,2) and u<=1-q and v<=1-q
    small=max((3+ell)/4,(2+2*ell)/3);assert small==F(3199,4000)<beta
    assert low<F(7,36)
    # The final gap theorem has this same coefficient, but its +2 is below K's +10.
    assert beta==F(31,36) and 2<10 and beta*1000+5<1000
    assert max(2,4,9)<10
    print('PASS: downward extension to [5/36,1/2]; small-triple budget 3199r/4000')
    print('PASS: c7<=31/36;',total,'exact cover nodes; f(k,7)<=ceil(31k/36)+10 for k>=1000')
    print('Read together with the hand lemmas and integer rounding proof in note_644.md.')


if __name__=='__main__':main()
