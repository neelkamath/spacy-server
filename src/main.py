"""Provides NLP via spaCy and sense2vec over an HTTP API."""

import os
import typing

import fastapi
import pydantic
import sense2vec
import spacy
import starlette.responses
import starlette.status

from dataclasses import dataclass

app: fastapi.FastAPI = fastapi.FastAPI()
model: str = os.getenv('SPACY_MODEL')
pipeline_error: str = f"The model ({model}) doesn't support " + '{}.'
nlp: spacy = spacy.load(model)
if os.getenv('SENSE2VEC') == '1':
    nlp.add_pipe(
        sense2vec.Sense2VecComponent(nlp.vocab).from_disk('src/s2v_old')
    )


def enforce_components(components: typing.List[str], message: str) -> None:
    """Throws the <message> if the model doesn't have the <components>."""
    for component in components:
        if not nlp.has_pipe(component):
            raise fastapi.HTTPException(
                status_code=400,
                detail=pipeline_error.format(message)
            )


class NERRequest(pydantic.BaseModel):
    sections: typing.List[str]
    sense2vec: bool = False


@dataclass
class BuiltEntity:
    text: str
    label: str
    start_char: int
    end_char: int
    lemma: str
    start: int
    end: int
    text_with_ws: str
    sense2vec: typing.List[str]


@dataclass
class SentenceWithEntities:
    text: str
    entities: typing.List[BuiltEntity]


@dataclass
class NERResponse:
    data: typing.List[SentenceWithEntities]


@app.post('/ner')
async def recognize_named_entities(request: NERRequest) -> NERResponse:
    enforce_components(['ner', 'parser'], 'named entity recognition')
    if request.sense2vec:
        enforce_components(
            ['sense2vec'],
            'There is no sense2vec model bundled with this service.'
        )
    response: NERResponse = NERResponse([])
    for doc in nlp.pipe(request.sections, disable=['tagger']):
        for sent in doc.sents:
            entities: typing.List[BuiltEntity] = [
                build_entity(ent, request.sense2vec) for ent in sent.ents
            ]
            data: SentenceWithEntities = SentenceWithEntities(
                text=sent.text,
                entities=entities
            )
            response.data.append(data)
    return response


class SimilarPhrase(pydantic.BaseModel):
    """Similar phrases computed by sense2vec."""

    """The similar phrase."""
    phrase: str
    """The phrase's similarity in the range of 0-1."""
    similarity: float


def compute_phrases(ent) -> typing.List[SimilarPhrase]:
    """Computes similar phrases for the entity (<ent>).

    The entity must have already been processed by the ner, parser, and
    sense2vec pipeline components.
    """
    similar: typing.List[SimilarPhrase] = []
    if ent._.in_s2v:
        for data in ent._.s2v_most_similar():
            similar.append(
                SimilarPhrase(phrase=data[0][0], similarity=float(data[1]))
            )
    return similar


def build_entity(ent: spacy, use_sense2vec: bool) -> BuiltEntity:
    return BuiltEntity(
        text=ent.text,
        label=ent.label_,
        start_char=ent.start_char,
        end_char=ent.end_char,
        lemma=ent.lemma_,
        start=ent.start,
        end=ent.end,
        text_with_ws=ent.text_with_ws,
        sense2vec=compute_phrases(ent) if use_sense2vec else [],
    )


class PhraseInSentence(pydantic.BaseModel):
    """A <phrase> in a <sentence>."""

    sentence: str
    phrase: str

    @pydantic.root_validator
    def phrase_must_be_in_sentence(cls, values):
        if values.get('phrase') not in values.get('sentence'):
            raise ValueError('phrase must be in sentence')
        return values


@dataclass
class Sense2vecResponse:
    sense2vec: typing.List[SimilarPhrase]


@app.post('/sense2vec')
async def sense2vec(request: PhraseInSentence) -> Sense2vecResponse:
    enforce_components(['ner', 'parser', 'sense2vec'], 'sense2vec')
    doc: nlp = nlp(request.sentence, disable=['tagger'])
    phrases: typing.List[SimilarPhrase] = []
    for ent in list(doc.sents)[0].ents:
        if ent.text == request.phrase:
            phrases: typing.List[SimilarPhrase] = compute_phrases(ent)
    return Sense2vecResponse(phrases)


