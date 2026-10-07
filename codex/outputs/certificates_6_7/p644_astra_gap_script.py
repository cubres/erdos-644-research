"""A seven-edge adaptive example using a gap in pair intersections.

r=100, T=85, good-triple pair sizes 50,10,10. If every pair of
family edges has intersection <=10 or >=50, the fourth edge,
which avoids all three pair cells, has intersection <=10 with
each large-overlap anchor (each available private part has size40).
Those two derived inequalities are supplied explicitly to the verifier.
The hand lemma in note_644.md supplies their global justification.
"""
from p644_strategy import Script,mass,contains,cellin,both,notin
from p644_strategy_lp import solve
from p644_strategy_budget import check_budget
from pathlib import Path
import json


def script():
    triple=(1,2,3);X=contains(1,3);Y=contains(1,2);Z=contains(2,3)
    W=cellin(triple,2)
    rest1=both(W,notin('W1'));rest2=both(rest1,notin('W2'));rest3=both(rest2,notin('W3'))
    steps={
        4:{'picks':[('W1',W,15)],'avoid':[X,Y,Z,'W1']},
        5:{'picks':[('W2',rest1,35)],'avoid':[X,'W2']},
        6:{'picks':[('W3',rest2,15)],'avoid':[X,'W3',Y,contains(3,4)]},
        7:{'avoid':[X,rest3,Z,contains(1,4)]}}
    hs=[(mass(X),50,50,(1,3)),(mass(Y),10,10,(1,2)),(mass(Z),10,10,(2,3)),
        (mass(contains(1,2,3)),0,0,(1,2,3)),
        (mass(contains(1,4)),0,10,(1,4)),(mass(contains(3,4)),0,10,(3,4))]
    return Script(7,100,85,steps,False,hs)


if __name__=='__main__':
    s=script();out={'solve':solve(s,want=True),'budget':check_budget(s,want=True)}
    print(out['solve']['status'],out['budget']['status'])
    assert out['solve']['status']=='PROVER WINS' and out['budget']['status']=='LEGAL'
    Path('logs/astra_gap_script.json').write_text(json.dumps(out,indent=1))
