import json

import main
import starlette.testclient

client = starlette.testclient.TestClient(main.app)
ner_body = {
    'sections': [
        'Net income was $9.4 million compared to the prior year of $2.7 '
        + 'million. Google is a big company.',
        'Revenue exceeded twelve billion dollars, with a loss of $1b.'
    ]
}


def test_ner_sense2vec_enabled():
    response = client.post('/ner', json={**ner_body, 'sense2vec': True})
    assert response.status_code == 200
    with open('src/outputs/ner/sense2vec_enabled.json') as f:
        assert response.json() == json.load(f)


def test_ner_sense2vec_disabled():
    response = client.post('/ner', json=ner_body)
    with open('src/outputs/ner/sense2vec_disabled.json') as f:
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
