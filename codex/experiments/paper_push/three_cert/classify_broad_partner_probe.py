"""Reproduce and exactly classify the first1,200 logged broad-probe states.
The original deterministic generator is reused verbatim; no terminal oracle
is rerun. Exact integer Fano/V4/pair checks separate known contradictions.
"""
from pathlib import Path
s=Path(__file__).with_name('probe_fano_v4_partners.py').read_text().split('    r=analyse(x,T)')[0]
s=s.replace('while time.process_time()-start<limit:', 'while count<1200:')
s+='''\n    count+=1\n    bad=known_bad(x,T)\n    records.append({'index':count,'capacities':list(map(str,x)),'types':[list(map(str,t)) for t in T],'existing_bad_tuple':bad})\n'''
from known_anchor_bad import known_bad
scope={'known_bad':known_bad,'__file__':str(Path(__file__).with_name('probe_fano_v4_partners.py'))}
exec(compile(s,'deterministic_broad_regeneration','exec'),scope)
import json,time
records=scope['records'];known=sum(q['existing_bad_tuple'] is not None for q in records)
out={'status':'EXACT_CLASSIFICATION_OF_LOGGED_FIRST_1200','states':len(records),'already_bad':known,'genuine_terminal_cases':len(records)-known,'cpu_seconds':round(time.process_time()-scope['start'],3),'records':records,'source_terminal_evidence':'fano_v4_partner_probe.log records all1,200 exact terminal costs<=677/1000; interrupted afterthis checkpoint to focus remainingbudget. Worstexactrequest storedseparately.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='records'}))
