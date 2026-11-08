"""Analyze a JSON molecular graph and optional pair of closed spatial curves."""
import argparse
import json
from pathlib import Path
from . import Molecule, linking_number


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--output',type=Path,help='Write JSON report (replaces existing file)')
    parser.add_argument('--subdivisions',type=int,default=8)
    args=parser.parse_args(argv)
    try:
        data=json.loads(args.input.read_text(encoding='utf-8'))
        if not isinstance(data,dict): raise ValueError('Input must be a JSON object')
        report={'graph':Molecule(data['atoms'],data['bonds']).summary()}
        if 'curves' in data:
            curves=data['curves']
            if not isinstance(curves,list) or len(curves)!=2:
                raise ValueError('curves must contain exactly two vertex arrays')
            report['linking']=linking_number(*curves,subdivisions=args.subdivisions)
        encoded=json.dumps(report,indent=2,allow_nan=False)+'\n'
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(encoded,encoding='utf-8')
        print(encoded,end='')
    except (OSError,ValueError,KeyError,TypeError,OverflowError) as exc:
        parser.error(str(exc))


if __name__=='__main__': main()
