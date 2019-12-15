# Developing

## Server

Replace `<MODEL>` with the name of the [spaCy model](https://spacy.io/models) (e.g., `en_core_web_sm`, `fr_core_news_md`). The model must be compatible with the spaCy version specified in [requirements.txt](../requirements.txt).

### Development

```
SPACY_MODEL=<MODEL> docker-compose -p dev --project-directory . \
    -f docker/docker-compose.yml -f docker/docker-compose.override.yml up --build
```

The server will be running on `http://localhost:8000`, and has automatic reload enabled.

### Testing

- For noninteractive environments (e.g., CI pipelines), you can run all the tests with the single command:
    ```
    docker-compose -p test --project-directory . -f docker/docker-compose.yml -f docker/docker-compose.test.yml \
        up --build --abort-on-container-exit --exit-code-from app
    ```
- For faster iterations (e.g., while developing), you can run the tests interactively. Changes to the source code will automatically be mirrored in the container.
    1. Run:
        ```
        docker-compose -p test --project-directory . -f docker/docker-compose.yml -f docker/docker-compose.test.yml \
            run --service-ports app bash
       ```
    1. `python -m venv venv`
    1. `. venv/bin/activate`
    1. Execute tests any number of times you want with pytest (e.g., `pytest`).
    1. You can exit the container after you're done testing by running `exit`.

### Production

```
docker build --build-arg SPACY_MODEL=<MODEL> -t spacy-server -f docker/Dockerfile .
docker run --rm -e SPACY_MODEL=<MODEL> -p 8000:8000 spacy-server
```

The container `EXPOSE`s port `8000`.

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