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
  tag="$DOCKER_HUB_USER"/spacy-server:"$version"-"$model"
  docker build --build-arg SPACY_MODEL="$model" -t "$tag" -f docker/Dockerfile .
  docker push "$tag"
  docker rmi "$tag" # Delete the image to prevent the device (e.g., CI runner) from running out of space and crashing.
done <scripts/models.txt
