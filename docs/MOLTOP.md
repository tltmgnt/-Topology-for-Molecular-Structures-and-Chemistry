# MolTop graph and spatial linking toolkit

**MolTop** is a dependency-free Python toolkit for molecular graph descriptors and numerical linking estimates of closed spatial curves. It makes the distinction between connectivity and embedding explicit: two disconnected ring graphs alone do not reveal whether their 3D curves are linked.

## Quick start

Python 3.10 or newer is required. From the repository root:

```bash
python -m moltop examples/benzene.json --output output/benzene.json
python -m moltop examples/hopf-link.json --output output/link.json
python -m moltop examples/hopf-link.json --subdivisions 16
```

Commands print a JSON report. `--output` also writes it to a file, creating parent directories and replacing an existing file. Install the package to use the `moltop` command:

```bash
python -m pip install .
moltop --help
```

## Input format

```json
{
  "atoms": ["C", "C", "O"],
  "bonds": [[0, 1], [1, 2]]
}
```

Atom indices are zero based. Atom labels are arbitrary nonempty metadata strings, not validated elements. Bonds are undirected, unweighted pairs. Self bonds and duplicate bonds (including reversed duplicates) are rejected. Include explicit hydrogen atoms only if they should contribute to graph descriptors; the toolkit does not add or remove them.

An optional `curves` field contains exactly two arrays of 3D vertices. Each curve is closed implicitly; repeating the first vertex at the end is also accepted. Curve vertices are independent of graph atoms: no correspondence is inferred. The Hopf example deliberately uses two coarse three-atom rings to illustrate graph connectivity and separate, more finely sampled ideal curves for the geometric calculation. It is a mathematical fixture, not a physically realistic molecular conformation.

## Python API

```python
from moltop import Molecule, linking_number

molecule = Molecule(["C"] * 6, [[i, (i + 1) % 6] for i in range(6)])
print(molecule.summary())
print(molecule.distances(0))

# curve_a and curve_b are ordered lists of 3D vertices.
# result = linking_number(curve_a, curve_b, subdivisions=16)
```

## Graph descriptors

| Output | Definition |
| --- | --- |
| Components | Atom-index lists for connected components |
| Degrees | Number of neighboring atoms per vertex |
| Cycle rank | E − V + C: dimension of the graph cycle space |
| Cycle basis | Deterministic fundamental cycles from a breadth-first spanning forest; closure is implicit |
| Bridges | Bonds whose removal increases the number of components |
| Wiener index | Sum of shortest-path lengths over unordered distinct atom pairs |
| Diameter | Largest shortest-path distance |
| Randić index | Sum over bonds of 1 / √(degree(u) degree(v)) |
| First Zagreb index | Sum over atoms of degree² |
| Second Zagreb index | Sum over bonds of degree(u) degree(v) |

Wiener index and diameter are `null` for disconnected graphs. For a single atom they are zero. A six-carbon ring has cycle rank 1, Wiener index 27, diameter 3, and no bridges. A four-atom path has Wiener index 10 and three bridges.

The basis is not a unique set of chemical rings, not a minimum cycle basis, and not an SSSR perception algorithm. Graph descriptors ignore bond order, aromaticity, valence, stereochemistry, coordinates, and atom identity. They cannot uniquely identify a molecule or predict chemical properties without an independently validated model.

## Spatial linking

`linking_number` estimates the Gauss double integral using midpoint quadrature on subdivided polygon edges. Default subdivision count is 8. The report includes the raw estimate and minimum inter-curve segment separation. The ideal Hopf link has linking-number magnitude 1, while separated planar circles give zero. Reversing one curve's orientation reverses the sign; exchanging curves preserves it.

Always compare subdivision counts (for example 8 and 16) and refine the original geometric curves when needed. The reported value is a numerical estimate, not a certified integer invariant. Do not round a poorly converged value and treat it as proof. Near contacts can demand substantial refinement. Coordinates must share one length unit; `minimum_separation` and the absolute contact tolerance (default 1e-9) use that unit.

Intersecting or near-contact curves and nonadjacent self-intersections are rejected using segment distances. This floating-point check is not a robust exact geometric predicate. Degenerate adjacent overlapping edges are not exhaustively validated; supply simple, nondegenerate closed curves. The implementation does not classify knots, calculate knot polynomials, or detect all links: a zero linking number does not prove two curves are unlinked. Open molecular chains require an explicit, justified closure supplied by the caller.

## Scope and limits

Graphs support up to 1000 atoms. Curves support up to 2000 input vertices; quadrature is capped at two million sample pairs, and subdivisions range from 1 to 32. Validation and integration use quadratic pairwise loops and are intended for small educational/research examples. No SMILES, SDF, PDB, periodic boundary handling, molecular force fields, geometry optimization, or chemical sanitization is included. JSON is the supported interchange format.

## Development

```bash
python -m unittest discover -s tests -v
```

Tests cover analytic graph descriptors, fused cycles and bridges, disconnected graphs, invalid input, the Hopf link, quadrature refinement, orientation and rigid-motion invariance, contact rejection, and CLI JSON export. GitHub Actions installs the package and runs tests and CLI examples on Python 3.10, 3.12, and 3.13.

Licensed under Apache 2.0; see [LICENSE](../LICENSE).
