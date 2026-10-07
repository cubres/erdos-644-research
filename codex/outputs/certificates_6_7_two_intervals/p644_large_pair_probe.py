"""Explore chronological exclusions above half the rank.

The cap construction itself works up to q<=beta; old discovery restricted
the initial pair to q<=1/2. A new independent replay is needed for this file.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time
from p644_interval_padded import merge,allowed
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions,gap_regions,partial_gap_regions
from p644_gap_one_trace import regions as one
from p644_gap_two_triples import regions as two
from p644_gap_trace_dichotomy import regions as dichotomy
from p644_interval_finish_one_trace import constant_regions
from p644_spectrum_fast import certify_box


def run():
    beta=F(107,125)
    src=json.loads(Path('logs/astra_below_6_7_verified_35_steps.json').read_text())
    data=json.loads(Path('logs/astra_static_template_facets_v3.json').read_text())
    base=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions()
    steps=list(src['steps']);exc=[tuple(map(F,g)) for g in src['excluded']];start=time.monotonic()
    todo=[(F(i,1000),F(i+5,1000)) for i in range(500,850,5)]
    todo+=[(F(i,1000),F(i+1,1000)) for i in range(140,500)]
    for turn in range(3):
        added=0;failures=[]
        for a,b in todo:
            if any(l<=a and b<=h for l,h in exc):continue
            rs=list(base)
            for ell,h in exc:rs+=gap_regions(h,ell)+partial_gap_regions(beta,h,ell)+one(beta,h,ell)+two(beta,h,ell)
            ms=[ell for ell,h in exc if ell<=F(1,2)<=h]
            m=min(ms) if ms else None
            if m is not None:rs+=constant_regions(m)
            cs=[(2-beta-a)/2]+[h for _,h in exc]+[F(i,1000) for i in range(145,501,10)]
            success=None;last=[]
            for u in dict.fromkeys(cs):
                v=2-beta-a-u
                if not(1-beta<=u<=1-b and b-a<=v<=1-a):continue
                records=[];good=True
                for yi in allowed(u,exc):
                    if not good:break
                    for zi in allowed(v,exc):
                        q=certify_box(rs,beta,(a,yi[0],zi[0]),(b,yi[1],zi[1]),limit=500,depth_limit=30)
                        if q['status']!='COVERED':
                            good=False;last.append({'u':str(u),'v':str(v),'result':q});break
                        records.append({'y':list(map(str,yi)),'z':list(map(str,zi)),'proof':q})
                if good:
                    success={'interval':list(map(str,[a,b])),'u':str(u),'v_at_left':str(v),'boxes':records,'prior_gaps':[[str(l),str(h)] for l,h in exc],'two_triples':True,'maximum_small':str(m) if m is not None else None}
                    break
            if success:
                steps.append(success);exc=merge(exc+[(a,b)]);added+=1
                print('EXCLUDED',a,b,'known',[(str(x),str(y)) for x,y in exc],'seconds',round(time.monotonic()-start,1),flush=True)
                out={**src,'adaptive_version':11,'steps':steps,'excluded':[[str(l),str(h)] for l,h in exc],'status':'PARTIAL'}
                Path('logs/astra_large_pair_107_125.checkpoint.json').write_text(json.dumps(out,separators=(',',':')))
            else:failures.append({'interval':list(map(str,[a,b])),'cap_failures':last})
            if any(ell<=F(71,250) and h>=F(1,2) for ell,h in exc):break
        Path('logs/astra_large_pair_107_125.failures.json').write_text(json.dumps(failures,separators=(',',':')))
        done=any(ell<=F(71,250) and h>=F(1,2) for ell,h in exc)
        print('ROUND',turn,'added',added,'remaining',len(failures),'seconds',round(time.monotonic()-start,1),flush=True)
        if done or not added:break
        todo=[tuple(map(F,s['interval'])) for s in failures]
    print('DONE',len(steps),'steps; excluded',[[str(l),str(h)] for l,h in exc],flush=True)


if __name__=='__main__':run()
