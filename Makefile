.DEFAULT_GOAL := test

test: clean
	python -m unittest discover

clean:
	find . -name '*.pyc' -exec rm -f {} +

runall: test
	echo 'ASSIGNMENTS'
	python -m week_2.assignment

.PHONY: test clean
