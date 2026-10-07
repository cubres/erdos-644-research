"""Reproduce the two final exact covers for the 431/500 general bound."""
from fractions import Fraction as F
from pathlib import Path
import json
from p644_case_cover import regions,unbalanced_regions,triangular_region,response_choice_regions,dominant_pair_regions,partial_core_regions,padded_pair_regions,padded_dominant_regions,gap_regions
from p644_spectrum_fast import certify_box


def main():
    data=json.loads(Path('logs/astra_static_template_facets_v3.json').read_text())
    rs=regions(data)+unbalanced_regions()+[triangular_region()]+response_choice_regions()+dominant_pair_regions()+partial_core_regions()+padded_pair_regions()+padded_dominant_regions()
    templates=[r['triangle'] for r in data];beta=F(431,500)
    high=certify_box(rs+gap_regions(F(3,8),F(9,50)),beta,(F(12,25),F(0),F(0)),(F(1,2),F(9,50),F(9,50)),limit=30000,depth_limit=60)
    assert high['status']=='COVERED'
    Path('logs/astra_gap_high_431_500.json').write_text(json.dumps({'beta':str(beta),'h':'3/8','low':'9/50','static_templates':templates,'proof':high},separators=(',',':')))
    cond=[]
    for z,fs in enumerate(response_choice_regions()):
        g=fs[:-1]
        for j in range(3):
            if j==z:continue
            f=[F(39,100),F(0),F(0),F(0)];f[j+1]=1;g.append(tuple(f))
        cond.append(g)
    rows=[]
    for yl,yh in [(F(0),F(9,50)),(F(3,8),F(763,2000))]:
        for zl,zh in [(F(0),F(9,50)),(F(3,8),F(763,2000))]:
            q=certify_box(rs+cond,beta,(F(3,8),yl,zl),(F(39,100),yh,zh),limit=30000,depth_limit=60)
            assert q['status']=='COVERED'
            rows.append({'y':list(map(str,[yl,yh])),'z':list(map(str,[zl,zh])),'proof':q})
    Path('logs/astra_gap_middle_431_500.json').write_text(json.dumps({'beta':str(beta),'m':'39/100','static_templates':templates,'boxes':rows},separators=(',',':')))
    print('COVERED: high',len(high['nodes']),'nodes; middle',sum(len(r['proof']['nodes']) for r in rows),'nodes')


if __name__=='__main__':main()
