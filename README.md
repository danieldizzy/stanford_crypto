# Stanford Crypto course

Course: https://www.coursera.org/learn/crypto/

Repo for solutions, misc hacking, etc.  This is less about learning
existing Python libraries than it is to understand crypto concepts.

I code in Python only infrequently, and so if you see something that
could be done better, please open an issue or create a PR ...  Thank
you.

Reddit: https://www.reddit.com/r/Stanfordcrypto/

## Code

Each assignment/project/whatever is a regular python module.

```
python path/to/assignment.py
```

There are some sanity check unit test checks that exec the modules in
`test`:

```
make test
```

or

```
python -m unittest discover
```

These are not real tests, but they ensure that things work.
