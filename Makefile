default: install


h help:
	@grep '^[a-z]' Makefile

install:
	pip install pip --upgrade
	pip install -r requirements.txt

run:
	python -m app
