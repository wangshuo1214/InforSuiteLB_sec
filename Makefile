.PHONY: all build publish

all: build publish

build:
	python setup.py bdist_wheel --universal sdist

publish:
	twine upload dist/*-`grep -oP "(?<=version\s=\s['\"])[^'\"]*(?=['\"])" inforsuitelb_sec/__init__.py`*
