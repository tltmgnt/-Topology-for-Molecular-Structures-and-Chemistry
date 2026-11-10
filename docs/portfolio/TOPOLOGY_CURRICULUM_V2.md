# Topology compatibility and curriculum v2 — -Topology-for-Molecular-Structures-and-Chemistry

The verified edition of version 2 adapts the explicit-molecular-graph teaching pattern to this repository's actual role. This edition adds executable learning checks and reviewed answer keys. It does not introduce a new topology engine or grant operational permission.

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

## Worked reasoning and source explanation

Water's unordered pair distances are O–H1=1, O–H2=1 and H1–H2=2, totaling 4. The code traverses from every atom and counts each pair twice, so its accumulated 8 is divided by two. For a triangle, m−n+c=3−3+1=1; for C=O it is 1−2+1=0 because bond order is a label on one edge. The isolated-carbon example returns C, demonstrating that PASS is only an upper-bound check, not chemical completion. A six-cycle and two separate triangles both give six identical C|C:1,C:1 neighborhoods, yet their component counts are 1 and 2. Matching local descriptor counts therefore cannot prove isomorphism.

Read the [inspected source](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py) alongside the [executable answer key](../../curriculum/lab.py). The source link is pinned to the inspected revision; the lab and any explicitly described fix are in this change.

