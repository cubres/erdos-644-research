"""pending stack entries per depth (from a gen_certp checkpoint): python3 progress.py certs/gcertp_<tag>_<pi0>.jsonl.gz.ck.pkl"""
import sys, pickle
for fn in sys.argv[1:]:
    st = pickle.load(open(fn, 'rb')); stack = st['stack']
    dep = {}
    for e in stack: dep[len(e[0])] = dep.get(len(e[0]), 0) + 1
    top = sorted(dep.items())[:8]
    print(fn.split('/')[-1], 'nodes', st['nodes'], 'leaves', st['nleaves'], 'stack', len(stack), 'pending by depth', top)
    if stack:
        deep = max(stack, key=lambda e: len(e[0]))[0]
        print('  current path (first 8):', [(nm[:30], ai) for nm, ai in deep[:8]])
