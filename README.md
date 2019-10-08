# spaCy NER Server

[![Built with spaCy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)

For developers who need named entity recognition, the spaCy NER Server is an HTTP API that provides industrial-strength natural language processing. Unlike other servers, our product is fast, easy to use, and well documented.

## Installation

You can try out the HTTP API using the development server `https://spacy-ner-server.herokuapp.com`. However, this server may be offline or serving a different API in the future. Hence, it's highly recommended to run your own instance.

### Running Your Own Instance

Install [Docker](https://hub.docker.com/search/?type=edition&offering=community).

To serve at `http://localhost:8080`, run `docker run --rm -p 8080:8080 neelkamath/spacy-ner-server`. 

You can change the port by setting the `PORT` environment variable (e.g., `docker run --rm -e PORT=6969 -p 6969:6969 neelkamath/spacy-ner-server`).

To run a particular version, run `docker run --rm -p 8080:8080 neelkamath/spacy-ner-server:<TAG>`, where `<TAG>` is from `https://hub.docker.com/r/neelkamath/spacy-ner-server/tags`.

The container `EXPOSE`s port `8080`.

### Generating an SDK

You can generate an API wrapper to use the HTTP API using these steps.

1. Install [node.js](https://nodejs.org/en/download/).
1. `npm i -g @openapitools/openapi-generator-cli`.
1. Run `openapi-generator list`.

    This will output something like:
    ```
    CLIENT generators:
        - ada
        - android
        ...
        - javascript
        ...
    SERVER generators:
        - ada-server
        - aspnetcore
        ...
    ```
    Pick one of these (e.g., `javascript`).
1. Run `openapi-generator generate -g <TARGET> -o <DIRECTORY> -i https://raw.githubusercontent.com/neelkamath/spacy-ner-server/master/docs/openapi.yaml`, where `<TARGET>` is what you picked, and `<DIRECTORY>` is the directory to output the generated SDK to. A documented and ready-to-use wrapper will now be available at `<DIRECTORY>`.

For advanced use cases, please see the [OpenAPI Generator documentation](https://openapi-generator.tech/).

## [Usage](https://neelkamath.gitlab.io/spacy-ner-server/)

## [Contributing](docs/CONTRIBUTING.md)

## License

This project is under the [MIT License](LICENSE).