#!/usr/bin/env sh

# Sets up the development environment.

python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python -m spacy download "$SPACY_MODEL"
