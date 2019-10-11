import json
import unittest

import app


class TestServer(unittest.TestCase):

    def test_ner(self):
        with app.app.test_client() as client:
            body = {
                'sections': [
                    'Net income was $9.4 million compared to the prior year '
                    + 'of $2.7 million. Google is a big company.',
                    'Revenue exceeded twelve billion dollars, with a loss of '
                    + '$1b.'
                ]
            }
            response = client.post('/ner', json=body).get_json()
            with open('outputs/ner.json') as f:
                self.assertEqual(response, json.load(f))

    def test_pos(self):
        with app.app.test_client() as client:
            text = 'Apple is looking at buying U.K. startup for $1 billion'
            response = client.post('/pos', json={'text': text}).get_json()
            with open('outputs/pos.json') as f:
                self.assertEqual(response, json.load(f))

    def test_tokenizer(self):
        with app.app.test_client() as client:
            text = 'Apple is looking at buying U.K. startup for $1 billion'
            response = client.post('/tokenize', json={'text': text}).get_json()
            with open('outputs/tokenize.json') as f:
                self.assertEqual(response, json.load(f))

    def test_health_check(self):
        with app.app.test_client() as client:
            self.assertEqual(client.get('/health_check').status_code, 204)


if __name__ == '__main__':
    unittest.main()
