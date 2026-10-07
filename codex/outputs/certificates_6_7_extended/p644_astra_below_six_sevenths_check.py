"""Independent replay of partial0.856 gaps and a precise finite-menu hole.

Standard library only. The hole rejects this menu at the displayed triple;
it is not a lower bound on f(k,7) or a barrier to different cap choices.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from p644_astra_one_trace_check import check,static_region,adaptive_regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_regions,partial_regions,padded_regions,padded_dominant_regions,gap_regions,partial_gap_regions,one_trace_regions,two_triple_regions,constant_gap_regions,trace_dichotomy_regions


def main():
    root=Path(__file__).parent
    path=root/'logs/astra_below_6_7_verified_35_steps.json'
    result=check(path)
    assert result['budget']=='107/125' and not result['closed']
    d=json.loads(path.read_text());beta=F(d['budget']);gaps=[tuple(map(F,g)) for g in d['excluded']]
    expected=[(F(51,250),F(53,250)),(F(11,40),F(89,250)),(F(54,125),F(47,100))]
    assert gaps==expected
    rs=[static_region(t) for t in d['static_templates']]
    rs+=adaptive_regions()+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_regions()+partial_regions()+padded_regions()+padded_dominant_regions()
    for ell,h in gaps:rs+=gap_regions(h,ell)+partial_gap_regions(beta,h,ell)+one_trace_regions(beta,h,ell)+two_triple_regions(beta,h,ell)
    x,y,z=point=(F(2,5),F(43,500),F(93,250));m=x
    rs+=constant_gap_regions(m)
    for ell,h in gaps:rs+=trace_dichotomy_regions(beta,h,ell,m)
    def value(f):return f[0]+sum(a*b for a,b in zip(f[1:],point))
    costs=[max(map(value,region)) for region in rs]
    assert min(costs)==F(2143,2500)>beta
    assert F(71,250)<x<=F(1,2)
    assert 0<=y<=z<=min(x,(2-beta-x)/2)
    assert all(not ell<=v<=h for v in point for ell,h in gaps)
    assert sum(point)==F(429,500)<2-beta-max(h-ell for ell,h in gaps)==F(1063,1000)
    print('PASS: exact finite-menu hole',list(map(str,point)))
    print('PASS:',len(rs),'independently reconstructed regions; minimum sufficient budget2143/2500 >107/125')
    print('PASS: largest-small and balanced-cap domains, all current gaps, and the minimum-sum upper bound')
    print('LIMITATION: this finite menu at one triple; different caps, initial requests and later adaptivity remain open')


if __name__=='__main__':main()
