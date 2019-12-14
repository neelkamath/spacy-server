# spaCy Server

[![Built with spaCy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)

This project provides industrial-strength NLP for multiple languages via [spaCy](https://spacy.io/) and [sense2vec](https://github.com/explosion/sense2vec) over a containerized HTTP API.

## Installation

### Server

Install [Docker](https://hub.docker.com/search/?type=edition&offering=community).

You can find specific tags (say for example, a French model) on the [Docker Hub repository](https://hub.docker.com/repository/docker/neelkamath/spacy-server/tags?page=1).

For example, to run an English model at `http://localhost:8000`, run:
```
docker run --rm -e SPACY_MODEL=en_core_web_sm -p 8000:8000 neelkamath/spacy-server:v1-en_core_web_sm
```

### Generating an SDK

You can generate a wrapper for the HTTP API using [OpenAPI Generator](https://openapi-generator.tech/) on the file [`https://raw.githubusercontent.com/neelkamath/spacy-server/master/docs/openapi.yaml`](https://raw.githubusercontent.com/neelkamath/spacy-server/master/docs/openapi.yaml).

## [Usage](https://neelkamath.gitlab.io/spacy-server/)

## [Contributing](docs/CONTRIBUTING.md)

## License

This project is under the [MIT License](LICENSE).
