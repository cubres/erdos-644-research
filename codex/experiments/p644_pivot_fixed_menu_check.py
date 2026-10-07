"""Exact bounded fixed-menu test after the focused inside-union pivot.

Tests the 35 integer compositions of 4 into four A deficits, at b=1,
all ordered retained four-row projections, both actual types and a sound
completion of noneligible types into their Fano containing stars.
No solver, floating point, or positive-mass cutoff is used.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json

T = F(219, 2)
P = F(111)
D1 = {1, 2, 3, 10, 12, 13, 14}
D2 = {6, 9, 11, 13}
ALLOWED = {0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 14}


def mask(label):
    return sum(1 << (int(r)-1) for r in label)


def actual_types(deficits):
    out = []
    for label, deficit in zip(('235','246','145','136'), deficits):
        old = mask(label)
        if F(37)-deficit:
            out.append((old | 1, F(37)-deficit))
        if deficit:
            out.append((old & ~1, F(deficit)))
    for label in ('1234','1256','3456'):
        out.append((mask(label) & ~1, F(33)))
        for r in label:
            defect = label.replace(r,'')
            out.append(((mask(defect) & ~1) | int(defect in ('123','124')), F(1)))
    assert sum(w for s,w in out) == 259
    assert [sum(w for s,w in out if s & (1 << r)) for r in range(6)] == [146]*6
    return out


def containing_types(deficits):
    d1,d2,d3,d4 = deficits
    return [(mask('1235'),37-d1),(mask('235'),d1),(mask('123'),F(1)),
            (mask('1246'),37-d2),(mask('246'),d2),(mask('124'),F(1)),
            (mask('3456'),F(33))]+[(mask(s),F(1))for s in ('456','356','346','345')]+[
            (mask('145'),F(37)),(mask('136'),F(37)),
            (mask('234'),F(35)),(mask('256'),F(37))]


def test_table(types, rows):
    masses=defaultdict(F)
    for support, weight in types:
        if weight:
            projected=sum(bool(support & (1 << r)) << j for j,r in enumerate(rows))
            masses[projected]+=weight
    if not set(masses) <= ALLOWED:
        return None
    d1=sum(masses[s] for s in D1)
    d2=sum(masses[s] for s in D2)
    if d1 > T or d2 > T:
        return {'legal':False,'d1':d1,'d2':d2}
    e9=min(masses[9],T-d1)
    e12=min(masses[12],T-d2)
    parts=[]
    for s,w in masses.items():
        if not w: continue
        code=int(s in D1)+2*int(s in D2)
        extra=e9 if s==9 else e12 if s==12 else F(0)
        if w>extra: parts.append((s,code,w-extra))
        if extra: parts.append((s,3,extra))
    endpoints={i for i,(s,q,w) in enumerate(parts)
               if any((s|t)==15 and (q&r)==0 for t,r,v in parts)}
    residual=sum(parts[i][2] for i in endpoints)
    return {'legal':True,'d1':d1,'d2':d2,'e9':e9,'e12':e12,
            'residual':residual,'covered':residual<P}


def main():
    rows_list=list(permutations(range(6),4))
    records=[]
    for a in range(5):
        for b in range(5-a):
            for c in range(5-a-b):
                ds=tuple(map(F,(a,b,c,4-a-b-c)))
                record={'deficits':[int(d)for d in ds]}
                for kind,builder in [('actual',actual_types),('containing',containing_types)]:
                    results=[];allowed=0;legal=0
                    for rows in rows_list:
                        res=test_table(builder(ds),rows)
                        if res is None:continue
                        allowed+=1
                        if not res['legal']:continue
                        legal+=1
                        results.append((res['residual'],rows,res))
                    record[kind]={'supported_orderings':allowed,'budget_legal_orderings':legal,
                                  'covered':any(r[0]<P for r in results)}
                    if results:
                        residual,rows,res=min(results,key=lambda t:(t[0],t[1]))
                        record[kind]['best']={'rows':[r+1 for r in rows],
                                             **{k:str(v)if isinstance(v,F)else v for k,v in res.items()}}
                record['covered']=record['actual']['covered']or record['containing']['covered']
                records.append(record)
    assert len(records)==35
    out={'status':'EXACT_FINITE_MENU_CHECK','scale':'b=1; deficits sum4',
         'budget':str(T),'strict_endpoint_target':str(P),
         'compositions_checked':35,'ordered_four_row_choices':len(rows_list),
         'covered_compositions':sum(r['covered']for r in records),
         'uncovered_deficits':[r['deficits']for r in records if not r['covered']],
         'records':records}
    target=Path(__file__).resolve().parent.parent/'outputs'/'agent_pivot_fixed_menu_results.json'
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items()if k!='records'},indent=2))


if __name__=='__main__':
    main()
