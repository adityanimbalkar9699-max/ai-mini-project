import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)

    def test_knowledge_base(self):
        response = self.app.get('/api/knowledge-base')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("rules", data)
        self.assertGreaterEqual(len(data["rules"]), 12)

    def test_forward_chain_api(self):
        response = self.app.post('/api/forward-chain', json={"symptoms": ["fever", "cough", "fatigue", "shortness_of_breath"]})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data["results"]), 0)
        self.assertEqual(data["results"][0]["diagnosis"], "Common Pneumonia")

    def test_backward_chain_api(self):
        response = self.app.post('/api/backward-chain', json={"target": "Common Pneumonia", "symptoms": ["fever", "cough", "fatigue", "shortness_of_breath"]})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertTrue(data["result"]["matched"])

    def test_api_test_suite(self):
        response = self.app.post('/api/test')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("test_results", data)

if __name__ == '__main__':
    unittest.main()
