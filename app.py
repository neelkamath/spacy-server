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
            response['data'].append({'sentence': str(sent),
                                     'entities': entities})
    return response


def build_entity(ent):
    return {'entity': str(ent),
            'type': ent.label_,
            'offset': {'start': ent.start_char, 'end': ent.end_char}}
