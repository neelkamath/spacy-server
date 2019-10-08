# Developing

## Server

### Development

1. Activate the environment.
    - Windows: `venv\Scripts\activate`
    - Other: `. venv/bin/activate`
1. Set Flask to development mode.
    - Windows: `set FLASK_ENV=development`
    - Other: `export FLASK_ENV=development`
1. `flask run`

The server will be running on `http://127.0.0.1:5000`, and will have automatic reload enabled.

### Testing

1. Activate the environment.
    - Windows: `venv\Scripts\activate`
    - Other: `. venv/bin/activate`
1. Test.
    - Server: `python test.py`
    - spaCy compatibility: `python -m spacy validate`

### Production

`docker build . -t spacy-ner-server`

To serve at `http://localhost:8080`, run `docker run --rm -p 8080:8080 spacy-ner-server`. You can change the port by setting the `PORT` environment variable (e.g., `docker run --rm -e PORT=6969 -p 6969:6969 crytal-skull`). The container `EXPOSE`s port `8080`.

## Specification

`docs/openapi.yaml` is the [OpenAPI specification](https://swagger.io/specification/) for the HTTP API.

### Testing

`spectral lint docs/openapi.yaml`

## Documentation

### Developing

`redoc-cli serve docs/openapi.yaml -w`

Open `http://localhost:8080` in your browser. 

The documentation will automatically rebuild whenever you save a change to `docs/openapi.yaml`. Refresh the page whenever you want to view the updated documentation.

### Production

`redoc-cli bundle docs/openapi.yaml -o public/index.html --title 'Crystal Skull'`

Open `public/index.html` in your browser.

## Releases

- If you are bumping the HTTP API version in `docs/openapi.yaml`, create a corresponding git tag and GitHub release.
- If required, update the [Docker Hub repository](https://hub.docker.com/r/neelkamath/crystal-skull)'s **Overview**.
- For every commit to the `master` branch in which the tests have passed, the following will automatically be done.
    - The new images will be uploaded to Docker Hub.
    - The Heroku deployment will be updated.
    - The new documentation will be hosted.