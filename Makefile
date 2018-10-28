.PHONY: base test

TEST_RESULTS = test-results.json

all: base $(TEST_RESULTS)

base:
	docker rmi -f cat-base || true
	docker build --target base -t cat-base .

test:
	docker build --target test -t cat-test .
	docker rm cat-test || true
	docker run --name cat-test cat-test || true

$(TEST_RESULTS): test
	docker cp cat-test:/app/test-results.json test-results.json

clean:
	rm $(TEST_RESULTS)
	docker rmi -f cat-base || true
	docker rmi -f cat-test || true
