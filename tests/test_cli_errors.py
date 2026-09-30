import subprocess,sys,tempfile,unittest,json
from pathlib import Path
class CliErrorTests(unittest.TestCase):
 def test_bad_svg_is_json_error(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.txt';p.write_text('<svg>')
   r=subprocess.run([sys.executable,'-m','hermes_learn','visual','write',str(Path(d)/'out.svg'),str(p)],capture_output=True,text=True)
   self.assertEqual(r.returncode,1)
   self.assertIn('error',json.loads(r.stderr))