| Source line | Explanation |
| --- | --- |
| [1](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L1) | The module documents connectivity, cycle rank and neighborhoods. The word neutral is a domain intention; neutrality is not established from this schema. |
| [2](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L2) | Counter supplies frequency maps for elements and repeated neighborhood strings. |
| [4](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L4) | VALENCE declares only maximum incident bond-order sums. It does not require saturation, infer charge or validate chemistry. |
| [7](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L7) | analyze accepts one record and either returns a scoped report or raises ValueError for malformed input. |
| [8](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L8) | Short-circuit or protects dictionary accesses. Exact keys reject extras; type(version) is int rejects True even though bool subclasses int. |
| [9](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L9) | Read the now-present atoms and bonds fields; their collection types remain to be validated. |
| [10](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L10) | Require a list of 1–64 atoms, bounding later all-sources traversal cost. |
| [11](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L11) | Create the atom-ID→element lookup; unique IDs will become graph vertices. |
| [12](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L12) | Process each explicit atom record. |
| [13](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L13) | Require exact id/element keys, a 1–32-character string ID and a supported element string. Whitespace-only IDs are not explicitly forbidden here. |
| [14](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L14) | Reject reused IDs before insertion can overwrite a prior atom. |
| [15](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L15) | Store the element label under its atom ID; equal element labels are allowed. |
| [16](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L16) | Allow an empty bond list but reject a non-list or more than 128 records. |
| [17](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L17) | Allocate an empty adjacency dictionary for every atom, including isolated ones; seen tracks unordered edge pairs. |
| [18](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L18) | Process each submitted bond once. |
| [19](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L19) | Require exactly source, target and order; aromaticity, charge and other extra fields are rejected. |
| [20](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L20) | Extract the two endpoint IDs and edge-order label. |
| [21](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L21) | Require known distinct string endpoints and order exactly int in {1,2,3}. Self-loops, True and 1.0 are rejected. |
| [22](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L22) | Sorting endpoints and converting to a tuple gives both directions the same hashable undirected key. |
| [23](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L23) | Reject repeated pairs regardless of direction or order, so double bonds must be one record with order=2. |
| [24](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L24) | Record the pair and write symmetric adjacency entries carrying the same order. |
| [25](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L25) | Track components still unrecorded and initialize an ordered-pair distance accumulator. |
| [26](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L26) | Traverse from every sorted atom for deterministic all-sources distance calculation, even after its component is known. |
| [27](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L27) | Mark the source discovered at distance zero and initialize a list used as a growing queue. |
| [28](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L28) | Python's list iterator visits elements appended during iteration; discovery order is breadth-first in this pattern. |
| [29](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L29) | Sorted adjacent IDs make discovery order reproducible. Sorting is not necessary for shortest-distance correctness. |
| [30](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L30) | Discover each vertex once, assign parent distance plus one and enqueue it. Bond order is ignored for these hop distances. |
| [31](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L31) | Sum reachable distances from this source only; disconnected targets make no contribution. |
| [32](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L32) | Record a component only for a source not removed by a previous component traversal. |
| [33](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L33) | The reachable IDs form this component; sort them, append it and subtract it from unseen. |
| [34](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L34) | Count only explicitly submitted element labels across all components. |
| [35](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L35) | Use C,H,then alphabetical others when C exists; otherwise alphabetically order all present elements. |
| [36](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L36) | Concatenate element symbols, omit a count of one, and infer no hydrogens. |
| [37](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L37) | Return sorted IDs whose incident bond-order sum strictly exceeds the declared upper bound. Unsaturated atoms do not fail. |
| [38](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L38) | For each center, sort neighbor element:order tokens and count the resulting one-hop multiset descriptor. Atom IDs are omitted; this is not canonical isomorphism. |
| [39](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L39) | Return schema/domain metadata, PASS unless upper bounds fail, and the explicit formula. Input errors raised earlier do not return this FAIL status. |
| [40](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L40) | Report vertex count, submitted edge count and the sorted membership of each connected component. |
| [41](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L41) | Compute independent graph cycles as m−n+c; halve ordered-pair distance totals to count each reachable unordered pair once. |
| [42](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L42) | Expose violating IDs and lexically sorted descriptor counts so consumers can inspect both diagnostics. |
| [43](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L43) | Both authority fields are constant False metadata; actual permissions would need a separate enforcement layer. |
| [44](https://github.com/tltmgnt/-Topology-for-Molecular-Structures-and-Chemistry/blob/7b1e4ad99b01f2a1d2cd07267df3841cc2ddebfc/molecular_topology/analysis.py#L44) | State omitted chemical semantics and the upper-bound interpretation so structural output is not promoted to feasibility, synthesis or clinical inference. |

## Run the worked laboratory

From the repository root, with Python 3.12 (the recorded local version is 3.12.14):

```sh
python curriculum/lab.py --verify
```

The lab checks **14 explicit expectations** against existing repository functions. It prints a JSON case report and exits nonzero on a wrong result. `--verify` additionally compares the entire case report with [expected.json](../../curriculum/expected.json). Read the input and predict each result before opening the answer key. No API account, credentials, model download, trading action or equipment connection is needed.

| Checkpoint | Expected answer |
| --- | --- |
| water formula | `"H2O"` |
| water pair distances: 1+1+2 | `4` |
| water local neighborhoods | `{"H\|O:1": 2, "O\|H:1,H:1": 1}` |
| triangle cycle space: 3-3+1 | `1` |
| double bond is one graph edge | `0` |
| isolated carbon gets no inferred hydrogen | `"C"` |
| upper bound exceeded | `["0"]` |
| boolean is not integer bond order | `"ValueError"` |
| reversed duplicate rejected | `"ValueError"` |
| record ordering leaves report unchanged | `{"atom_count": 3, "bond_count": 2, "clinical_use_authorized": false, "components": [["0", "1", "2"]], "cycle_rank": 0, "domain": "chemistry", "execution_authorized": false, "explicit_atom_formula": "H2O", "local_descriptor_counts": {"H\|O:1": 2, "O\|H:1,H:1": 1}, "schema_version": 1, "scope": "Explicit atoms and integer bonds only; no implicit hydrogens, aromaticity, charges, stereochemistry, canonical isomorphism, energies, chemical feasibility, synthesis or therapeutic inference. Valence checks are declared upper bounds, not chemical validation.", "status": "PASS", "valence_upper_bound_violations": [], "within_component_wiener_sum": 4}` |
| same one-hop descriptors do not imply isomorphism | `{"C\|C:1,C:1": 6}` |
| descriptor collision has different component counts | `[1, 2]` |
| no execution authority | `false` |
| no clinical authority | `false` |

The comparisons above encode independently specified small examples and contract expectations; a passing answer key is not evidence of complete domain correctness. The original functions and their existing test suites remain the authority for broader supported contracts.

## Learner tasks and assessment rubric

1. Before running the lab, predict every expected answer and derive one numeric result or state transition by hand.
2. Explain the worked reasoning above using the referenced source, including the rejected or counterexample case.
3. Add a new valid example and a nearby failing example. Explain which assumption changes, then compare against the existing implementation. For concept/static labs, keep the result explicitly at that level.
4. Complete the scorecard for a proposed extension and a simpler baseline. Leave measurements unknown until collected; a task that the baseline already solves is not evidence for additional topology.

| Competency | Points | Full-credit evidence |
| --- | --- | --- |
| Model and contract | 0–3 | Correct objects, relation direction, labels/units, input bounds and missingness. |
| Derivation and trace | 0–3 | Hand derivation agrees with the specified fixture; source steps explain why. |
| Counterexample | 0–3 | New failing/boundary case has a justified expected result; rejection is not suppressed. |
| Scope and necessity | 0–3 | Distinguishes software behavior from validation and compares an explicit simpler alternative. |

Completion requires at least 10/12 and no zero in scope/necessity. A runnable answer key alone is not evidence that a learner achieved this competency. No learner-outcome study has been performed.

## Verification evidence and maintenance

[VALIDATION.json](../../curriculum/VALIDATION.json) records the inspected base revision, local Python version, source/fixture hashes, lab/answer hashes, case count and exit codes. All cases were executed locally. An in-memory copy with a deliberately wrong comparison was also executed and returned nonzero, checking that the grading failure path is active. Those injected failures are harness checks, not scientific adversarial evaluations.

The dedicated [curriculum workflow](../../.github/workflows/curriculum.yml) runs the same `--verify` command on relevant pull-request changes. CI status is reported by GitHub; the local record does not assert that remote CI passed. Existing full-suite and installed-package requirements still apply to runtime changes. When source or fixture semantics change, inspect the diff and rederive answers before updating expected.json. Never regenerate expected answers solely to silence a failure. Refresh the local validation record after an actual run; do not rewrite its recorded base revision as if a new run occurred.

## Interoperability and adoption gate

Retain explicit domain contracts. Shared assurance records should refer to domain evidence and its assumptions rather than relabeling graph reachability, homology, statistical calibration and epistemic acceptance as interchangeable quantities. The canonical ResearchOs controller remains owned by ResearchOs; this curriculum does not create another controller fork.

Adopt additional mathematics only after a versioned experiment demonstrates a useful operation, the scorecard has evidence, the simpler baseline is inadequate and existing conformance checks remain satisfied. No implicit hydrogen, charge, aromaticity, stereochemistry, canonical isomorphism or chemical feasibility is inferred.
