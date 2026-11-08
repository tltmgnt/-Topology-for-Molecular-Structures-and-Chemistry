"""Scoped synthetic domain adapter; no external execution."""
import math
from moltop import Molecule, linking_number

def check():
    n=24
    a=[(math.cos(2*math.pi*i/n),math.sin(2*math.pi*i/n),0) for i in range(n)]
    b=[(1+math.cos(2*math.pi*i/n),0,math.sin(2*math.pi*i/n)) for i in range(n)]
    ring=Molecule(['C']*6,[[i,(i+1)%6] for i in range(6)]).summary()
    link=linking_number(a,b)
    return {'domain':'molecular-structures','statement':'The synthetic six-cycle has Wiener index 27 and the ideal Hopf link estimates linking magnitude 1.',
            'passed':ring['wiener_index']==27 and abs(abs(link['estimate'])-1)<0.002,
            'configuration':{'ring_atoms':6,'link_vertices':n,'subdivisions':8},'observed':{'ring':ring,'link':link},
            'scope':'Mathematical software fixture, not a real molecule or scientific replication'}
