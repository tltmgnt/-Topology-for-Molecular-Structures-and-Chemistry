# Topology compatibility and curriculum v2 — -Topology-for-Molecular-Structures-and-Chemistry

Version 2 adapts the explicit-molecular-graph teaching pattern to this repository's actual role. This is documentation and a learning/decision framework; it introduces no mathematical engine, runtime dependency or operational permission.

## Repository decision

| Question | Repository-specific answer |
| --- | --- |
| Architectural role | specialized graph tool |
| Minimum useful mathematics | Labeled graph theory and cycle-space rank |
| Relationships to preserve | Explicit atoms, undirected adjacency, integer bond labels and local neighborhoods |
| Concrete operation / capstone | Trace explicit water, a triangle and a double-bond pair; distinguish edge count from bond-order sum |
| Necessity and scope boundary | No implicit hydrogen, charge, aromaticity, stereochemistry, canonical isomorphism or chemical feasibility is inferred |

The decision is a source-based recommendation, not measured proof that a new specialty improves this repository. Start with the existing implementation and compare any proposed abstraction against a simpler alternative.

## Six-criterion compatibility scorecard

Complete one scorecard per proposed candidate and per concrete operation. Leave unmeasured entries unknown. Scores are human judgments from 0 (no fit) to 5 (strong evidenced fit); unknown is not zero. Do not sum an incomplete card. A total out of 30 is a heuristic, not adoption approval, and feasibility or necessity can veto a high total.

| Criterion | Score | Required evidence |
| --- | --- | --- |
| Structural compatibility | Not yet scored | Map the repository objects and the relationships above without losing direction, labels, units or missingness. |
| Transformation support | Not yet scored | Demonstrate the capstone operation on accepted and rejected inputs. |
| Invariant preservation | Not yet scored | State the property preserved and supply a counterexample or perturbation. |
| Computational feasibility | Not yet scored | Measure size, time and memory on bounded fixtures; record limits. |
| Integration compatibility | Not yet scored | Verify existing schemas, APIs and neighboring contracts remain compatible. |
| Mathematical necessity | Not yet scored | Compare with labeled graph theory and cycle-space rank and explain the additional capability, if any. |

## Curriculum

Prerequisites: basic programming, sets, functions and graph vocabulary. Work in six competency-gated sessions, approximately 60–90 minutes each; empirical evaluation is a separate research activity.

| Session | Learning objective | Exercise | Completion evidence |
| --- | --- | --- | --- |
| 1. Model | Identify explicit atoms, undirected adjacency, integer bond labels and local neighborhoods. | Draw a minimal valid example and one excluded relationship. | Annotated object/relation inventory with explicit assumptions. |
| 2. Contract | Distinguish schema validity from substantive correctness. | Trace validation and propose malformed, missing and boundary inputs. | Input-to-rejection table grounded in current source. |
| 3. Operation | Explain labeled graph theory and cycle-space rank. | Trace explicit water, a triangle and a double-bond pair; distinguish edge count from bond-order sum. | Hand trace compared with existing software, or a clearly labeled specification when no runtime exists. |
| 4. Preservation | State what a transformation must preserve. | Rename identifiers, reorder records, then alter one meaningful relation; predict each effect under the actual contract. | Separate invariant, expected change and unsupported transformation. |
| 5. Comparison | Justify mathematical necessity and cost. | Complete the six-criterion card for the existing approach and one proposed alternative; record unknowns honestly. | Evidence-backed recommendation with baseline and explicit veto conditions. |
| 6. Reproduction | Communicate the bounded result. | Reproduce the capstone using existing offline fixtures and record software version, inputs, outputs and limitations. | Reviewable notebook or report distinguishing computation, replay, independent evaluation and authorization. |

## Source-linked reading laboratory

Every nonblank line of the original analyzer is covered below. Line numbers refer to the inspected source blob `d949be3a3a0e78fe78070d45d6207f2148a173b8` in [molecular_topology/analysis.py](../../molecular_topology/analysis.py). Recheck anchors after source changes.

