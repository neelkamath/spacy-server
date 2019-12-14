# Developing

## Server

### Development

```
docker-compose -p dev up --build
```

The server will be running on `http://localhost:8000`, and has automatic reload enabled.

### Testing

```
docker-compose -p test -f docker-compose.yml -f docker-compose.test.yml \
    up --build --abort-on-container-exit --exit-code-from app
```

### Production

```
docker build -t spacy-server .
```

The container `EXPOSE`s port `8000`. To serve at `http://localhost:8080`, run `docker run --rm -p 8000:8000 spacy-server`.

## Specification

`docs/openapi.yaml` is the [OpenAPI specification](https://swagger.io/specification/) for the HTTP API. Use `$ref` instead of inlining `schema`s so that OpenAPI Generator will name give usable names to the models.

### Testing

```
npx @stoplight/spectral lint docs/openapi.yaml
```

## Documentation

### Developing

``` 
npx redoc-cli serve docs/openapi.yaml -w
```

Open `http://127.0.0.1:8080` in your browser. 

The documentation will automatically rebuild whenever you save a change to `docs/openapi.yaml`. Refresh the page whenever you want to view the updated documentation.

### Production

``` 
npx redoc-cli bundle docs/openapi.yaml -o redoc-static.html --title 'spaCy Server'
```

Open `redoc-static.html` in your browser.

## Releases

- Create a GitHub release (this will automatically create the git tag). If you bumped the version in `docs/openapi.yaml`, then create a new release. If you haven't bumped the version but have updated the HTTP API's functionality, delete the existing GitHub release and git tag, and create a new one. Otherwise, skip this step. The release's title should be the features included (e.g., `NER, POS tagging, sentencizer, tokenizer, and sense2vec`). The tag should be the HTTP API's version (e.g., `v1`). The release's body should be ```Download and open the release asset, `redoc-static.html`, in your browser to view the HTTP API documentation.```. Upload the asset named `redoc-static.html` which contains the HTTP API docs.
- If required, update the [Docker Hub repository](https://hub.docker.com/r/neelkamath/spacy-server)'s **Overview**.
- For every commit to the `master` branch in which the tests have passed, the following will automatically be done.
    - The new images will be uploaded to Docker Hub.
    - The new documentation will be hosted.