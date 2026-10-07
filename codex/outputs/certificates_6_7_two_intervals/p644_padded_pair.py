"""Representative integral support and budget check of Lemma 7.32."""
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin,inpick
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget
from pathlib import Path
import json


def script(branch):
    r,x,y,z,T=1000,445,343,37,850
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3)
    Fprivate=cellin((1,2,3),2)
    A=contains(2,4);B=contains(3,4);C=contains(1,4)
    hs=[(mass(X),x,x,(1,2)),(mass(Y),y,y,(1,3)),(mass(Z),z,z,(2,3)),(mass(contains(1,2,3)),0,0,(1,2,3))]
    B2=both(B,notin('B1'));Crem=both(C,notin('C1'));C3=both(Crem,notin('C2'))
    steps={4:{'picks':[('P',Fprivate,T-x-y-z)],'avoid':[X,Y,Z,'P']},
      5:{'picks':[('B1',B,T-x-z),('C1',C,Aff(T-x-z)-mass(inpick('B1')))],'avoid':[X,Z,'B1','C1']},
      6:{'picks':[('C2',Crem,Aff(T-x-z)-mass(B2))],'avoid':[X,Z,B2,'C2']},
      7:{'avoid':[Y,Z,A,C3]}}
    if branch==0:
        hs.append((mass(A),0,T-y-z,(1,2,3,4)))
    else:
        hs.append((mass(A),T-y-z+1,r,(1,2,3,4)))
        BC=lambda E,L,placed:B(E,L,placed) or C(E,L,placed)
        steps.update({5:{'picks':[('U1',BC,T-x-z)],'avoid':[X,Z,'U1']},
          6:{'avoid':[X,Z,both(BC,notin('U1'))]},7:{'avoid':[Y,A]}})
    return Script(7,r,T,steps,False,hs)


if __name__=='__main__':
    rows=[]
    for branch in range(2):
        s=script(branch);q=solve(s,want=True);b=check_budget(s,want=True)
        print(branch,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        rows.append({'branch':branch,'support':q,'budget':b})
    Path('logs/astra_padded_pair.json').write_text(json.dumps(rows,indent=1))
