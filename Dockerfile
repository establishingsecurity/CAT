FROM debian:stretch-slim
ENV RUN_ARGS=""

RUN apt-get update && apt-get install -y \
    build-essential \
	libgmp-dev \
	libmpfr-dev \
	libmpc-dev \
	python3 \
	python3-dev \
	python3-pip \
	python \
	python-dev \
	pypy \
	pypy-dev \
	&& rm -rf /var/lib/apt/lists/*

# Add test dependencies
RUN pip3 install tox

WORKDIR /app
ADD README.md /app/README.md
ADD setup.py /app/setup.py
ADD conftest.py /app/conftest.py
ADD tox.ini /app/tox.ini

WORKDIR /app/cat
RUN tox --notest

ADD cat /app/cat

CMD tox ${RUN_ARGS}
