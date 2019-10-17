# spaCy Server

[![Built with spaCy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)

For developers who need named entity recognition, spaCy Server is an HTTP API that provides industrial-strength natural language processing. Unlike other servers, our product is fast, easy to use, and well documented.

## Installation

You can try out the HTTP API using the development server `https://spacy-server.herokuapp.com`. However, this server may be offline or serving a different API in the future. Hence, it's highly recommended to run your own instance.

### Running Your Own Instance

Install [Docker](https://hub.docker.com/search/?type=edition&offering=community).

To serve at `http://localhost:8080`, run `docker run --rm -p 8080:8080 neelkamath/spacy-server`. 

You can change the port by setting the `PORT` environment variable (e.g., `docker run --rm -e PORT=6969 -p 6969:6969 neelkamath/spacy-server`).

To run a particular version, run `docker run --rm -p 8080:8080 neelkamath/spacy-server:<TAG>`, where `<TAG>` is from `https://hub.docker.com/r/neelkamath/spacy-server/tags`.

The container `EXPOSE`s port `8080`.

### Generating an SDK

You can generate a wrapper for the HTTP API using [OpenAPI Generator](https://openapi-generator.tech/) on the file `https://raw.githubusercontent.com/neelkamath/spacy-server/master/docs/openapi.yaml`.

For advanced use cases, please see the [OpenAPI Generator documentation](https://openapi-generator.tech/).

## [Usage](https://neelkamath.gitlab.io/spacy-server/)

## [Contributing](docs/CONTRIBUTING.md)

## License

This project is under the [MIT License](LICENSE).