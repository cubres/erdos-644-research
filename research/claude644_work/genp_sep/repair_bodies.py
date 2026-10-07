"""After an abrupt reboot: make each gen_certp body gzip readable up to the checkpointed leaf count.
usage: python3 repair_bodies.py certs/gcertp_<tag>_<pi0>.jsonl.gz ...   (body = <..>.body, checkpoint = <..>.ck.pkl)
Backs up a damaged body as *.reboot_backup_<n>.  Multi-member gzip handled (each resume appends a member)."""
import sys, gzip, pickle, zlib, os, shutil
for fin in sys.argv[1:]:
    body = fin + '.body'; ck = fin + '.ck.pkl'
    nl = pickle.load(open(ck, 'rb'))['nleaves']
    raw = open(body, 'rb').read(); data = b''; complete = True; members = 0
    while raw:
        d = zlib.decompressobj(16 + zlib.MAX_WBITS)
        try: data += d.decompress(raw)
        except zlib.error as e: print(fin, 'zlib error', e); complete = False; break
        members += 1
        if not d.eof: complete = False; break       # last member truncated
        raw = d.unused_data
    data = data[:data.rfind(b'\n') + 1]
    have = data.count(b'\n')
    print(fin.split('/')[-1], 'members', members, 'complete' if complete else 'TRUNCATED', 'lines', have, 'checkpoint', nl)
    if complete and have == nl:
        print('  ok'); continue
    if have < nl:
        print('  SHORT by', nl - have, 'leaves: keeping', have, '(gap to patch later from missing-alternative report)')
        keep = have
    else:
        keep = nl
    k = 0
    while os.path.exists(body + '.reboot_backup_%d' % k): k += 1
    shutil.copy2(body, body + '.reboot_backup_%d' % k)
    lines = data.split(b'\n')[:keep]
    with gzip.open(body + '.fixed', 'wb') as g: g.write(b'\n'.join(lines) + b'\n')
    os.replace(body + '.fixed', body)
    print('  rewritten with', keep, 'lines; backup', body + '.reboot_backup_%d' % k)
