#!/usr/bin/env bash

# Executes a command in a virtual environment (e.g., <sh setup.sh 'uvicorn main:app --reload'>).

python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
$1
