"""Provides spaCy NLP over an HTTP API."""

import en_core_web_sm
import flask

app = flask.Flask(__name__)
nlp = en_core_web_sm.load()


@app.route('/health_check')
def check_health():
    return flask.Response(status=204)


@app.route('/', methods=['POST'])
def recognize_named_entities():
    response = {'data': []}
    sections = flask.request.get_json()['sections']
    for doc in nlp.pipe(sections, disable=['tagger']):
        for sent in doc.sents:
            entities = [build_entity(ent) for ent in sent.ents]
            data = {'sentence': sent.text, 'entities': entities}
            response['data'].append(data)
    return response


def build_entity(ent):
    return {
        'text': ent.text,
        'label': ent.label_,
        'start_char': ent.start_char,
        'end_char': ent.end_char,
        'lemma': ent.lemma_,
        'start': ent.start,
        'end': ent.end,
        'text_with_ws': ent.text_with_ws
    }
