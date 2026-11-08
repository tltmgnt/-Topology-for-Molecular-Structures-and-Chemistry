"""Verify the installed MolTop interface outside the source checkout."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

with tempfile.TemporaryDirectory() as directory:
    for filename in ('benzene.json','hopf-link.json'):
        output=Path(directory)/filename
        result=subprocess.run([sys.executable,'-I','-m','moltop',str(ROOT/'examples'/filename),
                               '--output',str(output)],cwd=directory,capture_output=True,text=True,check=True)
        report=json.loads(result.stdout)
        assert report==json.loads(output.read_text())
        assert 'graph' in report
        if filename=='benzene.json':assert report['graph']['wiener_index']==27
        else:assert abs(abs(report['linking']['estimate'])-1)<.002
print('Installed MolTop graph and linking CLI passed outside source tree')
