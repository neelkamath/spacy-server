"""Provides spaCy NLP over an HTTP API."""

import en_core_web_sm
import flask
from sense2vec import Sense2VecComponent

app = flask.Flask(__name__)
nlp = en_core_web_sm.load()
nlp.add_pipe(Sense2VecComponent(nlp.vocab).from_disk("s2v_old"))


@app.route('/ner', methods=['POST'])
def recognize_named_entities():
    response = {'data': []}
    sections = flask.request.get_json()['sections']
    for doc in nlp.pipe(sections, disable=['tagger']):
        for sent in doc.sents:
            entities = [build_entity(ent) for ent in sent.ents]
            data = {'text': sent.text, 'entities': entities}
            response['data'].append(data)
    return response


def build_entity(ent):
    similar = []
    if ent._.in_s2v:
        for data in ent._.s2v_most_similar():
            similar.append(
                {'phrase': data[0][0], 'similarity': float(data[1])}
            )
    return {
        'text': ent.text,
        'label': ent.label_,
        'start_char': ent.start_char,
        'end_char': ent.end_char,
        'lemma': ent.lemma_,
        'start': ent.start,
        'end': ent.end,
        'text_with_ws': ent.text_with_ws,
        'sense2vec': similar,
    }


@app.route('/pos', methods=['POST'])
def tag_parts_of_speech():
    data = []
    doc = nlp(flask.request.get_json()['text'])
    for token in [build_token(token) for token in doc]:
        text = token['sent']
        del token['sent']
        if text in [obj['text'] for obj in data]:
            for obj in data:
                if obj['text'] == text:
                    obj['tags'].append(token)
                    break
        else:
            data.append({'text': text, 'tags': [token]})
    return {'data': data}


def build_token(token):
    return {
        'sent': token.sent.text,
        'text': token.text,
        'text_with_ws': token.text_with_ws,
        'whitespace': token.whitespace_,
        'head': token.head.text,
        'left_edge': token.left_edge.text,
        'right_edge': token.right_edge.text,
        'index': token.i,
        'ent_type': token.ent_type_,
        'ent_iob': token.ent_iob_,
        'lemma': token.lemma_,
        'normalized': token.norm_,
        'shape': token.shape_,
        'prefix': token.prefix_,
        'suffix': token.suffix_,
        'is_alpha': token.is_alpha,
        'is_ascii': token.is_ascii,
        'is_digit': token.is_digit,
        'is_title': token.is_title,
        'is_punct': token.is_punct,
        'is_left_punct': token.is_left_punct,
        'is_right_punct': token.is_right_punct,
        'is_space': token.is_space,
        'is_bracket': token.is_bracket,
        'is_quote': token.is_quote,
        'is_currency': token.is_currency,
        'like_url': token.like_url,
        'like_num': token.like_num,
        'like_email': token.like_email,
        'is_oov': token.is_oov,
        'is_stop': token.is_stop,
        'pos': token.pos_,
        'tag': token.tag_,
        'dep': token.dep_,
        'lang': token.lang_,
        'prob': token.prob,
        'char_offset': token.idx,
    }


@app.route('/tokenizer', methods=['POST'])
def tokenize():
    text = flask.request.get_json()['text']
    doc = nlp(text, disable=['tagger', 'parser', 'ner'])
    return {'tokens': [token.text for token in doc]}


@app.route('/sentencizer', methods=['POST'])
def sentencize():
    text = flask.request.get_json()['text']
    doc = nlp(text, disable=['tagger', 'ner'])
    return {'sentences': [sent.text for sent in doc.sents]}


@app.route('/health_check')
def check_health():
    return flask.Response(status=204)