class TextModel(pydantic.BaseModel):
    text: str


@dataclass
class Token:
    text: str
    text_with_ws: str
    whitespace: str
    head: str
    head_index: int
    left_edge: str
    right_edge: str
    index: int
    ent_type: str
    ent_iob: str
    lemma: str
    normalized: str
    shape: str
    prefix: str
    suffix: str
    is_alpha: bool
    is_ascii: bool
    is_digit: bool
    is_title: bool
    is_punct: bool
    is_left_punct: bool
    is_right_punct: bool
    is_space: bool
    is_bracket: bool
    is_quote: bool
    is_currency: bool
    like_url: bool
    like_num: bool
    like_email: bool
    is_oov: bool
    is_stop: bool
    pos: str
    tag: str
    dep: str
    lang: str
    prob: int
    char_offset: int


@dataclass
class TaggedText:
    text: str
    tags: typing.List[Token]


@dataclass
class POSResponse:
    data: typing.List[TaggedText]


@dataclass
class TokenWithSentence:
    token: Token
    sent: str


@app.post('/pos')
async def tag_parts_of_speech(request: TextModel) -> POSResponse:
    enforce_components(['ner', 'parser', 'tagger'], 'part-of-speech tagging')
    data: typing.List[TaggedText] = []
    doc: nlp = nlp(request.text, disable=['sense2vec'])
    for token_with_sent in [build_token_with_sent(token) for token in doc]:
        if token_with_sent.sent in [obj.text for obj in data]:
            for obj in data:
                if obj.text == token_with_sent.sent:
                    obj.tags.append(token_with_sent.token)
                    break
        else:
            data.append(
                TaggedText(token_with_sent.sent, [token_with_sent.token])
            )
    return POSResponse(data)


def build_token_with_sent(token) -> TokenWithSentence:
    return TokenWithSentence(
        sent=token.sent.text,
        token=Token(
            text=token.text,
            text_with_ws=token.text_with_ws,
            whitespace=token.whitespace_,
            head=token.head.text,
            head_index=token.head.i,
            left_edge=token.left_edge.text,
            right_edge=token.right_edge.text,
            index=token.i,
            ent_type=token.ent_type_,
            ent_iob=token.ent_iob_,
            lemma=token.lemma_,
            normalized=token.norm_,
            shape=token.shape_,
            prefix=token.prefix_,
            suffix=token.suffix_,
            is_alpha=token.is_alpha,
            is_ascii=token.is_ascii,
            is_digit=token.is_digit,
            is_title=token.is_title,
            is_punct=token.is_punct,
            is_left_punct=token.is_left_punct,
            is_right_punct=token.is_right_punct,
            is_space=token.is_space,
            is_bracket=token.is_bracket,
            is_quote=token.is_quote,
            is_currency=token.is_currency,
            like_url=token.like_url,
            like_num=token.like_num,
            like_email=token.like_email,
            is_oov=token.is_oov,
            is_stop=token.is_stop,
            pos=token.pos_,
            tag=token.tag_,
            dep=token.dep_,
            lang=token.lang_,
            prob=token.prob,
            char_offset=token.idx,
        )
    )


@dataclass
class TokenizerResponse:
    tokens: typing.List[str]


@app.post('/tokenizer')
async def tokenize(request: TextModel) -> TokenizerResponse:
    doc: nlp = nlp(
        request.text,
        disable=['tagger', 'parser', 'ner', 'sense2vec']
    )
    return TokenizerResponse([token.text for token in doc])


@dataclass
class SentencizerResponse:
    sentences: typing.List[str]


@app.post('/sentencizer')
async def sentencize(request: TextModel) -> SentencizerResponse:
    enforce_components(['parser'], 'sentence segmentation')
    doc: nlp = nlp(request.text, disable=['tagger', 'ner', 'sense2vec'])
    return SentencizerResponse([sent.text for sent in doc.sents])


@app.get('/health_check')
async def check_health() -> starlette.responses.Response:
    return starlette.responses.Response(
        status_code=starlette.status.HTTP_204_NO_CONTENT
    )
