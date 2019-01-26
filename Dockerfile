# Base image
FROM debian:buster-slim as base

RUN apt-get update && apt-get install -y \
	build-essential \
	libgmp-dev \
	libmpfr-dev \
	libmpc-dev \
	python3.6 \
	python3.6-dev \
	python3-pip \
	python \
	python-pip \
	libssl-dev \
	libflint-dev \
	# libflint-arb-dev \
    && rm -rf /var/lib/apt/lists/*

# TODO: Fix this madness, this is a dirty workaround
# First build newest version of arb, this takes some time
WORKDIR /build
ADD https://github.com/fredrik-johansson/arb/archive/2.16.0.tar.gz /build/
RUN tar xvf "2.16.0.tar.gz"
WORKDIR /build/arb-2.16.0
RUN ./configure && make && make install && ldconfig

WORKDIR /app
ADD README.md /app/README.md
ADD setup.py /app/setup.py

# TODO: Fix this madness, this is a dirty workaround
# Cython is needed to build some other stuff, and for some reason numpy too
RUN pip3 install cython numpy

RUN pip3 install -e "."

ADD cat /app/cat

# Test image
FROM base as test
ENV RUN_ARGS=""

RUN pip3 install -e ".[test,format]"

ADD conftest.py /app/conftest.py
ADD tox.ini /app/tox.ini

RUN tox --notest
ADD test /app/test

CMD tox --result-json /app/test-results.json -- ${RUN_ARGS}

# Doc image
FROM base as doc

RUN pip3 install -e ".[dev,doc]"
RUN apt-get update && apt-get install -y \
	texlive-full \
	inkscape \
	poppler-utils \
	graphviz \
    && rm -rf /var/lib/apt/lists/*

ADD doc /app/doc

WORKDIR /app/doc
CMD make html

# Dist image
FROM base as dist

RUN pip install setuptools wheel
RUN pip3 install setuptools wheel

CMD python3 setup.py sdist bdist_wheel && python setup.py sdist bdist_wheel
