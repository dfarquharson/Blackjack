REPO = dsjf-blackjack
VERSION = $(shell git rev-parse HEAD)

build:
	docker build -t $(REPO):$(VERSION) .

run: build
	docker run -it --rm $(REPO):$(VERSION)

repl: build
	docker run -it --rm $(REPO):$(VERSION) ipython

style: build
	docker run -it --rm $(REPO):$(VERSION) pycodestyle *.py

test: build
	docker run -it --rm $(REPO):$(VERSION) pytest test_*.py

coverage: build
	docker run -it --rm $(REPO):$(VERSION) \
		pytest --cov-report term \
		--cov . \
		--cov-branc
