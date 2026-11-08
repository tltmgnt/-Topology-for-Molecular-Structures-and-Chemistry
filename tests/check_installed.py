import json,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as directory:
    bundle=Path(directory)/'bundle'
    for args in (["molecular-topology","analyze",str(ROOT/'examples/reference.json'),"--output",str(bundle)],["molecular-topology","verify",str(bundle)]):
        r=subprocess.run(args,cwd=directory,capture_output=True,text=True,check=True)
        assert json.loads(r.stdout)['execution_authorized'] is False
print('Installed domain CLI passed outside source tree')
