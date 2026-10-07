from pathlib import Path
import zipfile, hashlib, json
root=Path(__file__).resolve().parent.parent
entries=json.loads((root/'provenance/recovered-files.json').read_text())
archived={e['member']:e for e in entries if e.get('storage')=='evidence_archive'}
def preserve(dest,data):
    if not dest.is_relative_to(root): raise ValueError('Unsafe archive member')
    if dest.exists():
        if hashlib.sha256(dest.read_bytes()).digest()!=hashlib.sha256(data).digest():
            raise FileExistsError('Refusing to overwrite different file: '+str(dest))
    else:
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
count=0
for archive in sorted((root/'evidence').glob('*.zip')):
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            if member.is_dir():continue
            data=z.read(member)
            if member.filename in archived:
                entry=archived[member.filename]
                if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
                    raise ValueError('Evidence hash mismatch: '+member.filename)
            preserve((root/member.filename).resolve(),data);count+=1
for e in entries:
    if e.get('storage')!='evidence_archive_parts':continue
    data=b''.join((root/p['member']).read_bytes() for p in e['parts'])
    if len(data)!=e['bytes'] or hashlib.sha256(data).hexdigest()!=e['sha256']:
        raise ValueError('Reconstructed evidence hash mismatch: '+e['origin'])
    preserve((root/e['origin']).resolve(),data)
print('Verified or extracted',count,'archive members and reconstructed all split files')
