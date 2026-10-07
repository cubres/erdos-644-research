"""Exact integer checks of the three-request packing in the 11/13 gap theorem."""
from itertools import combinations
from pathlib import Path
import json
from p644_strategy import Script,mass,contains,both,notin
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget


def script(m,kind):
    r,T=3900,3300;x=(2*r-T-m)//2;b=r-T+x
    X=contains(1,2);B=contains(3,4)
    pairs=[(1,3),(2,4),(2,3),(1,4)]
    U=lambda E,L,placed:any(set(p)<=E for p in pairs)
    hs=[(mass(X),x,x,(1,2)),(mass(B),b,b,(3,4))]
    hs.extend((mass(contains(*p)),m,m,p) for p in pairs)
    hs.extend((mass(contains(*p)),0,0,p) for p in combinations(range(1,5),3))
    if kind=='split':
        steps={5:{'picks':[('B1',B,b//2)],'avoid':[X,'B1']},6:{'avoid':[X,both(B,notin('B1'))]},7:{'avoid':[U]}}
    else:
        u=4*m;x2=max(0,(x-u)//2);d=max(u+x2,x-x2);b2=max(0,min(b,(x+b-d)//2))
        steps={5:{'picks':[('X2',X,x2),('B2',B,b2)],'avoid':[X,both(B,notin('B2'))]},
          6:{'avoid':['X2','B2',U]},7:{'avoid':[both(X,notin('X2')),'B2']}}
    return Script(7,r,T,steps,False,hs)


if __name__=='__main__':
    rows=[]
    for m,kind in [(400,'cross'),(500,'cross'),(550,'split')]:
        s=script(m,kind);q=solve(s,want=True);b=check_budget(s,want=True)
        print(m,kind,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        rows.append({'m':m,'kind':kind,'support':q,'budget':b})
    Path('logs/astra_gap_matching.json').write_text(json.dumps(rows,indent=1))
