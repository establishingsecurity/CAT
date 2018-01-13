#!/bin/bash

set -e

RUN_ARGS=""
while [[ $# -gt 0 ]]
	do
	key="$1"
	case $key in
		-s|--slow)
		RUN_ARGS="$RUN_ARGS --slow -n auto"
		shift # past argument
		;;
		*)    # unknown option
		shift # past argument
		;;
	esac
done

docker build -t cat-test -f Dockerfile.test .
docker run --rm --env RUN_ARGS="$RUN_ARGS" cat-test
docker rmi cat-test
