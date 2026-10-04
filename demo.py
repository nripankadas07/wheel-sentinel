import tempfile,json,zipfile,hashlib,base64,csv,io
from pathlib import Path
from wheel_sentinel import inspect
with tempfile.TemporaryDirectory() as d:
 p=Path(d,'demo.whl');body=b'x=1\n';digest=base64.urlsafe_b64encode(hashlib.sha256(body).digest()).rstrip(b'=').decode();record=io.StringIO();writer=csv.writer(record);writer.writerow(['demo.py','sha256='+digest,len(body)]);writer.writerow(['demo-0.1.dist-info/RECORD','',''])
 with zipfile.ZipFile(p,'w') as z:z.writestr('demo.py',b'x=2\n');z.writestr('demo-0.1.dist-info/RECORD',record.getvalue())
 print(json.dumps(inspect(p),indent=2))
