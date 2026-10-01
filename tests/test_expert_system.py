import unittest
import sys
import os

# Add AI_Mini_Project directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from inference import run_forward_chaining, run_backward_chaining
from knowledge.knowledge_base import kb

RULES = kb.get_all_rules()

class TestExpertSystem(unittest.TestCase):

    def test_forward_chaining_pneumonia(self):
        symptoms = ["fever", "cough", "fatigue", "shortness_of_breath"]
        results = run_forward_chaining(RULES, symptoms)
        self.assertGreater(len(results), 0)
        top_match = results[0]
        self.assertEqual(top_match["diagnosis"], "Common Pneumonia")
        self.assertTrue(top_match["is_full_match"])
        self.assertEqual(top_match["match_ratio"], 100.0)

    def test_forward_chaining_partial(self):
        symptoms = ["fever", "headache"]
        results = run_forward_chaining(RULES, symptoms)
        self.assertGreater(len(results), 0)
        match_found = any(r["match_count"] >= 2 for r in results)
        self.assertTrue(match_found)

    def test_backward_chaining_valid(self):
        target = "Common Pneumonia"
        symptoms = ["fever", "cough", "fatigue", "shortness_of_breath"]
        res = run_backward_chaining(RULES, target, symptoms)
        self.assertTrue(res["matched"])
        self.assertEqual(len(res["missing_symptoms"]), 0)

    def test_backward_chaining_missing_evidence(self):
        target = "Meningitis"
        symptoms = ["fever", "headache"] # missing stiff_neck, sensitivity_to_light
        res = run_backward_chaining(RULES, target, symptoms)
        self.assertFalse(res["matched"])
        self.assertIn("stiff_neck", res["missing_symptoms"])

    def test_unknown_disease(self):
        target = "NonExistentDisease"
        symptoms = ["fever"]
        res = run_backward_chaining(RULES, target, symptoms)
        # Should not find the disease
        self.assertFalse(res["matched"])

if __name__ == '__main__':
    unittest.main()
