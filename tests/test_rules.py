import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from inference import run_forward_chaining, run_backward_chaining
from knowledge.knowledge_base import kb

class TestRulesAndEdgeCases(unittest.TestCase):

    def setUp(self):
        self.rules = kb.get_all_rules()

    def test_empty_symptoms_forward(self):
        results = run_forward_chaining(self.rules, [])
        # Should return no full matches or empty/partial
        full_matches = [r for r in results if r["is_full_match"]]
        self.assertEqual(len(full_matches), 0)

    def test_unknown_disease_backward(self):
        res = run_backward_chaining(self.rules, "AlienVirusX", ["fever", "cough"])
        self.assertFalse(res["matched"])
        self.assertIn("AlienVirusX", res["missing_symptoms"])

    def test_multiple_possible_diagnoses(self):
        # Symptoms overlapping multiple rules (fever, headache, fatigue)
        symptoms = ["fever", "headache", "fatigue"]
        results = run_forward_chaining(self.rules, symptoms)
        # Should match Influenza (R02) partially or fully, and possibly others
        self.assertGreater(len(results), 0)

    def test_knowledge_base_loading(self):
        rules = kb.get_all_rules()
        self.assertGreaterEqual(len(rules), 12)
        symptoms = kb.get_all_symptoms()
        self.assertGreater(len(symptoms), 10)
        diseases = kb.get_all_diseases()
        self.assertGreaterEqual(len(diseases), 12)

if __name__ == '__main__':
    unittest.main()
