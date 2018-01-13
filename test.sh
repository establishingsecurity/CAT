#!/bin/bash

set -e

docker build -t cat-test -f Dockerfile.test .
docker run --rm cat-test
docker rmi cat-test
