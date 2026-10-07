"""Finish the remaining 0.380--0.383 intersection interval at budget6/7."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json
from p644_interval_padded import allowed,merge
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions,gap_regions,partial_gap_regions
from p644_gap_one_trace import regions as one
from p644_gap_two_triples import regions as two
from p644_gap_trace_dichotomy import regions as dichotomy
from p644_interval_finish_one_trace import constant_regions
from p644_spectrum_fast import certify_box


def main():
    src=json.loads(Path('logs/astra_interval_two_triples_6_7.json').read_text())
    exc=[tuple(map(F,g)) for g in src['excluded']];assert exc==[(F(143,1000),F(19,50)),(F(383,1000),F(1,2))]
    beta=F(6,7);ell,h=exc[0];m=exc[1][0];a,b=h,m;u=(2-beta-a)/2;v=u
    data=json.loads(Path('logs/astra_static_template_facets_v3.json').read_text())
    rs=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions()
    for l,hh in exc:rs+=gap_regions(hh,l)+partial_gap_regions(beta,hh,l)+one(beta,hh,l)+two(beta,hh,l)
    rs+=constant_regions(m)+dichotomy(beta,h,ell,m)
    records=[]
    for yi,zi in product(allowed(u,exc),allowed(v,exc)):
        q=certify_box(rs,beta,(a,yi[0],zi[0]),(b,yi[1],zi[1]),limit=30000,depth_limit=65,split_planes=[(-beta,F(1),F(1),F(1))])
        print(yi,zi,{k:w if k!='nodes' else len(w) for k,w in q.items()},flush=True)
        assert q['status']=='COVERED'
        records.append({'y':list(map(str,yi)),'z':list(map(str,zi)),'proof':q})
    step={'interval':list(map(str,[a,b])),'u':str(u),'v_at_left':str(v),'boxes':records,'prior_gaps':src['excluded'],'two_triples':True,'maximum_small':str(m),'trace_dichotomy':{'ell':str(ell),'h':str(h),'m':str(m)}}
    exc=merge(exc+[(a,b)]);assert exc==[(ell,F(1,2))]
    out={**src,'adaptive_version':10,'steps':src['steps']+[step],'excluded':[[str(a),str(b)] for a,b in exc],'status':'COVERED'}
    Path('logs/astra_interval_finished_6_7.json').write_text(json.dumps(out,separators=(',',':')))
    print('DONE',len(out['steps']),'steps;',sum(len(r['proof']['nodes']) for r in records),'newnodes; excluded',out['excluded'],flush=True)


if __name__=='__main__':main()
