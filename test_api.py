import unittest
import requests
import subprocess
import time

BASE_URL = "http://localhost:8000"

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(["python", "app.py"])
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def test_predict(self):
        response = requests.get(f"{BASE_URL}/predict")
        self.assertEqual(response.status_code, 200)
        self.assertIn("predictions", response.json())

    def test_train(self):
        response = requests.post(f"{BASE_URL}/train")
        self.assertEqual(response.status_code, 200)
        self.assertIn("retrained", response.json()["message"])

    def test_scoring(self):
        response = requests.get(f"{BASE_URL}/scoring")
        self.assertEqual(response.status_code, 200)
        self.assertIn("f1_score", response.json())

    def test_logs(self):
        response = requests.get(f"{BASE_URL}/logs")
        self.assertEqual(response.status_code, 200)
        self.assertIn("logs", response.json())

if __name__ == '__main__':
    unittest.main()