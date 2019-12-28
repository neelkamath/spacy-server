import json
import re
import typing

import fastapi
import main
import pydantic
import pytest
import requests
import starlette.testclient

client: starlette.testclient.TestClient = starlette.testclient.TestClient(
    main.app
)

ner_sections: typing.List[str] = [
    'Net income was $9.4 million compared to the prior year of $2.7 million. '
    + 'Google is a big company.',
    'Revenue exceeded twelve billion dollars, with a loss of $1b.'
]


def test_ner_sense2vec_enabled() -> None:
    response: requests.Response = client.post(
        '/ner',
        json=dict(main.NERRequest(sections=ner_sections, sense2vec=True))
    )
    assert response.status_code == 200
    with open('src/outputs/ner/sense2vec_enabled.json') as f:
        assert response.json() == json.load(f)


def test_ner_sense2vec_disabled() -> None:
    response: requests.Response = client.post(
        '/ner',
        json=dict(main.NERRequest(sections=ner_sections))
    )
    with open('src/outputs/ner/sense2vec_disabled.json') as f:
        assert response.json() == json.load(f)


def test_ner_spacy_fail() -> None:
    fail('/ner', main.NERRequest(sections=ner_sections), pipe='ner')


def test_ner_sense2vec_fail() -> None:
    fail(
        '/ner',
        main.NERRequest(sections=ner_sections, sense2vec=True),
        pipe='sense2vec'
    )


def test_sense2vec_success() -> None:
    body: main.PhraseInSentence = main.PhraseInSentence(
        sentence='Bill Gates founded Microsoft in April 4, 1975.',
        phrase='Bill Gates'
    )
    response: requests.Response = client.post('/sense2vec', json=dict(body))
    assert response.status_code == 200
    with open('src/outputs/sense2vec.json') as f:
        assert response.json() == json.load(f)


pos_body: main.TextModel = main.TextModel(
    text='Apple is looking at buying U.K. startup for $1 billion'
)


def test_pos() -> None:
    response: requests.Response = client.post('/pos', json=dict(pos_body))
    assert response.status_code == 200
    with open('src/outputs/pos.json') as f:
        assert response.json() == json.load(f)


def test_pos_fail() -> None:
    fail('/pos', pos_body, pipe='parser')


def test_tokenizer() -> None:
    text: main.TextModel = main.TextModel(
        text='Apple is looking at buying U.K. startup for $1 billion'
    )
    response: requests.Response = client.post('/tokenizer', json=dict(text))
    assert response.status_code == 200
    with open('src/outputs/tokenizer.json') as f:
        assert response.json() == json.load(f)


sentencizer_body: main.TextModel = main.TextModel(
    text='Apple is looking at buying U.K. startup for $1 billion. Another '
         + 'sentence.'
)


def test_sentencizer() -> None:
    response: requests.Response = client.post(
        '/sentencizer',
        json=dict(sentencizer_body)
    )
    assert response.status_code == 200
    with open('src/outputs/sentencizer.json') as f:
        assert response.json() == json.load(f)


def test_sentencizer_fail() -> None:
    fail('/sentencizer', sentencizer_body, pipe='parser')


def test_health_check() -> None:
    assert client.get('/health_check').status_code == 204


def fail(endpoint: str, body: pydantic.BaseModel, pipe: str) -> None:
    with main.nlp.disable_pipes(pipe):
        response: requests.Response = client.post(endpoint, json=dict(body))
        assert re.match(r'4\d\d', str(response.status_code))
        assert 'detail' in response.json()


def test_enforce_components() -> None:
    with pytest.raises(fastapi.HTTPException):
        component: str = 'nonexistent_component'
        main.enforce_components([component], component)


def test_compute_phrases() -> None:
    sentence: str = 'Bill Gates founded Microsoft in April 4, 1975.'
    doc: main.nlp = main.nlp(sentence, disable=['tagger'])
    for ent in list(doc.sents)[0].ents:
        if ent.text == 'Bill Gates':
            with open('src/outputs/compute_phrases.json') as f:
                assert main.compute_phrases(ent) == json.load(f)
