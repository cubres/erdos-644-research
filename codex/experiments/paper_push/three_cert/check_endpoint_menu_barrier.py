"""Standalone exact replay of the endpoint obstruction to the current menu.

The original three types have P7 by the common-part >4/7 lemma. The candidate
bad seven-tuples may use one additional TYPE any number of times. All Fano,
V4,42two-type, and learned mixed1321 assignments are included. A separate
brute-force enumeration of corner cut levels checks the request-cost optimum.
This is a restricted-menu obstruction, not a counterexample to Th(3).
"""
import json,itertools
from pathlib import Path
from fractions import Fraction as F
from repeated_response_oracle import analyse
x=tuple(F(v,100000) for v in (76000,75000,75000))
T=[tuple(F(v,100000) for v in row) for row in ((50849,0,49151),(0,50099,49901),(0,49951,50049))]
assert sum(x[i]-T[i][i] for i in range(3))==F(75003,100000)
assert all(T[i][i]>2*x[i]/3 for i in range(3))
assert min(t[2] for t in T)>4*x[2]/7
r=analyse(x,T,all_known=True);corners=r['escape_corners']
levels=[sorted({x[i]}|{cc[i][0] for cc in corners}) for i in range(3)]
best=sum(x)-1;bestu=None;checked=0
for u in itertools.product(*levels):
 checked+=1
 if not all(any(v<low or (v==low and (strict or low>0)) for v,(low,strict) in zip(u,c)) for c in corners):continue
 cost=sum(x)-sum(u)
 if cost<best:best=cost;bestu=u
assert best==r['request_cost']==F(8321,10000)
assert best>F(3,4)
out={'status':'PASS_EXACT_RESTRICTED_MENU_OBSTRUCTION','capacities':x,'types':T,
     'own_slack_sum':F(75003,100000),'common_part_P7_margin':min(t[2] for t in T)-4*x[2]/7,
     'best_request_cost':best,'retained_box':bestu,'boxes':len(r['boxes']),
     'escape_orthants':len(corners),'brute_cut_triples_checked':checked,
     'scope':'One new type may repeat in every Fano,V4,42pair,or mixed1321 template. Requests chosen by arbitrary per-part deletion cannot force this menu belowthe displayed cost. Further queries, extremal selection, or other supports are not excluded.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,default=str,indent=2));print(json.dumps(out,default=str))
