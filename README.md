# Stanford Crypto course

Course: https://www.coursera.org/learn/crypto/

Repo for solutions, misc hacking, etc.  This is less about learning
existing Python libraries than it is to understand crypto concepts.

I code in Python only infrequently, and so if you see something that
could be done better, please open an issue or create a PR ...  Thank
you.

Reddit: https://www.reddit.com/r/Stanfordcrypto/

## Setup

OSX setup for gmpy2, per http://stackoverflow.com/questions/23187801/

```
brew install libmpc
brew install mpfr
```

```
virtualenv venv
source venv/bin/activate
make init
```

## Running the code

Each assignment/project/whatever is a python module (file).  In some
cases, you can run it directly:

```
$ python path/to/assignment.py
```

In some cases, running it as a file will give you errors:

```
$ python week_1/assignment/bonus.py
Traceback (most recent call last):
  File "week_1/assignment/bonus.py", line 12, in <module>
    from lib.helpers import *
ImportError: No module named lib.helpers
```

This is because some helpers are pulled into a separate library.  Run
these assignments from the project root dir as a module instead:

```
$ python -m week_1.assignment.bonus
```

## Tests

There are some sanity check unit test checks that exec the modules in
`test`, run them with `$ make test` or just `$ make`, or `$ python -m
unittest discover` if you're not into the whole brevity
thing[.](https://www.youtube.com/watch?v=Be7Og9Gc_KY)


These are not real tests, but they ensure that things work.
