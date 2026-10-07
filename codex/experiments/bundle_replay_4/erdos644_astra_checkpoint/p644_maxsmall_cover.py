"""Discovery using a largest pair intersection m<=r/2.

All family pair intersections are <=m or >r/2. The new conditional response
lemma replaces the last inequality of Lemma 7.26 by T>=m+max(x,y).
Independent replay and a complete integer global proof are still required.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions
from p644_spectrum_fast import certify_box


def conditional_regions():
    base=response_choice_regions();out=[]
    for z,fs in enumerate(base):
        g=fs[:-1]
        for j in range(3):
            if j==z:continue
            row=[F(0)]*4;row[1]=1;row[j+1]+=1;g.append(tuple(row))
        out.append(g)
    return out


def run(beta=F(31,36)):
    data=json.loads(Path('logs/astra_static_template_facets_v2.json').read_text())
    rs=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+conditional_regions()+dominant_pair_regions()
    rows=[];start=time.monotonic();todo=[(F(i,200),F(i+1,200),0) for i in reversed(range(54,100))]
    failures=[]
    while todo:
        a,b,depth=todo.pop();cap=min(b,(2-beta-a)/2)
        q=certify_box(rs,beta,(a,F(0),F(0)),(b,cap,cap),limit=10000,depth_limit=55)
        if q['status']=='COVERED':
            rows.append({'interval':[str(a),str(b)],'cap':str(cap),'proof':q})
            print('COVER',float(a),float(b),'nodes',len(q['nodes']),flush=True)
        elif depth<4:
            mid=(a+b)/2;todo.append((mid,b,depth+1));todo.append((a,mid,depth+1))
        else:
            failures.append({'interval':[str(a),str(b)],'cap':str(cap),'failure':q})
            print('FAIL',str(a),str(b),q,flush=True)
            # One concrete hole is enough to determine the next lemma to seek.
            break
    out={'status':'PARTIAL' if failures else 'COVERED','budget':str(beta),'slabs':rows,'failures':failures,
         'static_templates':[r['triangle'] for r in data]}
    Path('logs/astra_maxsmall_dominant_'+str(beta).replace('/','_')+'.json').write_text(json.dumps(out,separators=(',',':')))
    print('DONE',out['status'],round(time.monotonic()-start,1),flush=True)

if __name__=='__main__':run()
