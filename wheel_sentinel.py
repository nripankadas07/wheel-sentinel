import argparse,base64,csv,hashlib,io,json,posixpath,stat,zipfile
from pathlib import Path
def inspect(path,max_bytes=100000000,max_members=10000):
    if max_bytes<=0 or max_members<=0:raise ValueError('limits must be positive')
    errors=[]
    with zipfile.ZipFile(path) as z:
        members=z.infolist()
        if len(members)>max_members:raise ValueError('member limit exceeded')
        if sum(x.file_size for x in members)>max_bytes:raise ValueError('uncompressed size limit exceeded')
        names=[x.filename for x in members]
        if len(names)!=len(set(names)):errors.append({'kind':'duplicate_zip_names'})
        for x in members:
            n=x.filename
            if n.startswith(('/', '\\')) or '\\' in n or ':' in n or any(p in ('..','.') for p in n.split('/')) or '\x00' in n:errors.append({'kind':'unsafe_path','path':n})
            if stat.S_ISLNK(x.external_attr>>16):errors.append({'kind':'symlink','path':n})
            if x.flag_bits&1:errors.append({'kind':'encrypted','path':n})
        records=[n for n in names if n.endswith('.dist-info/RECORD')]
        if len(records)!=1:errors.append({'kind':'record_count','count':len(records)});return {'members':len(names),'errors':errors}
        record=records[0];entries={}
        for row in csv.reader(io.StringIO(z.read(record).decode('utf-8'))):
            if len(row)!=3:raise ValueError('RECORD row must have three fields')
            n,digest,size=row
            if n in entries:errors.append({'kind':'duplicate_record_path','path':n})
            entries[n]=(digest,size)
        files={x.filename:x for x in members if not x.is_dir()}
        for n in sorted(files):
            if n not in entries:
                if not n.endswith(('.dist-info/RECORD.jws','.dist-info/RECORD.p7s')):errors.append({'kind':'unrecorded_file','path':n})
                continue
            digest,size=entries[n]
            if n==record:
                if digest or size:errors.append({'kind':'record_self_hash','path':n})
                continue
            if not digest or not size:errors.append({'kind':'missing_hash_or_size','path':n});continue
            try:
                algorithm,expected=digest.split('=',1)
                if algorithm not in ('sha256','sha384','sha512'):raise ValueError('unsupported hash')
                wanted=int(size)
                if wanted<0:raise ValueError('negative size')
                h=hashlib.new(algorithm)
                with z.open(n) as f:
                    while True:
                        b=f.read(65536)
                        if not b:break
                        h.update(b)
                actual=base64.urlsafe_b64encode(h.digest()).rstrip(b'=').decode('ascii')
                if actual!=expected:errors.append({'kind':'hash_mismatch','path':n})
                if wanted!=files[n].file_size:errors.append({'kind':'size_mismatch','path':n})
            except (ValueError,UnicodeError):errors.append({'kind':'invalid_record_digest','path':n})
        for n in sorted(entries.keys()-files.keys()):errors.append({'kind':'record_missing_file','path':n})
        return {'members':len(names),'errors':errors}
def main():
    p=argparse.ArgumentParser();p.add_argument('wheel');p.add_argument('--max-bytes',type=int,default=100000000);p.add_argument('--max-members',type=int,default=10000);a=p.parse_args()
    try:r=inspect(a.wheel,a.max_bytes,a.max_members)
    except (ValueError,OSError,UnicodeError,zipfile.BadZipFile,RuntimeError) as e:p.exit(2,str(e)+'\n')
    print(json.dumps(r,indent=2));return int(bool(r['errors']))
if __name__=='__main__':raise SystemExit(main())
