#!/bin/bash

set -e

docker build -t cat-test -f Dockerfile.test .
docker run --rm -it cat-test ipython
