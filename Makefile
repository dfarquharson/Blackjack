REPO = dsjf-blackjack
VERSION = $(shell git rev-parse HEAD)
WORKDIR = $(shell pwd)
UUID = $(shell python -c 'import uuid; print(uuid.uuid4())')

build:
	docker build -t $(REPO):$(VERSION) .

run: build
	docker run -it --rm $(REPO):$(VERSION)

run-log: build
	docker run -it --rm \
		--volume=$(WORKDIR):/code \
		$(REPO):$(VERSION) \
		python blackjack.py > game-$(UUID).log

repl: build
	docker run -it --rm $(REPO):$(VERSION) ipython

style: build
	docker run -it --rm $(REPO):$(VERSION) pycodestyle *.py

test: build
	docker run -it --rm $(REPO):$(VERSION) pytest test_*.py

coverage:
	pytest --cov-report term \
		--cov-branch \
		--cov .

coverage-html:
	pytest --cov-report html \
		--cov-branch \
		--cov .

logs-list:
	ls -laht | grep .log

logs-nuke:
	rm game-*.log