| Line | Statement | Learning check |
| --- | --- | --- |
| [1](../../molecular_topology/analysis.py#L1) | `"""Explicit neutral molecular graphs: connectivity, cycle rank and local descriptors."""` | Explain the stated scope and identify a claim the implementation does not establish. |
| [2](../../molecular_topology/analysis.py#L2) | `from collections import Counter` | Identify the dependency and explain which operation needs it. |
| [4](../../molecular_topology/analysis.py#L4) | `VALENCE={'H':1,'B':3,'C':4,'N':3,'O':2,'F':1,'P':5,'S':6,'Cl':1,'Br':1,'I':1}` | Explain the declared convention or bound and why it is not an empirical fact. |
| [7](../../molecular_topology/analysis.py#L7) | `def analyze(data):` | State the input/output contract and trace one normal and one failing case. |
| [8](../../molecular_topology/analysis.py#L8) | `if not isinstance(data,dict) or set(data)!={'schema_version','atoms','bonds'} or type(data['schema_version']) is not int or data['schema_version']!=1:raise ValueError('exact schema_version 1, atoms, bonds required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [9](../../molecular_topology/analysis.py#L9) | `atoms,bonds=data['atoms'],data['bonds']` | Explain the statement, track its state change and predict its effect on the worked example. |
| [10](../../molecular_topology/analysis.py#L10) | `if not isinstance(atoms,list) or not 1<=len(atoms)<=64:raise ValueError('require 1..64 explicit atoms')` | Construct the triggering input and explain why rejection preserves the contract. |
| [11](../../molecular_topology/analysis.py#L11) | `elements={}` | Explain the statement, track its state change and predict its effect on the worked example. |
| [12](../../molecular_topology/analysis.py#L12) | `for atom in atoms:` | State the loop invariant, termination argument and one boundary case. |
| [13](../../molecular_topology/analysis.py#L13) | `if not isinstance(atom,dict) or set(atom)!={'id','element'} or not isinstance(atom['id'],str) or not 1<=len(atom['id'])<=32 or not isinstance(atom['element'],str) or atom['element'] not in VALENCE:raise ValueError('supported explicit atom record required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [14](../../molecular_topology/analysis.py#L14) | `if atom['id'] in elements:raise ValueError('duplicate atom')` | Construct the triggering input and explain why rejection preserves the contract. |
| [15](../../molecular_topology/analysis.py#L15) | `elements[atom['id']]=atom['element']` | Explain the statement, track its state change and predict its effect on the worked example. |
| [16](../../molecular_topology/analysis.py#L16) | `if not isinstance(bonds,list) or len(bonds)>128:raise ValueError('at most 128 bonds')` | Construct the triggering input and explain why rejection preserves the contract. |
| [17](../../molecular_topology/analysis.py#L17) | `neighbors={n:{} for n in elements};seen=set()` | Draw the represented relation; identify direction, multiplicity and edge labels. |
| [18](../../molecular_topology/analysis.py#L18) | `for bond in bonds:` | State the loop invariant, termination argument and one boundary case. |
| [19](../../molecular_topology/analysis.py#L19) | `if not isinstance(bond,dict) or set(bond)!={'source','target','order'}:raise ValueError('exact bond fields required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [20](../../molecular_topology/analysis.py#L20) | `a,b,order=bond['source'],bond['target'],bond['order']` | Explain the statement, track its state change and predict its effect on the worked example. |
| [21](../../molecular_topology/analysis.py#L21) | `if not isinstance(a,str) or not isinstance(b,str) or a not in elements or b not in elements or a==b or type(order) is not int or order not in (1,2,3):raise ValueError('supported endpoints and integer bond order 1..3 required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [22](../../molecular_topology/analysis.py#L22) | `key=tuple(sorted((a,b)))` | Explain the statement, track its state change and predict its effect on the worked example. |
| [23](../../molecular_topology/analysis.py#L23) | `if key in seen:raise ValueError('parallel/duplicate bond')` | Construct the triggering input and explain why rejection preserves the contract. |
| [24](../../molecular_topology/analysis.py#L24) | `seen.add(key);neighbors[a][b]=order;neighbors[b][a]=order` | Draw the represented relation; identify direction, multiplicity and edge labels. |
| [25](../../molecular_topology/analysis.py#L25) | `unseen=set(elements);parts=[];distance_sum=0` | Trace component bookkeeping on a disconnected example. |
| [26](../../molecular_topology/analysis.py#L26) | `for source in sorted(elements):` | State the loop invariant, termination argument and one boundary case. |
| [27](../../molecular_topology/analysis.py#L27) | `distances={source:0};queue=[source]` | Trace discovery order and state the reachability or shortest-path invariant. |
| [28](../../molecular_topology/analysis.py#L28) | `for node in queue:` | Trace discovery order and state the reachability or shortest-path invariant. |
| [29](../../molecular_topology/analysis.py#L29) | `for target in sorted(neighbors[node]):` | Draw the represented relation; identify direction, multiplicity and edge labels. |
| [30](../../molecular_topology/analysis.py#L30) | `if target not in distances:distances[target]=distances[node]+1;queue.append(target)` | Trace discovery order and state the reachability or shortest-path invariant. |
| [31](../../molecular_topology/analysis.py#L31) | `distance_sum+=sum(distances.values())` | Trace discovery order and state the reachability or shortest-path invariant. |
| [32](../../molecular_topology/analysis.py#L32) | `if source in unseen:` | Trace component bookkeeping on a disconnected example. |
| [33](../../molecular_topology/analysis.py#L33) | `part=sorted(distances);parts.append(part);unseen-=set(part)` | Trace discovery order and state the reachability or shortest-path invariant. |
| [34](../../molecular_topology/analysis.py#L34) | `counts=Counter(elements.values())` | Derive the explicit inventory and ordering; identify information never inferred. |
| [35](../../molecular_topology/analysis.py#L35) | `element_order=(['C','H']+sorted(set(counts)-{'C','H'})) if 'C' in counts else sorted(counts)` | Derive the explicit inventory and ordering; identify information never inferred. |
| [36](../../molecular_topology/analysis.py#L36) | `formula=''.join(e+(str(counts[e]) if counts[e]>1 else '') for e in element_order if counts[e])` | Derive the explicit inventory and ordering; identify information never inferred. |
| [37](../../molecular_topology/analysis.py#L37) | `gaps=[n for n in sorted(elements) if sum(neighbors[n].values())>VALENCE[elements[n]]]` | Explain the declared convention or bound and why it is not an empirical fact. |
| [38](../../molecular_topology/analysis.py#L38) | `descriptors=Counter(elements[n]+'\|'+','.join(sorted(elements[t]+':'+str(o) for t,o in neighbors[n].items())) for n in elements)` | Draw the represented relation; identify direction, multiplicity and edge labels. |
| [39](../../molecular_topology/analysis.py#L39) | `return {'schema_version':1,'domain':'chemistry','status':'FAIL' if gaps else 'PASS','explicit_atom_formula':formula,` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [40](../../molecular_topology/analysis.py#L40) | `'atom_count':len(elements),'bond_count':len(bonds),'components':parts,` | Trace component bookkeeping on a disconnected example. |
| [41](../../molecular_topology/analysis.py#L41) | `'cycle_rank':len(bonds)-len(elements)+len(parts),'within_component_wiener_sum':distance_sum//2,` | Trace component bookkeeping on a disconnected example. |
| [42](../../molecular_topology/analysis.py#L42) | `'valence_upper_bound_violations':gaps,'local_descriptor_counts':dict(sorted(descriptors.items())),` | Derive the neighborhood multiset and give a limitation of this representation. |
| [43](../../molecular_topology/analysis.py#L43) | `'execution_authorized':False,'clinical_use_authorized':False,` | Explain the statement, track its state change and predict its effect on the worked example. |
| [44](../../molecular_topology/analysis.py#L44) | `'scope':'Explicit atoms and integer bonds only; no implicit hydrogens, aromaticity, charges, stereochemistry, canonical isomorphism, energies, chemical feasibility, synthesis or therapeutic inference. Valence checks are declared upper bounds, not chemical validation.'}` | Explain the statement, track its state change and predict its effect on the worked example. |
## Assessment and verification

A learner must explain the model, trace the capstone, identify a counterexample and state the scope boundary. Assess these four competencies equally; a numerical score cannot compensate for an unsupported scientific or operational claim.

Relevant existing checks:

- [tests/test_combined_adapter.py](../../tests/test_combined_adapter.py)
- [tests/test_domain.py](../../tests/test_domain.py)
- [tests/test_moltop.py](../../tests/test_moltop.py)

Follow [README](../../README.md) for environment and installed-package instructions. Read scripts before execution; source-reading exercises do not authorize provider calls, model downloads, live orders, hardware actions or messages. Synthetic fixtures establish software behavior only. This documentation change does not report those exercises as already executed.

## Interoperability and adoption gate

Retain explicit domain contracts. Shared assurance records should refer to domain evidence and its assumptions rather than relabeling graph reachability, homology, statistical calibration and epistemic acceptance as interchangeable quantities. The canonical ResearchOs controller remains owned by ResearchOs; this curriculum does not create another controller fork.

Adopt additional mathematics only after a versioned experiment demonstrates a useful operation, the scorecard has evidence, the simpler baseline is inadequate and existing conformance checks remain satisfied. No implicit hydrogen, charge, aromaticity, stereochemistry, canonical isomorphism or chemical feasibility is inferred.
