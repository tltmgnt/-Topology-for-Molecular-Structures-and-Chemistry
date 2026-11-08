"""Both bounded synthetic toolkits; not independent scientific reproduction."""
import math
from molecular_topology import analyze
from moltop import Molecule, linking_number

DATA={'schema_version': 1, 'atoms': [{'id': 'o', 'element': 'O'}, {'id': 'h1', 'element': 'H'}, {'id': 'h2', 'element': 'H'}], 'bonds': [{'source': 'o', 'target': 'h1', 'order': 1}, {'source': 'o', 'target': 'h2', 'order': 1}]}


def check():
    explicit=analyze(DATA)
    n=24
    a=[(math.cos(2*math.pi*i/n),math.sin(2*math.pi*i/n),0) for i in range(n)]
    b=[(1+math.cos(2*math.pi*i/n),0,math.sin(2*math.pi*i/n)) for i in range(n)]
    ring=Molecule(['C']*6,[[i,(i+1)%6] for i in range(6)]).summary()
    link=linking_number(a,b)
    passed=explicit['explicit_atom_formula']=='H2O' and explicit['cycle_rank']==0 and ring['wiener_index']==27 and abs(abs(link['estimate'])-1)<.002
    return {'domain':'molecular-structures',
            'statement':'Synthetic explicit water graph checks and MolTop six-cycle/Hopf-link calculations match their scoped references.',
            'passed':bool(passed),
            'configuration':{'explicit_graph':DATA,'ring_atoms':6,'link_vertices':n,'subdivisions':8},
            'observed':{'explicit_graph':explicit,'ring':ring,'link':link},
            'scope':'Two correlated local software fixtures. Explicit graph checks do not establish chemical validity; spatial linking is a numerical estimate, not a certified invariant. No scientific reproduction or medical inference.'}
