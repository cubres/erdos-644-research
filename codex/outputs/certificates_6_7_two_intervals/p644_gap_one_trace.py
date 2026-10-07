"""Partial-core lemma using a bound on just one new pair intersection."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget


def regions(beta,h,ell):
    beta,h,ell=map(F,(beta,h,ell))
    base=[(F(0),F(1),F(1),F(0)),
      (beta+1-h,F(-1),F(0),F(-1)),
      (1-h,F(0),F(1),F(0)),
      (ell,F(0),F(1),F(0)),
      (F(1),F(-1),F(-1),F(1)),
      ((1+ell)/2,F(0),F(0),F(1,2)),
      ((1+ell)/2,F(1,2),F(0),F(-1,2)),
      (F(1),F(0),F(-1),F(0)),
      ((3+ell)/4,F(1,2),F(-1,2),F(-1,4))]
    out=[]
    for perm in permutations(range(3)):
        fs=[]
        for f in base:
            row=[f[0],F(0),F(0),F(0)]
            for j,k in enumerate(perm):row[k+1]=f[j+1]
            fs.append(tuple(row))
        out.append(fs)
    return out


def script(branch):
    if branch:r,x,y,z,T,ell=1000,500,100,300,940,220
    else:r,x,y,z,T,ell=1000,380,220,380,860,224
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3);Q=contains(2,3,4)
    A=lambda E,L,P:contains(2,4)(E,L,P) and not contains(3)(E,L,P)
    B=lambda E,L,P:contains(3,4)(E,L,P) and not contains(2)(E,L,P)
    C=contains(1,4)
    S=lambda E,L,P:contains(1)(E,L,P) and not (contains(3)(E,L,P) or contains(4)(E,L,P))
    hs=[(mass(X),x,x,(1,2)),(mass(Y),y,y,(1,3)),(mass(Z),z,z,(2,3)),
        (mass(contains(1,2,3)),0,0,(1,2,3)),(mass(contains(2,4)),0,ell,(2,4))]
    if branch:
        hs.append((mass(B),T-x,r,(1,2,3,4)));cut=Aff(x-T)+mass(B)
    else:
        hs.append((mass(B),0,T-x,(1,2,3,4)));cut=0
    base=mass(Q)+y+mass(A)
    if branch:base+=cut
    steps={4:{'picks':[('Z0',Z,T-x-y)],'avoid':[X,Y,'Z0']},
      5:{'picks':[('B12',B,cut),('S1',S,Aff(T)-base)],'avoid':[Q,Y,A,'B12','S1']},
      6:{'avoid':[Z,C,'B12',both(S,notin('S1'))]},
      7:{'avoid':[X,both(B,notin('B12'))]}}
    return Script(7,r,T,steps,False,hs)


if __name__=='__main__':
    out=[]
    for branch in [0,1]:
        s=script(branch);q=solve(s,want=True);b=check_budget(s,want=True)
        print(branch,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        out.append({'branch':branch,'support':q,'budget':b})
    Path('logs/astra_gap_one_trace.json').write_text(json.dumps(out,indent=1))
