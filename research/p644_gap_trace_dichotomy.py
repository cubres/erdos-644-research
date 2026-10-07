"""Single-trace partial core, splitting on a second trace across r/2."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin,inpick
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget


def regions(beta,h,ell,m):
    beta,h,ell,m=map(F,(beta,h,ell,m))
    base=[(F(0),F(1),F(1),F(0)),(beta+1-h,F(-1),F(0),F(-1)),
      (1-h,F(0),F(1),F(0)),(ell,F(0),F(1),F(0)),(m,F(0),F(0),F(1)),
      ((1+ell)/2,F(0),F(0),F(1,2)),((1+ell)/2,F(1,2),F(0),F(-1,2)),
      ((1+m)/2,F(1,2),F(-1,2),F(0)),((3+ell)/4,F(1,2),F(-1,2),F(-1,4)),
      (m,F(1),F(0),F(0)),(ell,F(0),F(1),F(1)),
      ((1+ell)/2,F(-1,2),F(0),F(1)),(F(1,2),F(0),F(0),F(2,3))]
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
    r,x,y,z,T,ell,m=1000,382,110,381,858,143,383
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3);Q=contains(2,3,4)
    A=lambda E,L,P:contains(2,4)(E,L,P) and not contains(3)(E,L,P)
    B=lambda E,L,P:contains(3,4)(E,L,P) and not contains(2)(E,L,P)
    C=contains(1,4);GH=contains(3,4)
    hs=[(mass(X),x,x,(1,2)),(mass(Y),y,y,(1,3)),(mass(Z),z,z,(2,3)),
      (mass(contains(1,2,3)),0,0,(1,2,3)),(mass(contains(2,4)),0,ell,(2,4))]
    steps={4:{'picks':[('Z0',Z,T-x-y)],'avoid':[X,Y,'Z0']}}
    if branch<2:
        hs.append((mass(C),0,m,(1,4)))
        if branch:hs.append((mass(B),T-x,r,(1,2,3,4)));cut=Aff(x-T)+mass(B)
        else:hs.append((mass(B),0,T-x,(1,2,3,4)));cut=0
        S=lambda E,L,P:contains(1)(E,L,P) and not(contains(3)(E,L,P) or contains(4)(E,L,P))
        base=mass(Q)+y+mass(A)+cut
        steps.update({5:{'picks':[('B12',B,cut),('S1',S,Aff(T)-base)],'avoid':[Q,Y,A,'B12','S1']},
          6:{'avoid':[Z,C,'B12',both(S,notin('S1'))]},7:{'avoid':[X,both(B,notin('B12'))]}})
    else:
        hs.extend([(mass(C),501,r,(1,4)),(mass(GH),0,m,(3,4))])
        D=cellin((1,2,3,4),1)
        steps.update({5:{'picks':[('D1',D,Aff(T-x)-mass(GH))],'avoid':[X,GH,'D1']},
          6:{'picks':[('C2',C,Aff(T-y-z)-mass(A)),('D2',both(D,notin('D1')),Aff(T-y-z)-mass(A)-mass(inpick('C2')))],'avoid':[Y,Z,A,'C2','D2']},
          7:{'avoid':[Z,both(C,notin('C2')),both(both(D,notin('D1')),notin('D2'))]}})
    return Script(7,r,T,steps,False,hs)


if __name__=='__main__':
    out=[]
    for branch in range(3):
        s=script(branch);q=solve(s,want=True);b=check_budget(s,want=True)
        print(branch,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        out.append({'branch':branch,'support':q,'budget':b})
    Path('logs/astra_gap_trace_dichotomy.json').write_text(json.dumps(out,indent=1))
