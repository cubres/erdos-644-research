"""Exact integer checks of all four response cases in Lemma 7.31."""
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin,inpick
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget
from pathlib import Path
import json


def script(branch):
    r,x,y,z,T=2000,500,500,900,1675
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3);four=(1,2,3,4)
    Q=cellin(four,2,3,4);A=cellin(four,2,4);B=cellin(four,3,4);C=cellin(four,1,4);D=cellin(four,1);V=cellin(four,2,3)
    hs=[(mass(X),x,x,(1,2)),(mass(Y),y,y,(1,3)),(mass(Z),z,z,(2,3)),(mass(contains(1,2,3)),0,0,(1,2,3))]
    steps={4:{'picks':[('Z0',Z,T-x-y)],'avoid':[X,Y,'Z0']}}
    Dr=both(D,notin('D1'));Dlast=both(Dr,notin('D2'))
    if branch==0:
        hs.append((mass(C),0,T-z,four))
        steps.update({5:{'picks':[('D1',D,Aff(T-x)-mass(Q)-mass(B))],'avoid':[X,Q,B,'D1']},
          6:{'picks':[('D2',Dr,Aff(T-y)-mass(Q)-mass(A))],'avoid':[Y,Q,A,'D2']},
          7:{'avoid':[Z,C,Dlast]}})
    elif branch in [1,2]:
        hs.append((mass(C),T-z+1,r,four))
        if branch==1:
            P,R,s,t,small,big=A,B,x,y,A,B;J,K=X,Y
        else:
            P,R,s,t,small,big=B,A,y,x,B,A;J,K=Y,X
        hs.append((mass(small),0,r+s+z-2*T-1,four))
        steps.update({5:{'picks':[('D1',D,Aff(T-s)-mass(Q)-mass(big))],'avoid':[J,Q,big,'D1']},
          6:{'picks':[('C2',C,Aff(T-t-z)-mass(small)),('D2',Dr,Aff(T-t-z)-mass(small)-mass(inpick('C2')))],
             'avoid':[K,Z,small,'C2','D2']},
          7:{'avoid':[Z,both(C,notin('C2')),Dlast]}})
    else:
        hs.extend([(mass(C),T-z+1,r,four),(mass(A),r+x+z-2*T,r,four),(mass(B),r+y+z-2*T,r,four)])
        V23=both(V,notin('V13'))
        steps.update({5:{'picks':[('C12',C,mass(C)+(z-T)),
              ('V13',V,Aff(T-x)-mass(Q)-mass(B)-mass(inpick('C12'))),
              ('D1',D,Aff(T-x)-mass(Q)-mass(B)-mass(inpick('C12'))-mass(inpick('V13')))],
             'avoid':[Q,X,B,'C12','V13','D1']},
          6:{'picks':[('D2',Dr,Aff(T-y)-mass(Q)-mass(A)-mass(inpick('C12'))-mass(V23))],
             'avoid':[Q,Y,A,'C12',V23,'D2']},
          7:{'avoid':[Z,both(C,notin('C12')),Dlast]}})
    return Script(7,r,T,steps,False,hs)

if __name__=='__main__':
    rows=[]
    for branch in range(4):
        s=script(branch);q=solve(s,want=True);b=check_budget(s,want=True)
        print('branch',branch,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        rows.append({'branch':branch,'support':q,'budget':b})
        Path('logs/astra_partial_core_cases.json').write_text(json.dumps(rows,indent=1))
