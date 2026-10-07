"""Gap lemma retaining two triple cells after the fourth response."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget


def regions(beta,h,ell):
    beta,h,ell=map(F,(beta,h,ell))
    base=[(beta+1-h,F(-1),F(-1),F(0)),
      (beta+1-h,F(0),F(-1),F(-1)),
      (2-2*h,F(0),F(-1),F(0)),
      (ell,F(1),F(0),F(0)),(ell,F(0),F(0),F(1)),
      (F(1,2),F(0),F(1),F(0)),(F(3,4),F(0),F(0),F(0)),
      (F(3,5),F(1,5),F(1,5),F(1,5))]
    out=[]
    for perm in permutations(range(3)):
        fs=[]
        for f in base:
            row=[f[0],F(0),F(0),F(0)]
            for j,k in enumerate(perm):row[k+1]=f[j+1]
            fs.append(tuple(row))
        out.append(fs)
    return out


def script(full_core=False):
    if full_core:r,x,y,z,T,h0,ell=1000,350,250,250,880,500,400
    else:r,x,y,z,T,h0,ell=56000,23016,13489,22512,47040,26656,24024
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3)
    g=max(0,r-y-h0);S=x+y+z
    rest=lambda E,L,P:(X(E,L,P) or Z(E,L,P)) and not('X0' in L or 'Z0' in L)
    U=lambda E,L,P:E & frozenset([1,2,3,4]) in [frozenset([1]),frozenset([3])]
    EH=contains(1,4);FH=contains(2,4);GH=contains(3,4)
    hs=[(mass(X),x,x,(1,2)),(mass(Y),y,y,(1,3)),(mass(Z),z,z,(2,3)),
        (mass(contains(1,2,3)),0,0,(1,2,3)),(mass(EH),0,ell,(1,4)),(mass(GH),0,ell,(3,4))]
    steps={4:{'picks':[('X0',X,g),('Z0',Z,g),('R',rest,T-y-2*g),('F0',cellin((1,2,3),2),max(0,T-S))],
              'avoid':[Y,'X0','Z0','R','F0']},
       5:{'picks':[('U1',U,Aff(T-x)-mass(GH))],'avoid':[X,GH,'U1']},
       6:{'picks':[('U2',both(U,notin('U1')),Aff(T-z)-mass(EH))],'avoid':[Z,EH,'U2']},
       7:{'avoid':[Y,FH,both(both(U,notin('U1')),notin('U2'))]}}
    return Script(7,r,T,steps,False,hs)


if __name__=='__main__':
    out=[]
    for full_core in [False,True]:
        s=script(full_core);q=solve(s,want=True);b=check_budget(s,want=True)
        print(full_core,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        out.append({'full_core':full_core,'support':q,'budget':b})
    Path('logs/astra_gap_two_triples.json').write_text(json.dumps(out,indent=1))
