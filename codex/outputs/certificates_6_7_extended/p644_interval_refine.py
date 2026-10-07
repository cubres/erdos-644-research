"""Refine remaining intersection intervals, preserving the chronological proof."""
from fractions import Fraction as F
from pathlib import Path
import json,time
from p644_interval_padded import merge,allowed
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions
from p644_spectrum_fast import certify_box


def run():
    data=json.loads(Path('logs/astra_static_template_facets_v3.json').read_text())
    rs=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions()
    src=json.loads(Path('logs/astra_interval_padded_31_36.json').read_text())
    beta=F(src['budget']);steps=list(src['steps']);excluded=[tuple(map(F,p)) for p in src['excluded']]
    todo=[(F(i,1000),F(i+1,1000)) for i in list(range(195,220))+list(range(370,400))+list(range(480,500))]
    start=time.monotonic();failures=[]
    for turn in range(3):
        failures=[]
        for a,b in todo:
            if any(l<=a and b<=h for l,h in excluded):continue
            cs=[(2-beta-a)/2]+[end for _,end in excluded]+[F(i,1000) for i in range(300,501,5)]
            success=None;bad=[]
            for u in dict.fromkeys(cs):
                v=2-beta-a-u
                if not(1-beta<=u<=1-b and b-a<=v<=1-a):continue
                records=[];good=True
                for yl,yh in allowed(u,excluded):
                    if not good:break
                    for zl,zh in allowed(v,excluded):
                        q=certify_box(rs,beta,(a,yl,zl),(b,yh,zh),limit=5000,depth_limit=55)
                        if q['status']!='COVERED':good=False;bad.append({'u':str(u),'box':[str(yl),str(yh),str(zl),str(zh)],'failure':q});break
                        records.append({'y':[str(yl),str(yh)],'z':[str(zl),str(zh)],'proof':q})
                if good:success={'interval':[str(a),str(b)],'u':str(u),'v_at_left':str(v),'boxes':records};break
            if success:
                steps.append(success);excluded=merge(excluded+[(a,b)])
                print('EXCLUDED',a,b,'known',[(str(x),str(y)) for x,y in excluded],flush=True)
            else:failures.append((a,b))
        out={**src,'steps':steps,'excluded':[[str(a),str(b)] for a,b in excluded],'unclosed_slabs':[[str(a),str(b)] for a,b in failures]}
        Path('logs/astra_interval_refine_31_36.json').write_text(json.dumps(out,separators=(',',':')))
        print('ROUND',turn,'remaining',len(failures),'seconds',round(time.monotonic()-start,1),flush=True)
        if len(failures)==len(todo) or not failures:break
        todo=failures
    print('DONE',len(steps),'steps; excluded',out['excluded'],flush=True)


if __name__=='__main__':run()
