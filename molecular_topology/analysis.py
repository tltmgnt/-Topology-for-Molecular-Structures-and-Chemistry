"""Explicit neutral molecular graphs: connectivity, cycle rank and local descriptors."""
from collections import Counter

VALENCE={'H':1,'B':3,'C':4,'N':3,'O':2,'F':1,'P':5,'S':6,'Cl':1,'Br':1,'I':1}


def analyze(data):
    if not isinstance(data,dict) or set(data)!={'schema_version','atoms','bonds'} or type(data['schema_version']) is not int or data['schema_version']!=1:raise ValueError('exact schema_version 1, atoms, bonds required')
    atoms,bonds=data['atoms'],data['bonds']
    if not isinstance(atoms,list) or not 1<=len(atoms)<=64:raise ValueError('require 1..64 explicit atoms')
    elements={}
    for atom in atoms:
        if not isinstance(atom,dict) or set(atom)!={'id','element'} or not isinstance(atom['id'],str) or not 1<=len(atom['id'])<=32 or not isinstance(atom['element'],str) or atom['element'] not in VALENCE:raise ValueError('supported explicit atom record required')
        if atom['id'] in elements:raise ValueError('duplicate atom')
        elements[atom['id']]=atom['element']
    if not isinstance(bonds,list) or len(bonds)>128:raise ValueError('at most 128 bonds')
    neighbors={n:{} for n in elements};seen=set()
    for bond in bonds:
        if not isinstance(bond,dict) or set(bond)!={'source','target','order'}:raise ValueError('exact bond fields required')
        a,b,order=bond['source'],bond['target'],bond['order']
        if not isinstance(a,str) or not isinstance(b,str) or a not in elements or b not in elements or a==b or type(order) is not int or order not in (1,2,3):raise ValueError('supported endpoints and integer bond order 1..3 required')
        key=tuple(sorted((a,b)))
        if key in seen:raise ValueError('parallel/duplicate bond')
        seen.add(key);neighbors[a][b]=order;neighbors[b][a]=order
    unseen=set(elements);parts=[];distance_sum=0
    for source in sorted(elements):
        distances={source:0};queue=[source]
        for node in queue:
            for target in sorted(neighbors[node]):
                if target not in distances:distances[target]=distances[node]+1;queue.append(target)
        distance_sum+=sum(distances.values())
        if source in unseen:
            part=sorted(distances);parts.append(part);unseen-=set(part)
    counts=Counter(elements.values())
    element_order=(['C','H']+sorted(set(counts)-{'C','H'})) if 'C' in counts else sorted(counts)
    formula=''.join(e+(str(counts[e]) if counts[e]>1 else '') for e in element_order if counts[e])
    gaps=[n for n in sorted(elements) if sum(neighbors[n].values())>VALENCE[elements[n]]]
    descriptors=Counter(elements[n]+'|'+','.join(sorted(elements[t]+':'+str(o) for t,o in neighbors[n].items())) for n in elements)
    return {'schema_version':1,'domain':'chemistry','status':'FAIL' if gaps else 'PASS','explicit_atom_formula':formula,
            'atom_count':len(elements),'bond_count':len(bonds),'components':parts,
            'cycle_rank':len(bonds)-len(elements)+len(parts),'within_component_wiener_sum':distance_sum//2,
            'valence_upper_bound_violations':gaps,'local_descriptor_counts':dict(sorted(descriptors.items())),
            'execution_authorized':False,'clinical_use_authorized':False,
            'scope':'Explicit atoms and integer bonds only; no implicit hydrogens, aromaticity, charges, stereochemistry, canonical isomorphism, energies, chemical feasibility, synthesis or therapeutic inference. Valence checks are declared upper bounds, not chemical validation.'}
