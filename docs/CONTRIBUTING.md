# Contributing

If you're forking the repo to develop the project as your own and not just to send back a PR, follow [these steps](fork.md).

## Installation

1. Install [Docker](https://hub.docker.com/search/?type=edition&offering=community).
1. If you are generating documentation or testing the spec, install [node.js](https://nodejs.org/en/download/).
1. Clone the repository using one of the following methods.
    - SSH: `git clone git@github.com:neelkamath/spacy-server.git`
    - HTTPS: `git clone https://github.com/neelkamath/spacy-server.git`
1. If you are not going to use sense2vec, skip this step. Download the [pretrained vectors](https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz). Extract it into the project's `src` directory.

## [Developing](developing.md)