"""Exact replay of the current finite-menu hole at budget 31/36.

This imports only an independent certificate checker, never discovery code.
It certifies a limit of this particular menu, not of the general problem.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from p644_astra_global_bound_check import static_region,adaptive_regions,unbalanced_regions,triangular_region,response_choice_regions


def conditional_regions():
    out=[]
    for z,fs in enumerate(response_choice_regions()):
        rowset=fs[:-1]
        for j in range(3):
            if j==z:continue
            row=[F(0)]*4;row[1]=1;row[j+1]+=1;rowset.append(tuple(row))
        out.append(rowset)
    return out


def dominant_regions():
    out=[]
    for x in range(3):
        y,z=[i for i in range(3) if i!=x]
        fs=[(F(1,2),F(1,2),F(1,2),F(1,2))]
        for plus,minus in [(y,z),(z,y)]:
            f=[F(1),F(0),F(0),F(0)];f[x+1]=-1;f[plus+1]=1;f[minus+1]=-1;fs.append(tuple(f))
        f=[F(1,3),F(0),F(0),F(0)];f[x+1]=1;fs.append(tuple(f));out.append(fs)
    return out


def main():
    base=Path(__file__).parent;d=json.loads((base/'logs/astra_maxsmall_dominant_31_36.json').read_text())
    assert d['status']=='PARTIAL' and F(d['budget'])==F(31,36) and len(d['failures'])==1
    f=d['failures'][0]['failure'];assert f['status']=='UNCOVERED'
    p=tuple(map(F,f['point']));beta=F(31,36);m=p[0]
    assert F(27,100)<=m<=F(1,2)
    assert all(0<=x<=min(m,(2-beta-m)/2) for x in p[1:])
    assert all(p[i]+p[j]<=1 for i in range(3) for j in range(i+1,3))
    rs=[static_region(t) for t in d['static_templates']]
    rs+=adaptive_regions()+unbalanced_regions()+[triangular_region()]+response_choice_regions()+conditional_regions()+dominant_regions()
    values=[max(g[0]+sum(a*b for a,b in zip(g[1:],p)) for g in fs) for fs in rs]
    value=min(values);assert value==F(f['cost'])>beta
    assert sum(p)>beta
    print('PASS: exact finite-menu hole;',len(d['static_templates']),'static templates;',len(rs),'regions')
    print('point',','.join(map(str,p)),'menu budget',str(value),'>31/36; pair-cell core exceeds budget')
    print('LIMITATION: this rejects only the stated sufficient-region menu, not other avoidance strategies or the 3/4 conjecture')

if __name__=='__main__':main()
