"""After an abrupt reboot: make each cegar5 body gzip readable up to the checkpointed leaf count.
usage: python3 repair_bodies.py name1 name2 ...   (backs up a damaged body as *.reboot_backup_<n>)"""
import sys, gzip, pickle, zlib, os, shutil
for n in sys.argv[1:]:
    st = pickle.load(open('certs/ck5_%s.pkl' % n, 'rb')); nl = st['nleaves']
    src = 'certs/gcert5_%s.body.gz' % n
    raw = open(src, 'rb').read(); data = b''; complete = True
    while raw:                                   # multi-member gzip (cegar5 appends a member on every resume)
        d = zlib.decompressobj(16 + zlib.MAX_WBITS)
        try: data += d.decompress(raw)
        except zlib.error as e: print(n, 'zlib error', e); complete = False; break
        if not d.eof: complete = False; break    # last member truncated by the reboot
        raw = d.unused_data
    data = data[:data.rfind(b'\n') + 1]         # drop a partial last line
    have = data.count(b'\n')
    if complete and have >= nl:
        print(n, 'ok: complete stream,', have, 'lines >= checkpoint', nl); continue
    if have < nl:
        print(n, 'CANNOT REPAIR: only', have, 'complete lines < checkpoint', nl); continue
    k = 0
    while os.path.exists(src + '.reboot_backup_%d' % k): k += 1
    shutil.copy2(src, src + '.reboot_backup_%d' % k)
    lines = data.split(b'\n')[:nl]
    with gzip.open(src + '.fixed', 'wb') as g: g.write(b'\n'.join(lines) + b'\n')
    os.replace(src + '.fixed', src)
    print(n, 'repaired: kept', nl, 'of', have, 'lines; backup', src + '.reboot_backup_%d' % k)
