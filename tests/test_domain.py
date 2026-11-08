import copy,itertools,tempfile,unittest
from pathlib import Path
from molecular_topology import analyze
from molecular_topology.io import create,verify

def molecule(elements,bonds):return {'schema_version':1,'atoms':[{'id':str(i),'element':e} for i,e in enumerate(elements)],'bonds':[{'source':str(a),'target':str(b),'order':o} for a,b,o in bonds]}

class DomainTests(unittest.TestCase):
    def test_water(self):
        r=analyze(molecule(['O','H','H'],[(0,1,1),(0,2,1)]));self.assertEqual(r['explicit_atom_formula'],'H2O');self.assertEqual(r['cycle_rank'],0);self.assertEqual(r['within_component_wiener_sum'],4)
    def test_explicit_no_implicit_hydrogen(self):self.assertEqual(analyze(molecule(['C'],[]))['explicit_atom_formula'],'C')
    def test_triangle_ring(self):self.assertEqual(analyze(molecule(['C']*3,[(0,1,1),(1,2,1),(2,0,1)]))['cycle_rank'],1)
    def test_bond_order_not_graph_cycle(self):self.assertEqual(analyze(molecule(['C','O'],[(0,1,2)]))['cycle_rank'],0)
    def test_disconnected(self):self.assertEqual(len(analyze(molecule(['H','H'],[]))['components']),2)
    def test_valence_failure(self):
        r=analyze(molecule(['H','O'],[(0,1,2)]));self.assertEqual(r['status'],'FAIL');self.assertEqual(r['valence_upper_bound_violations'],['0'])
    def test_relabeling(self):
        d=molecule(['C','O','H','H'],[(0,1,1),(0,2,1),(1,3,1)]);r=analyze(d)
        mapping={'0':'z','1':'a','2':'x','3':'b'}
        for a in d['atoms']:a['id']=mapping[a['id']]
        for b in d['bonds']:b['source']=mapping[b['source']];b['target']=mapping[b['target']]
        d['atoms'].reverse();d['bonds'].reverse();q=analyze(d)
        for k in ['cycle_rank','within_component_wiener_sum','local_descriptor_counts','explicit_atom_formula']:self.assertEqual(r[k],q[k])
    def test_all_64_carbon_graphs_cycle_oracle(self):
        edges=list(itertools.combinations(range(4),2))
        for mask in range(64):
            bonds=[(*e,1) for i,e in enumerate(edges) if mask>>i&1];r=analyze(molecule(['C']*4,bonds))
            # Forest edge count from disjoint-set merging, independently of traversal.
            parent=list(range(4));merges=0
            def find(i):
                while parent[i]!=i:i=parent[i]
                return i
            for a,b,_ in bonds:
                a,b=find(a),find(b)
                if a!=b:parent[a]=b;merges+=1
            self.assertEqual(r['cycle_rank'],len(bonds)-merges)
    def test_aromatic_order_unsupported(self):
        with self.assertRaises(ValueError):analyze(molecule(['C','C'],[(0,1,1.5)]))
    def test_extra_charge_rejected(self):
        d=molecule(['N'],[]);d['atoms'][0]['charge']=1
        with self.assertRaises(ValueError):analyze(d)
    def test_duplicate_bond(self):
        with self.assertRaises(ValueError):analyze(molecule(['C','C'],[(0,1,1),(1,0,1)]))
    def test_missing_endpoint(self):
        with self.assertRaises(ValueError):analyze(molecule(['C'],[(0,1,1)]))
    def test_replay_failure(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';create(p,molecule(['H','O'],[(0,1,2)]));self.assertEqual(verify(p)['status'],'FAIL')
