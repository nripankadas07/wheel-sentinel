import tempfile,unittest,zipfile,base64,hashlib,io,csv
from pathlib import Path
from wheel_sentinel import inspect
def fixture(path,body=b'x=1\n',recordbody=None,name='demo.py'):
 digest=base64.urlsafe_b64encode(hashlib.sha256(body).digest()).rstrip(b'=').decode();s=io.StringIO();w=csv.writer(s);w.writerow([name,'sha256='+digest,len(body)]);w.writerow(['demo-0.1.dist-info/RECORD','',''])
 with zipfile.ZipFile(path,'w') as z:z.writestr(name,recordbody if recordbody is not None else body);z.writestr('demo-0.1.dist-info/RECORD',s.getvalue())
class Tests(unittest.TestCase):
 def test_valid_hashes(self):
  with tempfile.TemporaryDirectory() as d:p=Path(d,'a.whl');fixture(p);self.assertEqual(inspect(p)['errors'],[])
 def test_tamper(self):
  with tempfile.TemporaryDirectory() as d:p=Path(d,'a.whl');fixture(p,recordbody=b'x=2\n');self.assertIn('hash_mismatch',[x['kind'] for x in inspect(p)['errors']])
 def test_traversal_no_extraction(self):
  with tempfile.TemporaryDirectory() as d:p=Path(d,'a.whl');fixture(p,name='../escape');self.assertIn('unsafe_path',[x['kind'] for x in inspect(p)['errors']]);self.assertFalse(Path(d,'escape').exists())
 def test_size_bound(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d,'a.whl');fixture(p)
   with self.assertRaises(ValueError):inspect(p,max_bytes=1)
 def test_record_missing(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d,'a.whl')
   with zipfile.ZipFile(p,'w') as z:z.writestr('demo.py','x')
   self.assertEqual(inspect(p)['errors'][0]['kind'],'record_count')
