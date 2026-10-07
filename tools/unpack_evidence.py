from pathlib import Path
import zipfile, hashlib
root=Path(__file__).resolve().parent.parent
count=0
for archive in sorted((root/'evidence').glob('*.zip')):
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            dest=(root/member.filename).resolve()
            if not dest.is_relative_to(root): raise ValueError('Unsafe archive member')
            if member.is_dir(): continue
            data=z.read(member)
            if dest.exists():
                if hashlib.sha256(dest.read_bytes()).digest()!=hashlib.sha256(data).digest():
                    raise FileExistsError('Refusing to overwrite different file: '+str(dest))
            else:
                dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
            count+=1
print('Verified or extracted',count,'evidence members; existing different files were not overwritten')
