"""Independent strategy encoding of the small-triple-cell case, Lemma 7.27."""
from p644_strategy import Script,Aff,mass,contains,cellin,both,notin,inpick
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget
from pathlib import Path
import json


def script():
    r,x,y,z,T=1000,500,200,180,869
    X=contains(1,2);Y=contains(1,3);Z=contains(2,3);four=(1,2,3,4)
    Q=cellin(four,2,3,4);A=cellin(four,2,4);B=cellin(four,3,4);C=cellin(four,1,4);D=cellin(four,1)
    B2=both(B,notin('B1'));D2host=both(D,notin('D1'))
    steps={
     4:{'picks':[('Z0',Z,T-x-y)],'avoid':[X,Y,'Z0']},
     5:{'picks':[('B1',B,Aff(T-x)-mass(Q)),
                 ('D1',D,Aff(T-x)-mass(Q)-mass(inpick('B1')))],'avoid':[X,Q,'B1','D1']},
     6:{'picks':[('D2',D2host,Aff(T-x)-mass(Q)-mass(B2))],'avoid':[X,Q,B2,'D2']},
     7:{'avoid':[Y,Z,A,C,both(D2host,notin('D2'))]}}
    hs=[(mass(X),x,x,(1,2)),(mass(Y),y,y,(1,3)),(mass(Z),z,z,(2,3)),
        (mass(contains(1,2,3)),0,0,(1,2,3)),
        (mass(contains(1,4)),0,215,four),(mass(contains(2,4)),0,215,four)]
    return Script(7,r,T,steps,False,hs)

if __name__=='__main__':
    s=script();q=solve(s,want=True);print('SUPPORT',q['status'],flush=True)
    b=check_budget(s,want=True);print('BUDGET',b['status'],flush=True)
    assert q['status']=='PROVER WINS' and b['status']=='LEGAL'
    Path('logs/astra_triple_cell_script.json').write_text(json.dumps({'support':q,'budget':b},indent=1))
