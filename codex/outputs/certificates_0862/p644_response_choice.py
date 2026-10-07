"""Exact strict-support and budget checks for the three branches of Lemma 7.26."""
from p644_strategy import Script,Aff,mass,contains,both,notin,inpick
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget
from pathlib import Path
import json


def script(branch):
    r,x,y,z,T=800,308,308,43,692
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3)
    A=contains(2,4);B=contains(3,4);C=contains(1,4)
    hs=[(mass(X),x,x,(1,2)),(mass(Y),y,y,(1,3)),(mass(Z),z,z,(2,3)),
        (mass(contains(1,2,3)),0,0,(1,2,3))]
    steps={4:{'avoid':[X,Y,Z]}}
    if branch==1:
        hs.append((mass(B),0,T-x,(1,2,3,4)))
        steps.update({5:{'avoid':[X,B]},
          6:{'picks':[('A2',A,Aff(T-y-z)-mass(C))],'avoid':[Y,Z,C,'A2']},
          7:{'avoid':[Y,both(A,notin('A2'))]}})
    elif branch==2:
        hs.append((mass(A),0,T-y,(1,2,3,4)))
        steps.update({5:{'avoid':[Y,A]},
          6:{'picks':[('B2',B,Aff(T-x-z)-mass(C))],'avoid':[X,Z,C,'B2']},
          7:{'avoid':[X,both(B,notin('B2'))]}})
    else:
        hs.extend([(mass(A),T-y+1,r,(1,2,3,4)),(mass(B),T-x+1,r,(1,2,3,4))])
        steps.update({5:{'picks':[('B2',B,T-x)],'avoid':[X,'B2']},
          6:{'picks':[('A3',A,T-y)],'avoid':[Y,'A3']},
          7:{'avoid':[X,Y,Z,C,both(A,notin('A3')),both(B,notin('B2'))]}})
    return Script(7,r,T,steps,False,hs)

if __name__=='__main__':
    rows=[]
    for i in [1,2,3]:
        s=script(i);q=solve(s,want=True);b=check_budget(s,want=True)
        print('branch',i,q['status'],b['status'],flush=True)
        assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
        rows.append({'branch':i,'support':q,'budget':b})
    Path('logs/astra_response_choice.json').write_text(json.dumps(rows,indent=1))
