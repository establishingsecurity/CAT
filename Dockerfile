# Base image
FROM debian:stretch-slim as base

RUN apt-get update && apt-get install -y \
	build-essential \
	libgmp-dev \
	libmpfr-dev \
	libmpc-dev \
	python3 \
	python3-pip \
	python \
	python-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD README.md /app/README.md
ADD setup.py /app/setup.py

RUN pip3 install -e "."

ADD cat /app/cat
WORKDIR /app/cat

# Test image
FROM base as test
ENV RUN_ARGS=""

RUN apt-get update && apt-get install -y \
	pypy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip3 install -e ".[test]"

ADD conftest.py /app/conftest.py
ADD tox.ini /app/tox.ini

RUN tox --notest

CMD tox --result-json /app/test-results.json -- ${RUN_ARGS}

# Doc image
FROM base as doc

RUN apt-get update && apt-get install -y \
	pypy \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -e ".[doc]"

ADD doc /app/doc
WORKDIR /app/doc
CMD make
