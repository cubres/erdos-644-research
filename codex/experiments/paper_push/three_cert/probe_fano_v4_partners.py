"""Bounded deterministic rational probe; all accepted terminal rules are exact.
A surviving state disproves only this particular three-minimum one-response menu.
"""
import time,random,json,sys
from pathlib import Path
from fractions import Fraction as F
from fano_v4_partner_oracle import analyse,encoded
rng=random.Random(6440926);start=time.process_time();limit=float(sys.argv[1]) if len(sys.argv)>1 else 180
prefix=Path(__file__).with_name('fano_v4_partner_probe');count=0;attempts=0;worst=None;records=[]
while time.process_time()-start<limit:
    attempts+=1
    if attempts%3==0:xs=[rng.randint(750,1100) for _ in range(3)]
    elif attempts%3==1:xs=[rng.randint(750,825) for _ in range(3)]
    else:xs=[rng.randint(750,925) for _ in range(3)]
    if min(xs)>=857:continue
    lower=[2*v//3+1 for v in xs];room=sum(xs)-751-sum(lower)
    if room<0:continue
    # Vary total own slack, with repeated pressure near the target boundary.
    budget=room if attempts%4==0 else rng.randint(0,room)
    inc=[0,0,0]
    for _ in range(budget):inc[rng.randrange(3)]+=1
    gs=[lower[i]+inc[i] for i in range(3)]
    if any(gs[i]>min(xs[i],1000) for i in range(3)):continue
    if any(xs[i]-gs[i]+xs[j]-gs[j]>750 for i in range(3) for j in range(i)):continue
    rows=[]
    for i in range(3):
        rem=1000-gs[i]
        # A mixture of simplex-edge, near-edge, and generic off-traces.
        mode=rng.randrange(5)
        q=0 if mode==0 else rem if mode==1 else rng.randint(0,min(15,rem)) if mode==2 else rem-rng.randint(0,min(15,rem)) if mode==3 else rng.randint(0,rem)
        off=[j for j in range(3) if j!=i];row=[0,0,0];row[i]=gs[i];row[off[0]]=q;row[off[1]]=rem-q;rows.append(row)
    x=tuple(F(v,1000) for v in xs);T=[tuple(F(v,1000) for v in row) for row in rows]
    r=analyse(x,T);count+=1
    rec={'index':count,'capacities':list(map(str,x)),'types':[list(map(str,t)) for t in T],
         'request_cost':str(r['request_cost']),'closed_box_free':r['closed_box_free'],
         'boxes':len(r['boxes']),'escape_orthants':len(r['escape_corners'])}
    records.append(rec)
    if worst is None or r['request_cost']>worst['request_cost']:
        worst=r;prefix.with_suffix('.worst.json').write_text(encoded(r)+'\n')
    if not r['closes_at_three_quarters']:
        prefix.with_suffix('.counterstate.json').write_text(encoded(r)+'\n')
        print('EXACT_MENU_COUNTERSTATE',count,'cost',r['request_cost'],'capacities',x,'types',T,flush=True)
        break
    if count%100==0:print('PROGRESS',count,'CPU',round(time.process_time()-start,2),'worst',worst['request_cost'],flush=True)
summary={'status':'COUNTERSTATE' if records and F(records[-1]['request_cost'])>F(3,4) else 'BOUNDED_NO_COUNTERSTATE',
         'points_checked':count,'attempts':attempts,'cpu_seconds':round(time.process_time()-start,3),
         'seed':6440926,'worst_cost':str(worst['request_cost']) if worst else None,
         'scope':'Finite rational probe only; no uniform theorem follows. Capacities>=3/4, eachownminimum strictlyheavy, allpairslacks<=3/4, totalslack>3/4.',
         'records':records}
prefix.with_suffix('.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='records'}),flush=True)
