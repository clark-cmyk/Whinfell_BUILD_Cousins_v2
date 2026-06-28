"""Tests for China Policy SQ3 scoring engine."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from china_policy_track.data_parser import parse_input
from china_policy_track.sq3 import (
    INTERPRETATION_BANDS,
    WEIGHT_GROWTH_MARKET,
    WEIGHT_POLICY_HIERARCHY,
    WEIGHT_STATE_CONTROL,
    calculate_sq3,
    interpret_sq3_band,
    normalize_state_control_impulse,
    score_input,
    score_observation,
)

VALID_BANDS = {label for _, _, label in INTERPRETATION_BANDS}


class TestSQ3Scoring(unittest.TestCase):
    def _load_perplexity_obs(self):
        text = (REPO_ROOT / "china_policy_track/examples/sample_perplexity_export.txt").read_text()
        return parse_input(text)

    def _load_koyfin_obs(self):
        raw = json.loads(
            (REPO_ROOT / "china_policy_track/examples/sample_koyfin_export.json").read_text()
        )
        return parse_input(raw)

    def test_weights_sum_to_one(self):
        total = WEIGHT_POLICY_HIERARCHY + WEIGHT_STATE_CONTROL + WEIGHT_GROWTH_MARKET
        self.assertAlmostEqual(total, 1.0)

    def test_state_control_normalization_endpoints(self):
        self.assertEqual(normalize_state_control_impulse(100), 0.0)
        self.assertEqual(normalize_state_control_impulse(0), 50.0)
        self.assertEqual(normalize_state_control_impulse(-100), 100.0)

    def test_calculate_sq3_returns_bounded_score_and_band(self):
        result = calculate_sq3(policy_strength=74, state_impulse_score=38, growth_impulse_score=61)
        self.assertGreaterEqual(result.sq3_score, 0)
        self.assertLessEqual(result.sq3_score, 100)
        self.assertIn(result.interpretation_band, VALID_BANDS)
        self.assertEqual(result.interpretation_band, interpret_sq3_band(result.sq3_score))

    def test_score_observation_perplexity_sample(self):
        obs = self._load_perplexity_obs()
        first = score_observation(obs)
        second = score_observation(obs)
        self.assertGreaterEqual(first.sq3_score, 0)
        self.assertLessEqual(first.sq3_score, 100)
        self.assertTrue(first.interpretation_band)
        self.assertIn(first.interpretation_band, VALID_BANDS)
        self.assertEqual(first.sq3_score, second.sq3_score)
        self.assertEqual(first.interpretation_band, second.interpretation_band)

    def test_score_observation_koyfin_sample(self):
        obs = self._load_koyfin_obs()
        first = score_observation(obs)
        second = score_observation(obs)
        self.assertGreaterEqual(first.sq3_score, 0)
        self.assertLessEqual(first.sq3_score, 100)
        self.assertTrue(first.interpretation_band)
        self.assertEqual(first.sq3_score, second.sq3_score)
        self.assertEqual(first.interpretation_band, second.interpretation_band)

    def test_score_input_end_to_end(self):
        text = (REPO_ROOT / "china_policy_track/examples/sample_perplexity_export.txt").read_text()
        raw = json.loads(
            (REPO_ROOT / "china_policy_track/examples/sample_koyfin_export.json").read_text()
        )
        for payload in (text, raw):
            a = score_input(payload)
            b = score_input(payload)
            d = a.to_dict()
            self.assertIn("sq3_score", d)
            self.assertIn("interpretation_band", d)
            self.assertGreaterEqual(d["sq3_score"], 0)
            self.assertLessEqual(d["sq3_score"], 100)
            self.assertTrue(d["interpretation_band"])
            self.assertEqual(a.sq3_score, b.sq3_score)
            self.assertEqual(a.interpretation_band, b.interpretation_band)

    def test_result_dict_includes_audit_components(self):
        obs = self._load_perplexity_obs()
        d = score_observation(obs).to_dict()
        self.assertAlmostEqual(
            d["weights"]["policy_hierarchy"] + d["weights"]["state_control"] + d["weights"]["growth_market"],
            1.0,
        )
        self.assertIn("components", d)
        self.assertIn("normalized_inputs", d)


if __name__ == "__main__":
    unittest.main()