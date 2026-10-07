"""Portable replay of the general three-part two-box theorem.

The earlier intersecting certificate is replayed first. The mixed-disjoint
branch has independently reconstructed inputs and externally checked CPC
proofs. This script requires only Python's standard library and Ethos.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import time
from p644_box_certificate_check import replay as replay_intersecting
from p644_two_box_general_audit import audit
from p644_support_capacity_check import check_record


def replay(base,ethos=None):
    base=Path(base).resolve();manifest=json.loads((base/'MANIFEST.json').read_text())
    for name,digest in manifest.items():assert hashlib.sha256((base/name).read_bytes()).hexdigest()==digest,('hash mismatch',name)
    print('PASS',len(manifest),'general-bundle manifest hashes',flush=True)
    replay_intersecting(base/'intersecting',ethos)
    templates=json.loads((base/'logs/astra_two_type_recursive/templates.json').read_text());shapes=set()
    for item in templates.values():
        parents=item['parents'];assert all(0<m<127 for m in parents) and all(a|b!=127 for a in parents for b in parents)
        shape,_=check_record(item['record'],parents);shapes.add(shape)
    assert tuple([(F(5,6),F(1)),(F(1),F(3,4)),(F(4,3),F(0))]) in shapes
    assert tuple([(F(1,2),F(5,4)),(F(1),F(1))]) in shapes
    sig=base/'intersecting/proof_checkers/cvc5-1.4.0-signatures/cpc'
    checker=Path(ethos).resolve() if ethos else base/'intersecting/proof_checkers/ethos-0.2.4/ethos'
    root=base/'logs/astra_two_box_general_3_mixed';rows=[]
    for key in ['000','001','003','011','012','013','033','111','112','113','123','133','333']:
        start=time.time();info=audit(key,root,mixed=True);assert info.get('proof_assumptions_match')
        proof=(root/(key+'.cpc')).read_text();ops=re.findall(r'^\(([^\s()]+)',proof,re.M)
        assert set(ops)<={'include','declare-const','define','assume','assume-push','step','step-push','step-pop'}
        assert ops.count('include')==2 and ops.count('step-push')+ops.count('assume-push')==ops.count('step-pop')
        assert not re.search(r':rule\s+(?:trust|hole|oracle)\b',proof)
        assert re.search(r'^\(step\s+\S+\s+false\s+:rule\s+',proof.rstrip().splitlines()[-1])
        lines=proof.splitlines(keepends=True);assert all(lines[i].startswith('(include ') for i in (0,1))
        portable='(include "%s")\n(include "%s")\n'%(sig/'Cpc.eo',sig/'expert/CpcExpert.eo')+''.join(lines[2:])
        with tempfile.TemporaryDirectory(prefix='p644-mixed-proof-') as tmp:
            path=Path(tmp)/(key+'.cpc');path.write_text(portable)
            proc=subprocess.run([str(checker),str(path)],text=True,capture_output=True,timeout=240)
        assert proc.returncode==0 and proc.stdout.strip()=='correct',(key,proc.returncode,proc.stdout,proc.stderr)
        info.update(ethos='correct',seconds=round(time.time()-start,3));rows.append(info)
        print('PASS mixed',key,'audited assumptions',info['proof_assumptions'],'Ethos correct',flush=True)
    print('PASS: all intersecting and mixed-disjoint cases; general three-part two-box theorem.',flush=True)
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base',default=str(Path(__file__).parent))
    parser.add_argument('--ethos');parser.add_argument('--report');args=parser.parse_args()
    result=replay(args.base,args.ethos)
    if args.report:Path(args.report).write_text(json.dumps(result,indent=2))
