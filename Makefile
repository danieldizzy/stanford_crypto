.DEFAULT_GOAL := test

init:
	pip install -r requirements.txt

test: clean
	python -m unittest discover

# AES tests
a:
	python -m unittest test.test_everything.Test_AES

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
	echo '----------------------------------'
	python -m week_3.bonus test/week_3_bonus_test.txt
	echo '----------------------------------'
	python -m week_4.bonus

.PHONY: test clean
