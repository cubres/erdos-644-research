"""Chronological discovery below6/7, with the complete current lemma menu.

Accepted covers are exact, but require independent replay before being cited.
Failures describe only the supplied finite sufficient-region menu.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys,time
from p644_interval_padded import merge,allowed
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions,gap_regions,partial_gap_regions
from p644_gap_one_trace import regions as one
from p644_gap_two_triples import regions as two
from p644_gap_trace_dichotomy import regions as dichotomy
from p644_interval_finish_one_trace import constant_regions
from p644_spectrum_fast import certify_box


def run(beta):
    data=json.loads(Path('logs/astra_static_template_facets_v3.json').read_text())
    base=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions()
    suffix=str(beta).replace('/','_');output=Path('logs/astra_interval_below_6_7_'+suffix+'.json')
    steps=[];excluded=[];start=time.monotonic()
    seed=json.loads(Path('logs/astra_interval_finished_6_7.json').read_text())
    todo=list(dict.fromkeys(tuple(map(F,s['interval'])) for s in seed['steps']))
    todo+=list(dict.fromkeys((F(i,1000),F(i+1,1000)) for i in range(140,500)))
    for turn in range(4):
        added=0;failures=[];witnesses=[]
        for a,b in todo:
            if any(l<=a and b<=h for l,h in excluded):continue
            rs=list(base)
            for ell,h in excluded:rs+=gap_regions(h,ell)+partial_gap_regions(beta,h,ell)+one(beta,h,ell)+two(beta,h,ell)
            m=excluded[-1][0] if excluded and excluded[-1][1]==F(1,2) else None
            if m is not None:rs+=constant_regions(m)
            pars=None
            if m is not None and len(excluded)>1:
                ell,h=excluded[0];pars={'ell':str(ell),'h':str(h),'m':str(m)}
                rs+=dichotomy(beta,h,ell,m)
            cs=[(2-beta-a)/2]+[h for _,h in excluded]+[F(i,1000) for i in range(250,501,5)]
            success=None;last=[]
            for u in dict.fromkeys(cs):
                v=2-beta-a-u
                if not(1-beta<=u<=1-b and b-a<=v<=1-a):continue
                records=[];good=True
                for yl,yh in allowed(u,excluded):
                    if not good:break
                    for zl,zh in allowed(v,excluded):
                        q=certify_box(rs,beta,(a,yl,zl),(b,yh,zh),limit=3000,depth_limit=50,split_planes=[(-beta,F(1),F(1),F(1))])
                        if q['status']!='COVERED':
                            good=False;last.append({'u':str(u),'v':str(v),'result':q});break
                        records.append({'y':list(map(str,[yl,yh])),'z':list(map(str,[zl,zh])),'proof':q})
                if good:
                    success={'interval':list(map(str,[a,b])),'u':str(u),'v_at_left':str(v),'boxes':records,'prior_gaps':[[str(l),str(h)] for l,h in excluded],'two_triples':True}
                    if excluded:success['maximum_small']=str(m) if m is not None else None
                    if pars is not None:success['trace_dichotomy']=pars
                    break
            if success:
                steps.append(success);excluded=merge(excluded+[(a,b)]);added+=1
                print('EXCLUDED',a,b,'known',[(str(x),str(y)) for x,y in excluded],'seconds',round(time.monotonic()-start,1),flush=True)
                checkpoint={'budget':str(beta),'adaptive_version':10,'static_templates':[r['triangle'] for r in data],
                            'steps':steps,'excluded':[[str(l),str(h)] for l,h in excluded],'status':'PARTIAL'}
                output.with_suffix('.checkpoint.json').write_text(json.dumps(checkpoint,separators=(',',':')))
            else:
                failures.append((a,b));witnesses.append({'interval':list(map(str,[a,b])),'failures':last})
            if any(l<=F(1,4) and h==F(1,2) for l,h in excluded):break
        done=any(l<=F(1,4) and h==F(1,2) for l,h in excluded)
        out={'budget':str(beta),'adaptive_version':10,'static_templates':[r['triangle'] for r in data],
             'steps':steps,'excluded':[[str(a),str(b)] for a,b in excluded],
             'unclosed_slabs':[[str(a),str(b)] for a,b in failures],'status':'COVERED' if done else 'PARTIAL'}
        output.write_text(json.dumps(out,separators=(',',':')))
        output.with_suffix('.failures.json').write_text(json.dumps(witnesses,separators=(',',':')))
        print('ROUND',turn,'added',added,'remaining',len(failures),'seconds',round(time.monotonic()-start,1),flush=True)
        if done or not added:break
        todo=list(dict.fromkeys(failures))
    print('DONE',len(steps),'steps; excluded',out['excluded'],flush=True)


if __name__=='__main__':run(F(sys.argv[1]) if len(sys.argv)>1 else F(107,125))
