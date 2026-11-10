"""Offline curriculum answer key. Synthetic checks, never operational approval."""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
for base in (ROOT, ROOT / "src", ROOT / "layer-b"):
    sys.path.insert(0, str(base))
CASES = []

def check(name, actual, expected):
    passed = actual == expected
    CASES.append({"case": name, "actual": actual, "expected": expected, "passed": passed})
    if not passed:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")

def rejects(name, call, error=ValueError):
    try:
        call()
    except error:
        check(name, error.__name__, error.__name__)
    else:
        raise AssertionError(f"{name}: expected {error.__name__}")




def run():
    from molecular_topology.analysis import analyze
    def model(elements, bonds):
        return {"schema_version": 1, "atoms": [{"id": str(i), "element": e} for i, e in enumerate(elements)],
                "bonds": [{"source": str(a), "target": str(b), "order": o} for a,b,o in bonds]}
    water = model(["O","H","H"], [(0,1,1),(0,2,1)])
    r = analyze(water)
    check("water formula", r["explicit_atom_formula"], "H2O")
    check("water pair distances: 1+1+2", r["within_component_wiener_sum"], 4)
    check("water local neighborhoods", r["local_descriptor_counts"], {"H|O:1": 2, "O|H:1,H:1": 1})
    check("triangle cycle space: 3-3+1", analyze(model(["C"]*3, [(0,1,1),(1,2,1),(2,0,1)]))["cycle_rank"], 1)
    check("double bond is one graph edge", analyze(model(["C","O"], [(0,1,2)]))["cycle_rank"], 0)
    check("isolated carbon gets no inferred hydrogen", analyze(model(["C"], []))["explicit_atom_formula"], "C")
    bad = model(["H","O"], [(0,1,2)])
    check("upper bound exceeded", analyze(bad)["valence_upper_bound_violations"], ["0"])
    bad = copy.deepcopy(water); bad["bonds"][0]["order"] = True
    rejects("boolean is not integer bond order", lambda: analyze(bad))
    bad = copy.deepcopy(water); bad["bonds"].append({"source":"1","target":"0","order":1})
    rejects("reversed duplicate rejected", lambda: analyze(bad))
    reordered = copy.deepcopy(water); reordered["atoms"].reverse(); reordered["bonds"].reverse()
    check("record ordering leaves report unchanged", analyze(reordered), r)
    ring = model(["C"]*6, [(i,(i+1)%6,1) for i in range(6)])
    two_rings = model(["C"]*6, [(0,1,1),(1,2,1),(2,0,1),(3,4,1),(4,5,1),(5,3,1)])
    one, two = analyze(ring), analyze(two_rings)
    check("same one-hop descriptors do not imply isomorphism", one["local_descriptor_counts"], two["local_descriptor_counts"])
    check("descriptor collision has different component counts", [len(one["components"]),len(two["components"])], [1,2])
    check("no execution authority", r["execution_authorized"], False)
    check("no clinical authority", r["clinical_use_authorized"], False)

if __name__ == "__main__":
    if sys.argv[1:] not in ([], ["--verify"]):
        raise SystemExit("Usage: python curriculum/lab.py [--verify]")
    run()
    report = {"schema_version": 1, "status": "PASS", "case_count": len(CASES),
              "cases": CASES, "scope": "Synthetic curriculum checks only"}
    if sys.argv[1:] == ["--verify"]:
        expected = json.loads((Path(__file__).parent / "expected.json").read_text())
        if report != expected:
            raise AssertionError("Observed answers differ from curriculum/expected.json")
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))
