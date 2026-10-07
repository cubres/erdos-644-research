"""Discovery of final intersection-gap stages at beta=31/36."""
from fractions import Fraction as F
from pathlib import Path
import json
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions,gap_regions,partial_gap_regions
from p644_spectrum_fast import certify_box


def main():
    data=json.loads(Path('logs/astra_static_template_facets_v3.json').read_text())
    rs=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions()
    templates=[r['triangle'] for r in data];beta=F(31,36);h=F(187,500);ell=F(199,1000)
    high=certify_box(rs+gap_regions(h,ell)+partial_gap_regions(beta,h,ell),beta,(F(481,1000),F(0),F(0)),(F(1,2),ell,ell),limit=30000,depth_limit=65,split_planes=[(-beta,F(1),F(1),F(1))])
    Path('logs/astra_gap_high_31_36.json').write_text(json.dumps({'beta':str(beta),'h':str(h),'low':str(ell),'static_templates':templates,'proof':high},separators=(',',':')))
    print('HIGH',{k:v if k!='nodes' else len(v) for k,v in high.items()},flush=True)
    if high['status']!='COVERED':return
    m=F(391,1000);cond=[]
    for z,fs in enumerate(response_choice_regions()):
        g=fs[:-1]
        for j in range(3):
            if j==z:continue
            f=[m,F(0),F(0),F(0)];f[j+1]=1;g.append(tuple(f))
        cond.append(g)
    cap=(2-beta-h)/2;rows=[]
    for yl,yh in [(F(0),ell),(h,cap)]:
        for zl,zh in [(F(0),ell),(h,cap)]:
            q=certify_box(rs+cond,beta,(h,yl,zl),(m,yh,zh),limit=30000,depth_limit=60)
            rows.append({'y':list(map(str,[yl,yh])),'z':list(map(str,[zl,zh])),'proof':q})
            print('MIDDLE',yl,yh,zl,zh,{k:v if k!='nodes' else len(v) for k,v in q.items()},flush=True)
    Path('logs/astra_gap_middle_31_36.json').write_text(json.dumps({'beta':str(beta),'m':str(m),'static_templates':templates,'boxes':rows},separators=(',',':')))


if __name__=='__main__':main()
