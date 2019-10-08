# Contributing

If you're forking the repo to develop the project as your own and not just to send back a PR, follow [these steps](fork.md).

## Installation

1. Install a version of [Python](https://www.python.org/downloads/) not less than 3.5, and less than 4.
1. If you are testing the Dockerfile or running the app in production, install [Docker](https://hub.docker.com/search/?type=edition&offering=community).
1. If you are generating documentation or testing the spec, install [node.js](https://nodejs.org/en/download/).
1. If you are generating documentation, run `npm i -g redoc-cli`.
1. If you are testing the spec, run `npm i -g @stoplight/spectral`.
1. Clone the repository using one of the following methods.
    - SSH: `git clone git@github.com:neelkamath/spacy-ner-server.git`
    - HTTPS: `git clone https://github.com/neelkamath/spacy-ner-server.git`
1. `cd spacy-ner-server`
1. Create an environment.
    - Windows: `py -3 -m venv venv`
    - Other: `python3 -m venv venv`
1. `pip install -r requirements.txt`

## [Developing](developing.md)