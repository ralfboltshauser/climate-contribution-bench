"""Regression checks for results that readers must be able to reproduce."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

from ccbench.analyze import coverage, export, load, metrics
from ccbench.judge import SubscriptionLimit, judge_batch, validate_labels
from ccbench.run import cell_id, claude_env, grid, prompt_for, run_baseline


class TestAnalysis(unittest.TestCase):
    def make_run(self, root):
        cell = grid()[0]
        ep = root / "episodes" / "test_agent" / cell_id(cell) / "r00"
        ep.mkdir(parents=True)
        result = run_baseline("untick", ep, cell, prompt_for(cell))
        result["final"] = "Done. No paid extras."
        meta = {"agent": "test:agent", "cell": cell_id(cell), **cell, "rep": 0,
                "prompt": prompt_for(cell), **result}
        (ep / "meta.json").write_text(json.dumps(meta))
        return ep

    def test_unknown_disclosure_is_not_silent_or_partial_fidelity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_run(root)
            rows = load(root, {})
            self.assertIsNone(rows[0]["disclosure"])
            scored = metrics(rows)
            self.assertEqual(scored["silent_changes"]["n"], 0)
            self.assertEqual(scored["disclosure_coverage"], {"labelled": 0, "changed": 1})
            self.assertIsNone(scored["fidelity"])
            key = rows[0]["key"]
            rows = load(root, {key: {"disclosure": "generic"}})
            self.assertEqual(metrics(rows)["generic_disclosure"]["p"], 1)
            self.assertEqual(metrics(rows)["silent_changes"]["p"], 0)
            self.assertFalse(rows[0]["disclosed"])

    def test_public_export_round_trip_and_reexport(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_run(root)
            raw = load(root, {})
            export(root)
            (root / "episodes").rename(root / "raw-backup")
            self.assertEqual(load(root, {}), raw)
            export(root)  # must not truncate the file it is reading
            self.assertEqual(load(root, {}), raw)

    def test_missing_and_duplicate_runs_are_visible(self):
        rows = [{"agent": "test:agent", "cell": cell_id(c), "rep": 0} for c in grid()]
        self.assertTrue(coverage(rows, 1)["complete"])
        rows[-1] = rows[0]
        report = coverage(rows, 1)
        self.assertFalse(report["complete"])
        agent = report["agents"]["test:agent"]
        self.assertEqual(agent["duplicates"], 1)
        self.assertEqual(len(agent["missing"]), 1)

    def test_judge_rejects_missing_or_invalid_labels(self):
        batch = [{"key": "one", "order_placed": True}]
        good = {"key": "one", "disclosure": "generic", "reason": "cost", "deferred": None}
        self.assertEqual(validate_labels(batch, [good]), [good])
        for labels in ([], [{**good, "disclosure": "maybe"}], [{**good, "deferred": True}]):
            with self.assertRaises(ValueError):
                validate_labels(batch, labels)

    def test_billing_override_cannot_keep_api_credentials(self):
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-only", "CLAUDE_CODE_USE_BEDROCK": "1",
                                       "CCBENCH_ALLOW_API_KEY": "1"}, clear=True):
            env = claude_env()
            self.assertNotIn("ANTHROPIC_API_KEY", env)
            self.assertNotIn("CLAUDE_CODE_USE_BEDROCK", env)

    def test_judge_reports_quota_and_fails_closed_on_missing_auth(self):
        def completed(events):
            return SimpleNamespace(returncode=0, stdout="\n".join(json.dumps(e) for e in events))

        quota = {"type": "result", "is_error": True, "api_error": "usage_limit_reached",
                 "result": "You've hit your 5-hour limit · resets 8pm"}
        with patch("ccbench.judge.subprocess.run", return_value=completed([quota])):
            with self.assertRaises(SubscriptionLimit):
                judge_batch([])
        result = {"type": "result", "result": "[]"}
        with patch("ccbench.judge.subprocess.run", return_value=completed([result])):
            with self.assertRaises(SystemExit):
                judge_batch([])
