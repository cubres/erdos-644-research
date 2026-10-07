"""Independent standard-library audit of every two-type capacity function.

Checks primal/dual witnesses and every upper polygon facet; independently
reconstructs support-colour coverage. Optional multiprocessing changes speed
only, not the exact checks.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import multiprocessing
import time
import zipfile
from p644_support_lp_check import permutation_maps,colour_representatives


def check_record(record,parents):
    colour=record['colour'];certs={};valid={(F(0),F(0))}
    for certificate in record['lp_certificates']:
        direction=tuple(map(F,certificate['direction']));assert sum(direction)==1 and min(direction)>=0
        y=list(map(F,certificate['primal']));w=list(map(F,certificate['dual']))
        assert len(y)==len(parents) and len(w)==7 and min(y+w)>=0
        demand=[direction[colour>>j&1] for j in range(7)]
        assert all(sum(y[t] for t,m in enumerate(parents) if m>>j&1)>=demand[j] for j in range(7))
        assert all(sum(w[j] for j in range(7) if m>>j&1)<=1 for m in parents)
        value=sum(y);assert value==sum(a*b for a,b in zip(w,demand))==F(certificate['value'])
        point=(sum(w[j] for j in range(7) if not colour>>j&1),sum(w[j] for j in range(7) if colour>>j&1))
        assert point==tuple(map(F,certificate['point']));valid.add(point)
        valid.add((point[0],F(0)));valid.add((F(0),point[1]))
        assert direction not in certs;certs[direction]=value
    points=[tuple(map(F,p)) for p in record['all_vertices']]
    assert len(points)==len(set(points)) and all(p in valid for p in points)
    efficient=sorted(v for v in points if not any(v!=w and v[0]<=w[0] and v[1]<=w[1] for w in points))
    assert efficient==[tuple(map(F,p)) for p in record['vertices']]
    assert certs[(F(1),F(0))]==efficient[-1][0]
    assert certs[(F(0),F(1))]==efficient[0][1]
    for left,right in zip(efficient,efficient[1:]):
        a=left[1]-right[1];b=right[0]-left[0];assert a>0 and b>0
        direction=(a/(a+b),b/(a+b));assert direction in certs
        assert certs[direction]==(a*left[0]+b*left[1])/(a+b)
    return tuple(efficient),len(certs)


def worker(task):
    item,path,archive=task
    if archive:
        with zipfile.ZipFile(archive) as store:rows=json.loads(store.read(path))
    else:rows=json.loads(Path(path).read_text())
    found=set();functions=set();certificates=0
    for row in rows:
        assert row['truth_table']==item['truth_table'] and row['colour'] not in found
        found.add(row['colour']);function,n=check_record(row,item['maximal_cells']);functions.add(function);certificates+=n
    return item['truth_table'],found,functions,certificates


def run(root,workers=1,archive=None):
    root=Path(root);base=Path(__file__).parent
    catalogue=json.loads((base/'logs/astra_full_support_catalog.json').read_text())['orbits']
    maps=permutation_maps();expected={q['truth_table']:set(colour_representatives(q['maximal_cells'],maps)) for q in catalogue}
    assert sum(map(len,expected.values()))==54214
    tasks=[(q,q['truth_table']+'.json' if archive else str(root/(q['truth_table']+'.json')),archive) for q in catalogue]
    total=0;certificates=0;functions=set();started=time.time()
    with multiprocessing.get_context('spawn').Pool(workers) as pool:
        for stem,colours,new,count in pool.imap_unordered(worker,tasks):
            assert colours==expected[stem];total+=len(colours);certificates+=count;functions.update(new)
    assert total==54214
    reduction=base/'logs/astra_support_capacity_minimal.json'
    if reduction.exists():
        reduced=json.loads(reduction.read_text())
        keys={';'.join(','.join(map(str,p)) for p in f) for f in functions}
        assert keys==set(reduced['dominators'])
        records={}
        for row in reduced['minimal_functions']:
            shape=tuple(tuple(map(F,p)) for p in row['vertices']);assert shape in functions
            stem,colour=row['witness']
            if stem not in records:
                if archive:
                    with zipfile.ZipFile(archive) as store:records[stem]=json.loads(store.read(stem+'.json'))
                else:records[stem]=json.loads((root/(stem+'.json')).read_text())
            witness=next(q for q in records[stem] if q['colour']==colour)
            assert witness['vertices']==row['vertices']
    print('PASS:',total,'capacity functions;',certificates,'exact LP certificates;',len(functions),'distinct functions; seconds',round(time.time()-started,2),flush=True)
    return functions


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',default='logs/astra_support_capacity');parser.add_argument('--workers',type=int,default=1)
    parser.add_argument('--archive')
    args=parser.parse_args();run(args.root,args.workers,args.archive)
