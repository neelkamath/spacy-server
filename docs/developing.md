# Developing

## Server

Replace `<MODEL>` with the name of the [spaCy model](https://spacy.io/models) (e.g., `en_core_web_sm`). The model must be compatible with the spaCy version specified in [requirements.txt](../requirements.txt). Replace `<ENABLED>` with `1` or `0` to enable to disable sense2vec respectively.

### Development

```
SPACY_MODEL=<MODEL> SENSE2VEC=<ENABLED> docker-compose -p dev --project-directory . \
    -f docker/docker-compose.yml -f docker/docker-compose.override.yml up --build
```

The server will be running on `http://localhost:8000`, and has automatic reload enabled.

### Testing

```
docker-compose -p test --project-directory . -f docker/docker-compose.yml -f docker/docker-compose.test.yml \
    run --service-ports app sh -c '. scripts/setup.sh && bash'
   ```

Changes to the source code will automatically be mirrored in the container. A bind mount connects the project directory and the container so that you can run commands like `pytest`.

### Production

```
docker build <TARGET> --build-arg SPACY_MODEL=<MODEL> -t spacy-server -f docker/Dockerfile .
```
Replace `<TARGET>` with `--target base` if you want to disable sense2vec, and an empty string otherwise.

The container `EXPOSE`s port `8000`. Run using `docker run --rm -p 8000:8000 spacy-server`.

## Specification

`docs/spec/` contains the [OpenAPI specification](https://swagger.io/specification/) for the HTTP API. Use `$ref` instead of inlining `schema`s so that OpenAPI Generator will give usable names to the models.

### Developing

``` 
npx redoc-cli serve docs/spec/openapi.yaml -w
```

### Testing

```
npx @stoplight/spectral lint docs/spec/openapi.yaml
```

Open `http://127.0.0.1:8080` in your browser. The documentation will automatically rebuild whenever you save a change to `docs/spec/openapi.yaml`. Refresh the page whenever you want to view the updated documentation.

### Production

``` 
npx redoc-cli bundle docs/spec/openapi.yaml -o redoc-static.html --title 'spaCy Server'
```

Open `redoc-static.html` in your browser.

## Releases

- If you haven't updated the HTTP API functionality, skip this step.
    1. If you haven't bumped the version in the OpenAPI spec, delete the corresponding GitHub release and git tag.
    1. Generate  `redoc-static.html`: `npx redoc-cli bundle docs/spec/openapi.yaml -o redoc-static.html --title 'spaCy Server'`
    1. Create a GitHub release. The release's body should be ```Download and open the release asset, `redoc-static.html`, in your browser to view the HTTP API documentation.```. Upload `redoc-static.html` as an asset.
- If required, update the [Docker Hub repository](https://hub.docker.com/r/neelkamath/spacy-server)'s **Overview**.
- For every commit to the `master` branch in which the tests have passed, the following will automatically be done.
    - The new images will be uploaded to Docker Hub.
    - The new documentation will be hosted.