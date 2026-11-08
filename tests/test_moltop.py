import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from moltop import Molecule, linking_number


def circle(offset=0,n=24):
    return [(offset+math.cos(2*math.pi*i/n),math.sin(2*math.pi*i/n),0) for i in range(n)]


def hopf():
    return circle(),[(1+math.cos(2*math.pi*i/24),0,math.sin(2*math.pi*i/24)) for i in range(24)]


class GraphTests(unittest.TestCase):
    def test_chain_indices(self):
        s=Molecule(['C']*4,[[0,1],[1,2],[2,3]]).summary()
        self.assertEqual((s['cycle_rank'],s['wiener_index'],s['diameter']),(0,10,3))
        self.assertEqual(s['first_zagreb_index'],10)
        self.assertEqual(s['second_zagreb_index'],8)
        self.assertEqual(len(s['bridges']),3)
        self.assertAlmostEqual(s['randic_index'],2/math.sqrt(2)+0.5)

    def test_benzene(self):
        s=Molecule(['C']*6,[[i,(i+1)%6] for i in range(6)]).summary()
        self.assertEqual(s['cycle_rank'],1)
        self.assertEqual(s['wiener_index'],27)
        self.assertEqual(len(s['cycle_basis'][0]),6)
        self.assertEqual(s['bridges'],[])

    def test_fused_cycles_and_bridge(self):
        m=Molecule(['C']*5,[[0,1],[1,2],[2,0],[1,3],[3,2],[3,4]])
        self.assertEqual(m.summary()['cycle_rank'],2)
        self.assertEqual(len(m.cycle_basis()),2)
        self.assertEqual(m.bridges(),[[3,4]])
        for cycle in m.cycle_basis():
            for i,a in enumerate(cycle): self.assertIn(cycle[(i+1)%len(cycle)],m.adjacency[a])

    def test_disconnected_and_singleton(self):
        s=Molecule(['Na','Cl'],[]).summary()
        self.assertIsNone(s['wiener_index']); self.assertIsNone(s['diameter'])
        self.assertEqual(s['components'],[[0],[1]])
        self.assertEqual(Molecule(['He'],[]).summary()['wiener_index'],0)

    def test_invalid_graphs(self):
        for bonds in [[[0,0]],[[0,1],[1,0]],[[0,2]],[[True,1]],[[0]]]:
            with self.assertRaises(ValueError): Molecule(['C','C'],bonds)
        with self.assertRaises(ValueError): Molecule([],[])


class LinkingTests(unittest.TestCase):
    def test_link_and_orientation(self):
        a,b=hopf()
        value=linking_number(a,b)['estimate']
        self.assertAlmostEqual(abs(value),1,places=3)
        self.assertAlmostEqual(linking_number(b,a)['estimate'],value,places=10)
        self.assertAlmostEqual(linking_number(list(reversed(a)),b)['estimate'],-value,places=10)

    def test_unlink_and_rigid_motion(self):
        self.assertAlmostEqual(linking_number(circle(),circle(4))['estimate'],0,places=10)
        a,b=hopf()
        move=lambda ps:[(2*p[1]+3,-2*p[0]-4,2*p[2]+7) for p in ps]
        self.assertAlmostEqual(linking_number(move(a),move(b))['estimate'],linking_number(a,b)['estimate'],places=10)

    def test_refinement(self):
        a,b=hopf()
        coarse=abs(abs(linking_number(a,b,1)['estimate'])-1)
        fine=abs(abs(linking_number(a,b,16)['estimate'])-1)
        self.assertLess(fine,coarse)
        self.assertLess(fine,1e-4)

    def test_contacts_and_invalid_curves(self):
        a,b=hopf()
        with self.assertRaises(ValueError): linking_number(a,a)
        with self.assertRaises(ValueError): linking_number([(0,0,0),(1,1,0),(0,1,0),(1,0,0)],b)
        with self.assertRaises(ValueError): linking_number([(0,0,0)]*3,b)
        with self.assertRaises(ValueError): linking_number(a,b,0)
        with self.assertRaises(ValueError): linking_number(a,[(float('nan'),0,0)]*3)

    def test_explicit_closure(self):
        a,b=hopf()
        self.assertAlmostEqual(linking_number(a+[a[0]],b+[b[0]])['estimate'],linking_number(a,b)['estimate'])


class CliTests(unittest.TestCase):
    def test_report_export(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'nested'/'result.json'
            proc=subprocess.run([sys.executable,'-m','moltop','examples/benzene.json','--output',str(target)],capture_output=True,text=True,check=True)
            self.assertEqual(json.loads(proc.stdout),json.loads(target.read_text()))
            self.assertEqual(json.loads(proc.stdout)['graph']['cycle_rank'],1)

    def test_bad_input(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'bad.json'; path.write_text('{"atoms":[],"bonds":[]}')
            proc=subprocess.run([sys.executable,'-m','moltop',str(path)],capture_output=True,text=True)
            self.assertEqual(proc.returncode,2)
            self.assertNotIn('Traceback',proc.stderr)


if __name__=='__main__': unittest.main()
