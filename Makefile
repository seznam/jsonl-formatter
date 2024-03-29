init:
	pip install -r requirements.txt

test:
	python -m unittest discover -s tests

docker:
	docker build . --tag=seznam/jsonl-formatter:latest

docker-run:
	docker run -ti -v $$PWD:/mnt/pwd --entrypoint=bash seznam/jsonl-formatter

.PHONY: init test docker docker-run
