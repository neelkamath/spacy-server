import json

import main
import starlette.testclient

client = starlette.testclient.TestClient(main.app)


def test_ner():
    body = {
        'sections': [
            'Net income was $9.4 million compared to the prior year of $2.7 '
            + 'million. Google is a big company.',
            'Revenue exceeded twelve billion dollars, with a loss of $1b.'
        ]
    }
    response = client.post('/ner', json=body)
    assert response.status_code == 200
    with open('src/outputs/ner.json') as f:
        assert response.json() == json.load(f)


def test_pos():
    text = {'text': 'Apple is looking at buying U.K. startup for $1 billion'}
    response = client.post('/pos', json=text)
    assert response.status_code == 200
    with open('src/outputs/pos.json') as f:
        assert response.json() == json.load(f)


def test_tokenizer():
    text = {'text': 'Apple is looking at buying U.K. startup for $1 billion'}
    response = client.post('/tokenizer', json=text)
    assert response.status_code == 200
    with open('src/outputs/tokenizer.json') as f:
        assert response.json() == json.load(f)


def test_sentencizer():
    body = {
        'text': 'Apple is looking at buying U.K. startup for $1 billion. '
                + 'Another sentence.'
    }
    response = client.post('/sentencizer', json=body)
    assert response.status_code == 200
    with open('src/outputs/sentencizer.json') as f:
        assert response.json() == json.load(f)


def test_health_check():
    assert client.get('/health_check').status_code == 204
