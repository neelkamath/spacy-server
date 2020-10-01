import json
import re
from typing import List 

import pytest
from fastapi import HTTPException
from main import NERRequest, PhraseInSentence, TextModel, app, compute_phrases, enforce_components, nlp
from pydantic import BaseModel
from requests import Response
from starlette.testclient import TestClient

client: TestClient = TestClient(
    app
)

ner_sections: List[str] = [
    'Net income was $9.4 million compared to the prior year of $2.7 million. '
    + 'Google is a big company.',
    'Revenue exceeded twelve billion dollars, with a loss of $1b.'
]


def test_ner_sense2vec_enabled() -> None:
    response: Response = client.post(
        '/ner',
        json=dict(NERRequest(sections=ner_sections, sense2vec=True))
    )
    assert response.status_code == 200
    with open('src/outputs/ner/sense2vec_enabled.json') as f:
        assert response.json() == json.load(f)


def test_ner_sense2vec_disabled() -> None:
    response: Response = client.post(
        '/ner',
        json=dict(NERRequest(sections=ner_sections))
    )
    with open('src/outputs/ner/sense2vec_disabled.json') as f:
        assert response.json() == json.load(f)


def test_ner_spacy_fail() -> None:
    fail('/ner', NERRequest(sections=ner_sections), pipe='ner')


def test_ner_sense2vec_fail() -> None:
    fail(
        '/ner',
        NERRequest(sections=ner_sections, sense2vec=True),
        pipe='sense2vec'
    )


def test_sense2vec_success() -> None:
    body: PhraseInSentence = PhraseInSentence(
        sentence='Bill Gates founded Microsoft in April 4, 1975.',
        phrase='Bill Gates'
    )
    response: Response = client.post('/sense2vec', json=dict(body))
    assert response.status_code == 200
    with open('src/outputs/sense2vec.json') as f:
        assert response.json() == json.load(f)


pos_body: TextModel = TextModel(
    text='Apple is looking at buying U.K. startup for $1 billion'
)


def test_pos() -> None:
    response: Response = client.post('/pos', json=dict(pos_body))
    assert response.status_code == 200
    with open('src/outputs/pos.json') as f:
        assert response.json() == json.load(f)


def test_pos_fail() -> None:
    fail('/pos', pos_body, pipe='parser')


def test_tokenizer() -> None:
    text: TextModel = TextModel(
        text='Apple is looking at buying U.K. startup for $1 billion'
    )
    response: Response = client.post('/tokenizer', json=dict(text))
    assert response.status_code == 200
    with open('src/outputs/tokenizer.json') as f:
        assert response.json() == json.load(f)


sentencizer_body: TextModel = TextModel(
    text='Apple is looking at buying U.K. startup for $1 billion. Another '
         + 'sentence.'
)


def test_sentencizer() -> None:
    response: Response = client.post(
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


def fail(endpoint: str, body: BaseModel, pipe: str) -> None:
    with nlp.disable_pipes(pipe):
        response: Response = client.post(endpoint, json=dict(body))
        assert re.match(r'4\d\d', str(response.status_code))
        assert 'detail' in response.json()


def test_enforce_components() -> None:
    with pytest.raises(HTTPException):
        component: str = 'nonexistent_component'
        enforce_components([component], component)


def test_compute_phrases() -> None:
    sentence: str = 'Bill Gates founded Microsoft in April 4, 1975.'
    doc: nlp = nlp(sentence, disable=['tagger'])
    for ent in list(doc.sents)[0].ents:
        if ent.text == 'Bill Gates':
            with open('src/outputs/compute_phrases.json') as f:
                assert compute_phrases(ent) == json.load(f)
