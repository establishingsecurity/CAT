# Base image
FROM python:3.7-slim as base

# RUN apt-get update && apt-get install -y \
# 	build-essential \
#         libmpc-dev \
#         python3.7 \
#         python3.7-dev \
# 	python-pip \
# 	python3-pip \
# 	libssl-dev \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD README.md /app/README.md
ADD setup.py /app/setup.py

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
