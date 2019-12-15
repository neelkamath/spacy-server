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


def test_ner_fail():
    fail('/ner', ner_body, 'ner')


pos_body = {'text': 'Apple is looking at buying U.K. startup for $1 billion'}


def test_pos():
    response = client.post('/pos', json=pos_body)
    assert response.status_code == 200
    with open('src/outputs/pos.json') as f:
        assert response.json() == json.load(f)


def test_pos_fail():
    fail('/pos', pos_body, 'parser')


def test_tokenizer():
    text = {'text': 'Apple is looking at buying U.K. startup for $1 billion'}
    response = client.post('/tokenizer', json=text)
    assert response.status_code == 200
    with open('src/outputs/tokenizer.json') as f:
        assert response.json() == json.load(f)


sentencizer_body = {
    'text': 'Apple is looking at buying U.K. startup for $1 billion. Another '
            + 'sentence.'
}


def test_sentencizer():
    response = client.post('/sentencizer', json=sentencizer_body)
    assert response.status_code == 200
    with open('src/outputs/sentencizer.json') as f:
        assert response.json() == json.load(f)


def test_sentencizer_fail():
    fail('/sentencizer', sentencizer_body, 'parser')


def test_health_check():
    assert client.get('/health_check').status_code == 204


def fail(endpoint, body, pipe):
    with main.nlp.disable_pipes(pipe):
        response = client.post(endpoint, json=body)
        assert response.status_code == 400
        assert 'detail' in response.json()
