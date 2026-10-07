"""Replay the complete three-part, two-box certificate.

The model/assumption audit uses Python's standard library. Proof inference is
checked by the separate Ethos executable against the bundled cvc5 signatures.
Neither SMT solver nor discovery program is imported or required.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time

from p644_box_input_audit import audit
from p644_line_template_check import check as check_example

CASES = ['000','001','003','011','012','013_line','033',
         '111','112','113','123','133','333']


def replay(base, ethos=None):
    base = Path(base).resolve()
    manifest = json.loads((base/'MANIFEST.json').read_text())
    for rel, digest in manifest['sha256'].items():
        path = base/rel
        assert path.is_file(), ('missing file', rel)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, ('hash mismatch', rel)
    print('PASS: all %d manifest hashes' % len(manifest['sha256']), flush=True)
    reps = {min(tuple(sorted(s)), tuple(sorted({0:0,1:2,2:1,3:3}[v] for v in s)))
            for s in itertools.product(range(4), repeat=3)}
    assert {tuple(map(int,s[:3])) for s in CASES} == reps and len(reps) == 13
    root = base/'logs/astra_box_case_pipeline'
    sig = base/'proof_checkers/cvc5-1.4.0-signatures/cpc'
    checker = Path(ethos).resolve() if ethos else base/'proof_checkers/ethos-0.2.4/ethos'
    allowed = {'include','declare-const','define','assume','assume-push','step','step-push','step-pop'}
    rows = []
    for key in CASES:
        start = time.time()
        info = audit(key, root)
        assert info.get('proof_assumptions_match') is True
        proof = (root/(key+'.cpc')).read_text()
        commands = re.findall(r'^\(([^\s()]+)', proof, re.M)
        assert set(commands) <= allowed, ('unexpected proof command', key)
        assert commands.count('include') == 2
        assert commands.count('step-push') + commands.count('assume-push') == commands.count('step-pop')
        assert not re.search(r':rule\s+(?:trust|hole|oracle)\b', proof)
        assert re.search(r'^\(step\s+\S+\s+false\s+:rule\s+', proof.rstrip().splitlines()[-1])
        # Only the two checker signature locations change. The inference body,
        # audited assumptions and asserted final false conclusion stay intact.
        lines = proof.splitlines(keepends=True)
        assert all(lines[i].startswith('(include ') for i in (0,1))
        portable = '(include "%s")\n(include "%s")\n' % (sig/'Cpc.eo', sig/'expert/CpcExpert.eo')
        portable += ''.join(lines[2:])
        with tempfile.TemporaryDirectory(prefix='p644-proof-replay-') as tmp:
            target = Path(tmp)/(key+'.cpc')
            target.write_text(portable)
            proc = subprocess.run([str(checker), str(target)], capture_output=True,
                                  text=True, timeout=240)
        assert proc.returncode == 0 and proc.stdout.strip() == 'correct', (key, proc.returncode, proc.stdout, proc.stderr)
        info.update(ethos='correct', final_conclusion='false', seconds=round(time.time()-start,3))
        rows.append(info)
        print('PASS:', key, info['proof_assumptions'], 'audited assumptions; Ethos correct;', info['seconds'], 'seconds', flush=True)
    check_example(json.loads((base/'logs/astra_line_template_example.json').read_text()))
    print('PASS: complete theorem certificate; all 64 support patterns in 13 orbits.', flush=True)
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default=str(Path(__file__).resolve().parent))
    parser.add_argument('--ethos', help='Alternative Ethos 0.2.4 executable for this platform')
    parser.add_argument('--report', help='Optional JSON replay report')
    args = parser.parse_args()
    result = replay(args.base, args.ethos)
    if args.report:
        Path(args.report).write_text(json.dumps(result, indent=2))
