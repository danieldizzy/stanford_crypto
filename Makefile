.DEFAULT_GOAL := test

test: clean
	python -m unittest discover

# AES tests
a:
	python -m unittest test.test_everything.Test_AES.test_expand_key

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
	echo '----------------------------------'
	python -m week_2.bonus

.PHONY: test clean
