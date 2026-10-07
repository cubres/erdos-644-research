"""Bounded numerical discovery over all empty-common cores containing G.

Preserve and reuse existing per-model results. This is not an exact
infeasibility certificate, even when every numerical solve is optimal.
"""
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
G_TYPES = tuple(map(set, ('235', '246', '145', '136', '123', '124')))


def jobs():
    for deficits in ('1,1,1,1', '2,2,0,0'):
        for requests in (1, 2, 3):
            for old in combinations('123456', 5 - requests):
                if any(set(old) <= membership for membership in G_TYPES):
                    continue
                yield deficits, ''.join(old) + 'G', requests


def run(job):
    deficits, core, requests = job
    slug = deficits.replace(',', '_')
    path = ROOT / 'outputs' / ('agent_pivot_arbitrary_%s_%s_%s.json'
                               % (slug, core, requests))
    cached = path.exists()
    if not cached:
        proc = subprocess.run(
            [sys.executable, str(ROOT / 'work/p644_pivot_arbitrary_request_discover.py'),
             '--deficits', deficits, '--core', core, '--requests', str(requests),
             '--time', '20'], cwd=str(ROOT), capture_output=True, text=True)
        if proc.returncode:
            raise RuntimeError(proc.stderr)
    result = json.loads(path.read_text())
    assert result['core'] == core and result['requests'] == requests
    assert result['deficits'] == [int(x) for x in deficits.split(',')]
    assert result['positive_cell_cutoff'] is None
    assert result['endpoint_upper_bound'] == 110.999
    return dict(deficits=deficits, core=core, requests=requests,
                status=result['status'], best_budget=result['best_budget'],
                dual_bound=result['dual_bound'], reused=cached,
                source=str(path.relative_to(ROOT)))


def main():
    inputs = list(jobs())
    assert len(inputs) == 62
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(run, inputs))
    summary = dict(scope='Numerical discovery only, not an impossibility proof',
                   target_budget=109.5, endpoint_upper_bound=110.999,
                   positive_cell_cutoff=None, models=rows)
    path = ROOT / 'outputs/root_pivot_arbitrary_core_batch.json'
    path.write_text(json.dumps(summary, indent=2) + '\n')
    for deficits in ('1,1,1,1', '2,2,0,0'):
        for requests in (1, 2, 3):
            subset = [r for r in rows if r['deficits'] == deficits
                      and r['requests'] == requests]
            feasible = [r['best_budget'] for r in subset
                        if r['best_budget'] is not None]
            print(json.dumps(dict(deficits=deficits, requests=requests,
                                  models=len(subset),
                                  all_status_zero=all(r['status'] == 0 for r in subset),
                                  best_budget=min(feasible) if feasible else None)))
    print('Cached results reused: %s/%s' % (sum(r['reused'] for r in rows), len(rows)))


if __name__ == '__main__':
    main()
