#!/usr/bin/env sh

# Builds and uploads every image (e.g., neelkamath/spacy-server:2-en_core_web_sm-sense2vec) to Docker Hub.

# Get the HTTP API version.
version=$(grep version docs/openapi.yaml -m 1)
version=${version#*: }
version=$(echo "$version" | cut -d "'" -f 2)

# Log in.
echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USER" --password-stdin https://index.docker.io/v1/

# Build and upload the images.
while IFS='' read -r spacy_model || [ -n "$spacy_model" ]; do
  base_tag="$DOCKER_HUB_USER"/spacy-server:"$version"-"$spacy_model"
  sense2vec_tag="$base_tag"-sense2vec
  docker build --target base --build-arg SPACY_MODEL="$spacy_model" -t "$base_tag" -f docker/Dockerfile .
  docker build --build-arg SPACY_MODEL="$spacy_model" -t "$sense2vec_tag" -f docker/Dockerfile .
  docker push "$base_tag"
  docker push "$sense2vec_tag"
  docker rmi "$base_tag" "$sense2vec_tag" # Prevent the device (e.g., CI runner) from running out of space and crashing.
done <scripts/models.txt
