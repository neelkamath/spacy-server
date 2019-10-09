import json
import unittest

import app


class TestServer(unittest.TestCase):

    def test_health_check(self):
        with app.app.test_client() as client:
            self.assertEqual(client.get('/health_check').status_code, 204)

    def test_ner(self):
        with app.app.test_client() as client:
            sections = [
                'Net income was $9.4 million compared to the prior year of '
                + '$2.7 million. Google is a big company.',
                'Revenue exceeded twelve billion dollars, with a loss of $1b.'
            ]
            actual = client.post('/', json={'sections': sections}).get_json()
            with open('test.json') as f:
                expected = json.load(f)
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
