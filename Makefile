.PHONY: base test doc

TEST_RESULTS = test-results.json
DIST_RESULTS = dist
DOC_RESULTS = doc/_build

all: base $(TEST_RESULTS)

test-results: $(TEST_RESULTS)
doc-results: $(DOC_RESULTS)
dist-results: $(DIST_RESULTS)

base:
	docker rmi -f cat-base || true
	docker build --target base -t cat-base .

test:
	docker build --target test -t cat-test .
	docker rm cat-test || true
	docker run --name cat-test cat-test || true

test-slow:
	docker build --target test -t cat-test .
	docker rm cat-test || true
	docker run --name cat-test --env RUN_ARGS="--slow" cat-test || true

$(TEST_RESULTS): test
	docker cp cat-test:/app/test-results.json test-results.json
	docker cp cat-test:/app/test-results-py2.xml test-results-py2.xml
	docker cp cat-test:/app/test-results-py3.xml test-results-py3.xml


package:
	docker build --target dist -t cat-package .
	docker rm cat-package || true
	docker run --name cat-package cat-dist || true

$(DIST_RESULTS): package
	docker cp cat-dist:/app/dist dist

$(DOC_RESULTS): doc
	docker cp cat-doc:/app/doc/_build $(DOC_RESULTS)

doc:
	docker build --target doc -t cat-doc .
	docker rm cat-doc || true
	docker run --name cat-doc cat-doc || true

clean:
	rm $(TEST_RESULTS) || true
	rm -rf $(DIST_RESULTS) || true
	rm $(DOC_RESULTS) || true
	docker rmi -f cat-base || true
	docker rmi -f cat-test || true
	docker rmi -f cat-package || true
	docker rmi -f cat-doc || true
