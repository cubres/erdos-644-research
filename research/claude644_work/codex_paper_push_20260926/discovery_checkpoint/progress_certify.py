"""Checkpointed exact certification using the original rational certifier.

Only completed subtrees are reused. The independent checker still verifies the
entire final object, so checkpoint markers are never accepted as proof evidence.
"""
import sys,json,time,hashlib
from pathlib import Path
from fractions import Fraction as F
SRC='/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c'
sys.path.insert(0,SRC)
import b4core as bc
import certify5 as cert
from fast_duals import install as install_fast_duals, STATS as FAST_STATS
install_fast_duals(cert)

source=Path(sys.argv[1]);target=Path(sys.argv[2]);partial=Path(str(target)+'.partial.json')
digest=hashlib.sha256(source.read_bytes()).hexdigest()
D=json.loads(source.read_text())
if partial.exists():
    previous=json.loads(partial.read_text())
    if previous.get('source_sha256')==digest:D=previous['certificate']
if 'strict-types' in D.get('extensions',[]):
    from strict_types import install
    install()
old_walk=cert.walk;started=time.time();last=started;last_save=started;done=0;hits=0
def walk(node,C,E,nt):
    global last,last_save,done,hits
    if node.get('_certification_complete'):
        hits+=1;return
    old_walk(node,C,E,nt)
    node['_certification_complete']=True;done+=1
    now=time.time()
    if now-last>25:
        print('CERT_PROGRESS',done,'reused',hits,'stats',cert.STATS,'fast',FAST_STATS,'seconds',round(now-started),flush=True)
        last=now
    if now-last_save>90:
        partial.write_text(json.dumps({'source_sha256':digest,'certificate':D}))
        last_save=now
cert.walk=walk
lo=[F(v) for v in D['box'][0]];hi=[F(v) for v in D['box'][1]]
C,E=bc.base_region(D['balanced'],D['sorted'],(lo,hi),D.get('excess',False))
try:
    walk(D['tree'],C,E,0)
except BaseException:
    partial.write_text(json.dumps({'source_sha256':digest,'certificate':D}))
    raise
def clean(node):
    node.pop('_certification_complete',None)
    for kid in node.get('kids',[]):clean(kid[1] if isinstance(kid,list) else kid)
clean(D['tree'])
target.write_text(json.dumps(D))
print('CERTIFIED',source,cert.STATS,'fast',FAST_STATS,'seconds',round(time.time()-started,1),flush=True)
