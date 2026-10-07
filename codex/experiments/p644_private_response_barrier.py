"""Exact affine-in-b certificate for a private-edge response barrier.

No optimizer or prior certificate is read. All assertions hold for every
integer b>=2. The infinitely many private edges are handled by the
monotonic graph statements proved in the accompanying report.
"""
from itertools import combinations
from fractions import Fraction as F
from pathlib import Path
import json


def add(p, q):
    return tuple(x+y for x, y in zip(p, q))


def mul(p, q):
    return (p[0]*q[0], p[0]*q[1]+p[1]*q[0], p[1]*q[1])


def at(p, b):
    return sum(x*b**(len(p)-1-i) for i, x in enumerate(p))


def nonnegative(p):
    # Coefficients after substituting b=u+1 must be nonnegative.
    if len(p)==2:
        return p[0]>=0 and sum(p)>=0
    a, b, c=p
    return a>=0 and 2*a+b>=0 and a+b+c>=0


def instance():
    lines=[frozenset(s) for s in combinations(range(7),3)
           if (s[0]+1)^(s[1]+1)^(s[2]+1)==0]
    cells=[]
    for line in lines:
        mask=sum(1<<i for i in range(7) if i not in line)
        cells.append({'mask':mask,'weight':(33,-1 if line==frozenset((0,1,2)) else 0)})
    for line in lines:
        for h in sorted(set(range(7))-line):
            cells.append({'mask':sum(1<<i for i in range(7) if i not in line|{h}),
                          'weight':(1,0)})
    cells.append({'mask':121,'weight':(0,1)})
    x=len(cells)-1
    retained=(2,4,5,6)
    available={1,3,4,5,10,12,14}
    for cell in cells:
        trace=sum(bool(cell['mask']&(1<<r))<<j for j,r in enumerate(retained))
        if trace in available:
            cell['mask']|=128
    # Padding makes G have size k=144b+1 and does not alter the fixed
    # four-old-row graph. These are fresh points, in G and no other row.
    cells.append({'mask':128,'weight':(30,1)})
    Z={i for i,c in enumerate(cells) if c['mask']&1 and i!=x}
    return cells,Z,x


def graph(cells, rows, restricted=None):
    full=sum(1<<r for r in rows)
    endpoint=set()
    pair=(F(0),F(0),F(0))
    for i,c in enumerate(cells):
        for j in range(i,len(cells)):
            d=cells[j]
            if restricted is not None and i not in restricted and j not in restricted:
                continue
            if (c['mask']|d['mask'])&full!=full:
                continue
            if i==j:
                # Only the repair point has fixed cardinality one.
                if c['weight']==(0,1):
                    continue
                a,b=c['weight']
                q=(F(a*a,2),F(a*(2*b-1),2),F(b*(b-1),2))
            else:
                q=mul(c['weight'],d['weight'])
            assert nonnegative(q) and at(q,2)>0
            endpoint.update((i,j))
            pair=add(pair,q)
    mass=(0,0)
    for i in endpoint:
        mass=add(mass,cells[i]['weight'])
    return endpoint,mass,pair


def main():
    cells,Z,x=instance()
    old=range(8)
    P,p,Q=graph(cells,range(1,7))
    assert p==(111,0) and Q==(3669,0,0)
    assert not(P&Z)
    zmass=(0,0)
    for i in Z: zmass=add(zmass,cells[i]['weight'])
    assert zmass==(144,0)
    assert any(cells[i]['mask']&128 for i in Z)
    for row in old:
        mass=(0,0)
        for c in cells:
            if c['mask']&(1<<row):mass=add(mass,c['weight'])
        assert mass==((144,1) if row in (0,7) else (144,0))

    result={'status':'EXACT_PASS','valid_for':'every integer b>=2',
            'rank':'144b+1','endpoint_minimum':'111b','pair_minimum':'3669b^2',
            'tau_of_private_extension':3,'tables':{}}
    for count,restricted,name in ((6,None,'old_six'),(7,None,'old_seven'),
                                  (5,Z,'five_old_pairs_meeting_Z'),
                                  (4,Z,'four_old_pairs_meeting_Z')):
        table=[]
        for rows in combinations(old,count):
            ep,mass,pair=graph(cells,rows,restricted)
            assert at(pair,1)>0
            if count in (6,5):
                diff=(mass[0]-111,mass[1])
                assert nonnegative(diff)
                if diff==(0,0):
                    assert nonnegative((pair[0]-3669,pair[1],pair[2]))
            if count==4:
                assert nonnegative((mass[0]-184,mass[1]))
            if count==6 and not(ep&Z):
                # Every private edge Z+{z}, z in P, still meets this
                # actual endpoint set, proving the seven-row condition.
                assert P<=ep
            table.append({'rows':list(rows),'endpoint_affine':list(mass),
                          'pair_quadratic':[str(v) for v in pair]})
        result['tables'][name]=table
    path=Path(__file__).resolve().parents[1]/'outputs/agent_private_response_barrier.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='tables'},indent=2))


if __name__=='__main__':main()
