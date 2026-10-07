"""Chronological discovery with two surviving triple cells and prior gaps."""
from fractions import Fraction as F
from pathlib import Path
import json,time,sys
from p644_interval_padded import merge,allowed
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions,gap_regions,partial_gap_regions
from p644_gap_one_trace import regions as one_trace_regions
from p644_gap_two_triples import regions as two_triple_regions
from p644_interval_finish_one_trace import constant_regions
from p644_spectrum_fast import certify_box


def run(beta=F(6,7)):
    data=json.loads(Path('logs/astra_static_template_facets_v3.json').read_text())
    base=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions()
    suffix=str(beta).replace('/','_');src=json.loads(Path('logs/astra_interval_one_trace_'+suffix+'.json').read_text())
    steps=list(src['steps']);excluded=[tuple(map(F,p)) for p in src['excluded']]
    if beta==F(6,7):
        ep=json.loads(Path('logs/astra_two_triples_endpoint_6_7.json').read_text())
        assert ep['prior_gaps']==[[str(a),str(b)] for a,b in excluded]
        steps.append(ep);excluded=merge(excluded+[tuple(map(F,ep['interval']))])
    todo=[(F(i,1000),F(i+1,1000)) for i in range(140,500)]
    start=time.monotonic()
    for turn in range(4):
        added=0;failures=[]
        for a,b in todo:
            if any(l<=a and b<=h for l,h in excluded):continue
            rs=list(base)
            for ell,h in excluded:rs+=gap_regions(h,ell)+partial_gap_regions(beta,h,ell)+one_trace_regions(beta,h,ell)+two_triple_regions(beta,h,ell)
            m=excluded[-1][0] if excluded[-1][1]==F(1,2) else None
            if m is not None:rs+=constant_regions(m)
            cs=[(2-beta-a)/2]+[end for _,end in excluded]+[F(i,1000) for i in range(250,501,5)]
            success=None
            for u in dict.fromkeys(cs):
                v=2-beta-a-u
                if not(1-beta<=u<=1-b and b-a<=v<=1-a):continue
                records=[];good=True
                for yl,yh in allowed(u,excluded):
                    if not good:break
                    for zl,zh in allowed(v,excluded):
                        q=certify_box(rs,beta,(a,yl,zl),(b,yh,zh),limit=7000,depth_limit=60,split_planes=[(-beta,F(1),F(1),F(1))])
                        if q['status']!='COVERED':good=False;break
                        records.append({'y':[str(yl),str(yh)],'z':[str(zl),str(zh)],'proof':q})
                if good:
                    success={'interval':[str(a),str(b)],'u':str(u),'v_at_left':str(v),'boxes':records,'prior_gaps':[[str(l),str(h)] for l,h in excluded],'two_triples':True,'maximum_small':str(m) if m is not None else None};break
            if success:
                steps.append(success);excluded=merge(excluded+[(a,b)]);added+=1
                print('EXCLUDED',a,b,'known',[(str(x),str(y)) for x,y in excluded],'seconds',round(time.monotonic()-start,1),flush=True)
            else:failures.append((a,b))
            if any(l<=F(1,4) and h==F(1,2) for l,h in excluded):break
        done=any(l<=F(1,4) and h==F(1,2) for l,h in excluded)
        out={**src,'adaptive_version':9,'steps':steps,'excluded':[[str(a),str(b)] for a,b in excluded],'unclosed_slabs':[[str(a),str(b)] for a,b in failures],'status':'COVERED' if done else 'PARTIAL'}
        Path('logs/astra_interval_two_triples_'+suffix+'.json').write_text(json.dumps(out,separators=(',',':')))
        print('ROUND',turn,'added',added,'remaining',len(failures),'seconds',round(time.monotonic()-start,1),flush=True)
        if done or not added:break
        todo=failures
    print('DONE',len(steps),'steps; excluded',out['excluded'],flush=True)


if __name__=='__main__':run(F(sys.argv[1]) if len(sys.argv)>1 else F(6,7))
