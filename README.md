# spaCy Server

[![Built with spaCy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)

This project provides industrial-strength NLP via [spaCy](https://spacy.io/) and [sense2vec](https://github.com/explosion/sense2vec) over a containerized HTTP API.

## Installation

### Server

Install [Docker](https://hub.docker.com/search/?type=edition&offering=community).

### Generating an SDK

You can generate a wrapper for the HTTP API using [OpenAPI Generator](https://openapi-generator.tech/) on the file [`https://raw.githubusercontent.com/neelkamath/spacy-server/master/docs/spec/openapi.yaml`](https://raw.githubusercontent.com/neelkamath/spacy-server/master/docs/openapi.yaml).

## [Usage](https://hub.docker.com/r/neelkamath/spacy-server)

## [Contributing](docs/CONTRIBUTING.md)

## License

This project is under the [MIT License](LICENSE).
