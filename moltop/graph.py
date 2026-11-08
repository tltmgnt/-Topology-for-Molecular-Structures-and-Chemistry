"""Undirected molecular connectivity, independent of chemical perception rules."""
from collections import deque
import math


class Molecule:
    """Simple graph: atom labels are metadata; bond orders do not weight topology."""
    def __init__(self, atoms, bonds):
        if not isinstance(atoms, list) or not atoms or any(not isinstance(a,str) or not a.strip() for a in atoms):
            raise ValueError('atoms must be a nonempty list of nonempty labels')
        if len(atoms) > 1000:
            raise ValueError('At most 1000 atoms are supported')
        if not isinstance(bonds,list):
            raise ValueError('bonds must be a list of index pairs')
        self.atoms = tuple(atoms)
        self.adjacency = [set() for _ in atoms]
        edges = set()
        for bond in bonds:
            if not isinstance(bond,(list,tuple)) or len(bond) != 2:
                raise ValueError('Each bond must contain two atom indices')
            a,b = bond
            if any(type(v) is not int or not 0 <= v < len(atoms) for v in bond):
                raise ValueError('Bond indices must be integers in range')
            edge = tuple(sorted((a,b)))
            if a == b or edge in edges:
                raise ValueError('Self bonds and duplicate bonds are not supported')
            edges.add(edge)
            self.adjacency[a].add(b); self.adjacency[b].add(a)
        self.edges = tuple(sorted(edges))

    def distances(self, source):
        if type(source) is not int or not 0 <= source < len(self.atoms):
            raise ValueError('Source must be an atom index')
        distance = {source:0}
        queue = deque([source])
        while queue:
            a = queue.popleft()
            for b in sorted(self.adjacency[a]):
                if b not in distance:
                    distance[b] = distance[a]+1
                    queue.append(b)
        return distance

    def components(self):
        remaining = set(range(len(self.atoms)))
        result = []
        while remaining:
            component = sorted(self.distances(min(remaining)))
            remaining.difference_update(component)
            result.append(component)
        return result

    def cycle_basis(self):
        """Deterministic fundamental basis from a spanning forest, not SSSR."""
        parent, depth, tree = {}, {}, set()
        for root in range(len(self.atoms)):
            if root in parent:
                continue
            parent[root],depth[root] = None,0
            queue=deque([root])
            while queue:
                a=queue.popleft()
                for b in sorted(self.adjacency[a]):
                    if b not in parent:
                        parent[b],depth[b] = a,depth[a]+1
                        tree.add(tuple(sorted((a,b))))
                        queue.append(b)
        cycles=[]
        for a,b in self.edges:
            if (a,b) in tree:
                continue
            left,right=[a],[b]
            while depth[left[-1]] > depth[right[-1]]:
                left.append(parent[left[-1]])
            while depth[right[-1]] > depth[left[-1]]:
                right.append(parent[right[-1]])
            while left[-1] != right[-1]:
                left.append(parent[left[-1]]); right.append(parent[right[-1]])
            cycles.append(left+list(reversed(right[:-1])))
        return cycles

    def bridges(self):
        """An edge is a bridge exactly when no basis cycle contains it."""
        cyclic=set()
        for cycle in self.cycle_basis():
            for i,a in enumerate(cycle):
                cyclic.add(tuple(sorted((a,cycle[(i+1)%len(cycle)]))))
        return [list(e) for e in self.edges if e not in cyclic]

    def summary(self):
        components=self.components()
        degrees=[len(n) for n in self.adjacency]
        total,diameter=0,0
        for a in range(len(self.atoms)):
            distance=self.distances(a)
            total += sum(d for b,d in distance.items() if b>a)
            diameter=max(diameter,max(distance.values()))
        connected=len(components)==1
        return {'atom_count':len(self.atoms),'bond_count':len(self.edges),
                'components':components,'degrees':degrees,
                'cycle_rank':len(self.edges)-len(self.atoms)+len(components),
                'cycle_basis':self.cycle_basis(),'bridges':self.bridges(),
                'wiener_index':total if connected else None,
                'diameter':diameter if connected else None,
                'randic_index':sum(1/math.sqrt(degrees[a]*degrees[b]) for a,b in self.edges),
                'first_zagreb_index':sum(d*d for d in degrees),
                'second_zagreb_index':sum(degrees[a]*degrees[b] for a,b in self.edges)}
