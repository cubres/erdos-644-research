"""Discovery: exclude pair intervals using all previously excluded intervals.

Every accepted geometric box has the same exact affine-leaf proof as the
first-interval certificate. A complete independent replay and a global
rounding proof are still required before using this as a new theorem.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions
from p644_spectrum_fast import certify_box


def merge(intervals):
    out=[]
    for a,b in sorted(intervals):
        if out and a<=out[-1][1]:out[-1]=(out[-1][0],max(b,out[-1][1]))
        else:out.append((a,b))
    return out


def allowed(cap,excluded):
    out=[];start=F(0)
    for a,b in excluded:
        if a>cap:break
        if start<a:out.append((start,min(a,cap)))
        start=max(start,b)
    if start<cap:out.append((start,cap))
    if not out and cap==0:out=[(F(0),F(0))]
    return out


def run(beta=F(173,200)):
    data=json.loads(Path('logs/astra_static_template_facets_v3.json').read_text())
    rs=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions();excluded=[];steps=[];start=time.monotonic()
    todo=[(F(i,200),F(i+1,200)) for i in range(30,100)]
    output='logs/astra_interval_padded_'+str(beta).replace('/','_')+'.json'
    for iteration in range(4):
        failures=[]
        for a,b in todo:
            cs=[(2-beta-a)/2,F(7,20),F(2,5),F(3,10),2-beta-a-F(99,200),2-beta-a-F(37,100)]
            cs+=[end for _,end in excluded]
            cs+=[F(i,100) for i in range(20,51,5)]
            success=None
            for u in dict.fromkeys(cs):
                v=2-beta-a-u
                if not(1-beta<=u<=1-b and v>=b-a and v<=1-a):continue
                boxes=[];good=True
                for yl,yh in allowed(u,excluded):
                    if not good:break
                    for zl,zh in allowed(v,excluded):
                        q=certify_box(rs,beta,(a,yl,zl),(b,yh,zh),limit=3000,depth_limit=45)
                        if q['status']!='COVERED':good=False;break
                        boxes.append({'y':[str(yl),str(yh)],'z':[str(zl),str(zh)],'proof':q})
                if good:
                    success={'interval':[str(a),str(b)],'u':str(u),'v_at_left':str(v),'boxes':boxes};break
            if success:
                steps.append(success);excluded=merge(excluded+[(a,b)])
                print('EXCLUDED',str(a),str(b),'known',[(str(x),str(y)) for x,y in excluded],
                      'seconds',round(time.monotonic()-start,1),flush=True)
            else:failures.append((a,b))
        Path(output).write_text(json.dumps({'status':'PARTIAL','budget':str(beta),'adaptive_version':6,
          'static_templates':[r['triangle'] for r in data],'steps':steps,
          'excluded':[[str(a),str(b)] for a,b in excluded],'unclosed_slabs':[[str(a),str(b)] for a,b in failures]},separators=(',',':')))
        if len(failures)==len(todo) or not failures:break
        todo=failures
    print('DONE',len(steps),'steps; excluded',[(str(a),str(b)) for a,b in excluded],flush=True)

if __name__=='__main__':
    import sys
    run(F(sys.argv[1]) if len(sys.argv)>1 else F(31,36))
