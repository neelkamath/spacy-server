import json
import unittest

import app


class TestServer(unittest.TestCase):

    def test_ner(self):
        with app.app.test_client() as client:
            sections = [
                'Net income was $9.4 million compared to the prior year of '
                + '$2.7 million. Google is a big company.',
                'Revenue exceeded twelve billion dollars, with a loss of $1b.'
            ]
            actual = client.post('/ner', json={'sections': sections}).get_json()
            with open('outputs/ner.json') as f:
                expected = json.load(f)
            self.assertEqual(actual, expected)

    def test_pos(self):
        with app.app.test_client() as client:
            text = 'Apple is looking at buying U.K. startup for $1 billion'
            actual = client.post('/pos', json={'text': text}).get_json()
            with open('outputs/pos.json') as f:
                expected = json.load(f)
            self.assertEqual(actual, expected)

    def test_health_check(self):
        with app.app.test_client() as client:
            self.assertEqual(client.get('/health_check').status_code, 204)


if __name__ == '__main__':
    unittest.main()
