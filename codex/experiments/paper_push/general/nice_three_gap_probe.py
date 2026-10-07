"""Three rational gap extensions; discovery only, replay separately."""
import json
from itertools import permutations,product
from pathlib import Path
from compress_phases_probe import F,beta,base,remaining,certify_box
planes=[(-beta,F(1),F(1),F(1))]
planes += [(F(-4,7),)+p for p in set(permutations((F(1),F(1),F(-1))))]
planes += [(F(-11,7),)+p for p in set(permutations((F(2),F(1),F(1))))]
a,b,u,v=F(3,7),F(10,21),F(5,14),F(5,14)
boxes=[]
for yi,zi in product(remaining(u,[]),remaining(v,[])):
 proof=certify_box(base,beta,(a,yi[0],zi[0]),(b,yi[1],zi[1]),limit=40000,depth_limit=90,split_planes=planes)
 if proof['status']!='COVERED':
  print(proof);raise SystemExit(1)
 boxes.append({'y':list(map(str,yi)),'z':list(map(str,zi)),'proof':proof})
step={'interval':list(map(str,(a,b))),'u':str(u),'v_at_left':str(v),'boxes':boxes,'prior_gaps':[],'two_triples':True}
Path(__file__).with_name('nice_upper_seed.json').write_text(json.dumps(step,separators=(',',':')))
print('COVERED',sum(len(q['proof']['nodes']) for q in boxes),'nodes')
