#!/usr/bin/env sh

# Builds and uploads every image (e.g., neelkamath/spacy-server:v1-en_core_web_sm) to Docker Hub.

# Get the HTTP API version.
version=$(grep version docs/openapi.yaml -m 1)
version=${version#*: }
version=v$(echo "$version" | cut -d "'" -f 2)

# Log in.
echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USER" --password-stdin https://index.docker.io/v1/

# Build and upload the images.
while IFS='' read -r model || [ -n "$model" ]; do
  docker build --build-arg SPACY_MODEL="$model" -t "$DOCKER_HUB_USER"/spacy-server:"$version"-"$model" .
  docker push "$DOCKER_HUB_USER"/spacy-server:"$version"-"$model"
done <scripts/models.txt
