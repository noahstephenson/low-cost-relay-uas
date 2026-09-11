"""Catch stale implicit nodes in the generated reference atlas."""
import importlib.util
from pathlib import Path
import re
import unittest

spec = importlib.util.spec_from_file_location("atlas", Path(__file__).resolve().parents[1] / "scripts/generate-mermaid-views.py")
atlas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(atlas)

class DiagramViewTests(unittest.TestCase):
    def test_flow_edges_resolve_to_explicit_nodes(self):
        for title, diagram in atlas.extract_diagrams(atlas.render(atlas.load_catalogs())):
            if "flowchart " not in diagram:
                continue
            declared = set(re.findall(r'(\w+)\["', diagram))
            for line in diagram.splitlines():
                edge = re.match(r'\s*(\w+)\s+(?:-->|-\.->|<-->|---)(?:\|"[^"\n]*"\|)?\s*(\w+)', line)
                if edge:
                    for endpoint in edge.groups():
                        self.assertIn(endpoint, declared, (title, endpoint))

    def test_trace_preserves_requirement_to_verification_connections(self):
        text = atlas.render(atlas.load_catalogs())
        self.assertNotIn("REQ_FUN_001", text)
        self.assertRegex(text, r'REQ_001 -->\|"model analysis"\| VER_001')
        self.assertRegex(text, r'REQ_001 -\.->\|"external conformance"\| VER_009')

if __name__ == "__main__":
    unittest.main()
