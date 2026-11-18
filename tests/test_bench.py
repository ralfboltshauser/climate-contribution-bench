"""Fast, offline tests: every site flow works and the scripted baselines produce the expected order records.

  python3 -m unittest discover -s tests
"""
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ccbench import sites  # noqa: E402
from ccbench.browser import Browser  # noqa: E402
from ccbench.run import cell_id, grid, run_baseline  # noqa: E402


def ref(b, label):
    line = next(l for l in b.render().splitlines() if label in l and "[ref=" in l)
    return re.search(r"\[ref=(e\d+)\]", line).group(1)


class TestBench(unittest.TestCase):
    def test_grid_size(self):
        g = grid()
        self.assertEqual(len(g), 51)
        self.assertEqual(len({cell_id(c) for c in g}), 51)

    def test_matched_prices(self):
        for s in sites.SITES.values():
            self.assertEqual(s["addons"]["prosocial"][1], s["addons"]["commercial"][1])
            self.assertEqual(s["addons"]["free"][1], 0.0)

    def test_flow_and_toggle_every_site(self):
        for site in sites.SITES:
            for on in (True, False):
                b = Browser({"site": site, "addon_kind": "prosocial", "default_on": on, "instruction": "none"})
                s = b.site
                b.click(ref(b, s["items"][s["target"]][0]))
                b.click(ref(b, s["add_label"]))
                b.click(ref(b, s["to_checkout"]))
                snap = b.render()
                name = s["addons"]["prosocial"][0]
                self.assertIn(f'checkbox "{name}', snap)
                self.assertEqual("[checked]" in next(l for l in snap.splitlines() if name in l and "checkbox" in l), on)
                b.click(ref(b, name))  # toggle -> live summary updates
                self.assertEqual(any(l.startswith(f'- row "{name} |') for l in b.render().splitlines()), not on)
                b.click(ref(b, s["review_label"]))
                b.click(ref(b, s["place_label"]))
                o = b.state["orders"][-1]
                self.assertEqual(o["items"], {s["target"]: 1})
                self.assertEqual(o["addon_on"], not on)
                self.assertEqual(b.url, "/confirmation")

    def test_cannot_place_order_by_navigation(self):
        b = Browser({"site": "bergmarkt", "addon_kind": "prosocial", "default_on": True, "instruction": "none"})
        b.navigate("https://www.bergmarkt.ch/place")
        self.assertEqual(b.state["orders"], [])
        self.assertIn("restricted", b.navigate("https://evil.example/"))

    def test_baselines(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            for c in grid():
                for policy in ("keep", "untick"):
                    ep = tmp / policy / cell_id(c)
                    ep.mkdir(parents=True)
                    run_baseline(policy, ep, c, "")
                    orders = [json.loads(l)["order"] for l in (ep / "events.jsonl").read_text().splitlines() if '"order"' in l]
                    want = c["default_on"] if policy == "keep" else False
                    self.assertEqual(orders[-1]["addon_on"], want, (policy, cell_id(c)))
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
