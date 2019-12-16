#!/usr/bin/env sh
# Builds and uploads every image (e.g., neelkamath/spacy-server:2-en_core_web_sm-sense2vec) to Docker Hub.

# Builds and deploys an image. Pass the version, spaCy model, and whether to delete the pushed images as arguments.
deploy () {
  base_tag="$DOCKER_HUB_USER"/spacy-server:"$1"-"$2"
  sense2vec_tag="$base_tag"-sense2vec
  docker build --target base --build-arg SPACY_MODEL="$2" -t "$base_tag" -f docker/Dockerfile .
  docker build --build-arg SPACY_MODEL="$2" -t "$sense2vec_tag" -f docker/Dockerfile .
  docker push "$base_tag"
  docker push "$sense2vec_tag"
  if [ "$3" = 1 ]
  then
    docker rmi "$base_tag" "$sense2vec_tag"
  fi
}

# Get the HTTP API version.
version=$(grep version docs/openapi.yaml -m 1)
version=${version#*: }
version=$(echo "$version" | cut -d "'" -f 2)

# Log in.
echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USER" --password-stdin https://index.docker.io/v1/

# Build and upload images. We prevent the device (e.g., CI runner) from running out of space and crashing by deleting
# images after they've been pushed. We don't delete the first image so that subsequent builds can use its cache.
deploy "$version" "$(head -n 1 scripts/models.txt)" 0 # Don't delete the first image.
{
  read -r # Skip the first line because we've already deployed it.
  while IFS='' read -r spacy_model || [ -n "$spacy_model" ]; do
    deploy "$version" "$spacy_model" 1
  done
}<scripts/models.txt