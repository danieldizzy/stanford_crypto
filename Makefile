.DEFAULT_GOAL := test

test: clean
	python -m unittest discover

clean:
	find . -name '*.pyc' -exec rm -f {} +

runall: test
	echo 'ASSIGNMENTS'
	echo '----------------------------------'
	python -m week_1.assignment.q7
	echo '----------------------------------'
	python -m week_1.assignment.bonus
	echo '----------------------------------'
	python -m week_2.assignment

.PHONY: test clean
