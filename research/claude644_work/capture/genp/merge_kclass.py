"""merge frontier-split kclass_par.py outputs into one certificate file (same format as kclass_cert.py).
usage: merge_kclass.py TAG D W  -> cert/TAG_merged.json"""
import sys, json, os
TAG, D, W = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
C = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cert')
parts = [json.load(open(os.path.join(C, f'{TAG}_front{D}.json')))] + [json.load(open(os.path.join(C, f'{TAG}_w{k}of{W}.json'))) for k in range(W)]
out = dict(parts[0]); out['leaves'] = []; st = {'leaves': 0, 'certfail': 0, 'cex': 0, 'nodes': 0}
for P in parts:
    out['leaves'] += P['leaves']
    for k in st: st[k] += P['stats'][k]
out['stats'] = st; out['split'] = {'depth': D, 'workers': W}
json.dump(out, open(os.path.join(C, f'{TAG}_merged.json'), 'w'))
print("merged", TAG, st, "leaves in file", len(out['leaves']))
