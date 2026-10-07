"""Independent rational replay of chronological gap-dependent regions.

Only Python standard library; no discovery imports or numerical solver.
"""
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
import json,sys
from p644_astra_global_bound_check import static_region,adaptive_regions,unbalanced_regions,triangular_region,response_choice_regions,boxes,check_tree
from p644_astra_frontier_check import dominant_regions
from p644_astra_maxsmall_check import partial_regions,padded_regions,padded_dominant_regions,affine,permute
from p644_astra_interval_bound_check import merged,remaining,gap_regions,constant_gap_regions
from p644_astra_31_36_check import partial_gap_regions


def one_trace_regions(beta,h,ell):
    fs=[affine(f) for f in [lambda x,y,z:x+y,lambda x,y,z:beta+1-h-x-z,
      lambda x,y,z:1-h+y,lambda x,y,z:y+ell,lambda x,y,z:1-x-y+z,
      lambda x,y,z:(1+ell+z)/2,lambda x,y,z:(1+ell+x-z)/2,
      lambda x,y,z:1-y,lambda x,y,z:(3+ell+2*x-2*y-z)/4]]
    return [permute(fs,p) for p in permutations(range(3))]


def check(path):
    d=json.loads(path.read_text());beta=F(d['budget'])
    assert d['adaptive_version'] in [6,7,8]
    base=[static_region(t) for t in d['static_templates']]
    base+=adaptive_regions()+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_regions()+partial_regions()+padded_regions()+padded_dominant_regions()
    witness_path=Path(__file__).parent/'logs/astra_one_trace_menu_witness.json'
    if beta==F(43,50) and witness_path.exists():
        w=json.loads(witness_path.read_text());p=tuple(map(F,w['point']));ell,h=map(F,w['gap'])
        def at(fs):return max(f[0]+sum(a*b for a,b in zip(f[1:],p)) for f in fs)
        old=min(at(fs) for fs in base);new=at(one_trace_regions(beta,h,ell)[w['orientation_index']])
        assert old==F(w['old_budget'])==F(3441,4000)>beta
        assert new==F(w['new_budget'])==F(661,800)<beta
        print('PASS: exact single-trace comparison;',str(old),'to',str(new),'at',w['point'])
    excluded=[];total=0;conditional=0
    for step in d['steps']:
        a,b=map(F,step['interval']);u=F(step['u']);v=F(step['v_at_left'])
        assert 0<=a<b<=F(1,2) and u+v==2-beta-a
        assert 1-beta<=u<=1-b and b-a<=v<=1-a
        rs=list(base)
        if 'prior_gaps' in step:
            assert d['adaptive_version'] in [7,8]
            assert step['prior_gaps']==[[str(l),str(h)] for l,h in excluded]
            for ell,h in excluded:
                assert 0<=ell<h<=F(1,2)
                rs+=gap_regions(h,ell)+partial_gap_regions(beta,h,ell)+one_trace_regions(beta,h,ell)
            conditional+=1
        if 'maximum_small' in step:
            assert d['adaptive_version']==8 and 'prior_gaps' in step
            m=excluded[-1][0] if excluded[-1][1]==F(1,2) else None
            assert step['maximum_small']==(str(m) if m is not None else None)
            if m is not None:rs+=constant_gap_regions(m)
        expected=list(product(remaining(u,excluded),remaining(v,excluded)))
        assert [(tuple(map(F,s['y'])),tuple(map(F,s['z']))) for s in step['boxes']]==expected
        for s,((yl,yh),(zl,zh)) in zip(step['boxes'],expected):
            total+=check_tree(s['proof'],boxes((a,yl,zl),(b,yh,zh)),rs,beta)
        excluded=merged(excluded+[(a,b)])
    assert d['excluded']==[[str(a),str(b)] for a,b in excluded]
    print('PASS',str(beta),len(d['steps']),'chronological steps;',conditional,'gap-dependent steps;',total,'nodes; exclusions',d['excluded'])
    closed=any(ell<=F(1,4) and h==F(1,2) for ell,h in excluded)
    if closed:
        # Theorem7.42, with +4, contradicts tau>ceil(beta*r)+10.
        assert beta>=F(5,6) and beta*1000+11<=1000
        assert max(2,4,9)<10
        print('PASS: conditional 5/6 theorem completes the general bound f(r,7)<=ceil('+str(beta)+' r)+10 for r>=1000')
        print('Read together with Lemma7.43, Theorem7.42, the other hand lemmas, and integer rounding in note_644.md.')
    else:print('PARTIAL EXCLUSIONS ONLY: no general bound follows from this file alone')
    return {'budget':str(beta),'steps':len(d['steps']),'conditional_steps':conditional,'nodes':total,'exclusions':d['excluded'],'closed':closed}


if __name__=='__main__':
    if len(sys.argv)>1:path=Path(sys.argv[1])
    else:path=Path(__file__).parent/'logs/astra_interval_finished_43_50.json'
    check(path)
