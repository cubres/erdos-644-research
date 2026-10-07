"""Add exactly witnessed templates at the uncovered 0.862 configurations."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import json,random
from p644_static_dual import facets
from p644_static_templates import minimal,solve,blocker


def run(source='logs/astra_static_template_facets.json',files=None,output='logs/astra_static_template_facets_v2.json'):
    data=json.loads(Path(source).read_text())
    seen={tuple(tuple(L) for L in row['triangle']) for row in data}
    for file in files or ['logs/astra_static_hole_probe.json','logs/astra_static_hole_probe2.json']:
        q=json.loads(Path(file).read_text());assert q['status']=='EXACT_WITNESS'
        t0=tuple(minimal(tuple(map(int,P))) for P in q['parts'][:3])
        for perm in permutations(range(3)):
            t=tuple(t0[j] for j in perm)
            if t in seen:continue
            seen.add(t);fs,vs=facets(t)
            assert sum(map(len,list(t)+[blocker(t[2]),blocker(t[1]),blocker(t[0])]))<=15
            rng=random.Random(644)
            for _ in range(4):
                p=[F(rng.randrange(21),50) for j in range(3)]
                v=max(f[0]+sum(a*b for a,b in zip(f[1:],p)) for f in fs)
                assert abs(float(v)-solve(t,p,exact=False))<1e-8
            data.append({'triangle':t,'forms':[list(map(str,f)) for f in fs],'vertices':[list(map(str,p)) for p in vs]})
    Path(output).write_text(json.dumps(data,separators=(',',':')))
    print('PASS',len(data),'templates',sum(len(r['forms']) for r in data),'forms',flush=True)

if __name__=='__main__':run()
