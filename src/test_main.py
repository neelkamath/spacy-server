import json

import fastapi
import main
import pytest
import starlette.testclient

client = starlette.testclient.TestClient(main.app)

ner_body = {
    'sections': [
        'Net income was $9.4 million compared to the prior year of $2.7 '
        + 'million. Google is a big company.',
        'Revenue exceeded twelve billion dollars, with a loss of $1b.'
    ]
}
ner_sense2vec_body = {**ner_body, 'sense2vec': True}


def test_ner_sense2vec_enabled():
    response = client.post('/ner', json=ner_sense2vec_body)
    assert response.status_code == 200
    with open('src/outputs/ner/sense2vec_enabled.json') as f:
        assert response.json() == json.load(f)


def test_ner_sense2vec_disabled():
    response = client.post('/ner', json=ner_body)
    with open('src/outputs/ner/sense2vec_disabled.json') as f:
        assert response.json() == json.load(f)


def test_ner_spacy_fail():
    fail('/ner', ner_body, 'ner')


def test_ner_sense2vec_fail():
    fail('/ner', ner_sense2vec_body, 'sense2vec')


def test_sense2vec_success():
    body = {
        'sentence': 'Bill Gates founded Microsoft in April 4, 1975.',
        'phrase': 'Bill Gates'
    }
    response = client.post('/sense2vec', json=body)
    assert response.status_code == 200
    with open('src/outputs/sense2vec.json') as f:
        assert response.json() == json.load(f)


def test_sense2vec_fail():
    response = client.post(
        '/sense2vec',
        json={'sentence': 'My name is John Doe.', 'phrase': 'Johnny Doe'}
    )
    assert response.status_code == 400
    assert response.json()['detail'] == 'phrase must be in sentence'


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


def test_enforce_components():
    with pytest.raises(fastapi.HTTPException):
        component = 'nonexistent_component'
        main.enforce_components([component], component)


def test_compute_phrases():
    sentence = 'Bill Gates founded Microsoft in April 4, 1975.'
    doc = main.nlp(sentence, disable=['tagger'])
    for ent in list(doc.sents)[0].ents:
        if ent.text == 'Bill Gates':
            with open('src/outputs/compute_phrases.json') as f:
                assert main.compute_phrases(ent) == json.load(f)
