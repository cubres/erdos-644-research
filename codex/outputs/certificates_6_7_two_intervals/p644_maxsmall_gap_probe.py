"""Probe the largest small intersection using the current global gap menu.

This file is discovery only. The stated gaps require their own replay.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json,time
from p644_interval_padded import allowed
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions,gap_regions,partial_gap_regions
from p644_gap_one_trace import regions as one
from p644_gap_two_triples import regions as two
from p644_gap_trace_dichotomy import regions as dichotomy
from p644_interval_finish_one_trace import constant_regions
from p644_spectrum_fast import certify_box


def run():
    beta=F(107,125)
    exc=[(F(51,250),F(53,250)),(F(11,40),F(89,250)),(F(54,125),F(47,100))]
    data=json.loads(Path('logs/astra_static_template_facets_v3.json').read_text())
    base=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions()
    for ell,h in exc:base+=gap_regions(h,ell)+partial_gap_regions(beta,h,ell)+one(beta,h,ell)+two(beta,h,ell)
    todo=[(F(i,1000),F(i+1,1000),0) for i in reversed(range(284,500))]
    rows=[];failures=[];start=time.monotonic()
    while todo:
        a,b,depth=todo.pop()
        if any(l<=a and b<=h for l,h in exc):continue
        cap=min(b,(2-beta-a)/2);rs=base+constant_regions(b)
        for ell,h in exc:rs+=dichotomy(beta,h,ell,b)
        records=[];failure=None
        for yi,zi in product(allowed(cap,exc),repeat=2):
            q=certify_box(rs,beta,(a,yi[0],zi[0]),(b,yi[1],zi[1]),limit=2000,depth_limit=40)
            if q['status']!='COVERED':failure=q;break
            records.append({'y':list(map(str,yi)),'z':list(map(str,zi)),'proof':q})
        if failure is None:
            rows.append({'interval':list(map(str,[a,b])),'cap':str(cap),'boxes':records})
            print('COVER',str(a),str(b),'seconds',round(time.monotonic()-start,1),flush=True)
        elif depth<3:
            c=(a+b)/2;todo.append((c,b,depth+1));todo.append((a,c,depth+1))
        else:
            failures.append({'interval':list(map(str,[a,b])),'cap':str(cap),'failure':failure})
            print('FAILED',failures[-1],flush=True);break
    out={'budget':str(beta),'gaps':[[str(x) for x in g] for g in exc],'slabs':rows,'failures':failures,'status':'COVERED' if not failures else 'PARTIAL'}
    Path('logs/astra_maxsmall_gap_probe_107_125.json').write_text(json.dumps(out,separators=(',',':')))
    print('DONE',out['status'],len(rows),'slabs',round(time.monotonic()-start,1),'seconds',flush=True)


if __name__=='__main__':run()
