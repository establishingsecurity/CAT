.PHONY: base test

TEST_RESULTS = test-results.json
PACKAGE = dist

all: base $(TEST_RESULTS)

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

$(PACKAGE): package
	docker cp cat-dist:/app/dist dist

clean:
	rm $(TEST_RESULTS)
	rm $(DIST_RESULTS)
	docker rmi -f cat-base || true
	docker rmi -f cat-test || true
	docker rmi -f cat-package || true
