# Contributing to this code

This is mainly to try to document what I'm doing and not forget some of the commands or process.

The project is running with Python 3.7.6 (maybe earlier versions). `python` and `pip` commands assume Python 3.

## Contribution Installation

```bash
git git@github.com:karlcow/ymir.git
cd ymir
# To create the environment
python -m venv env
# This will activate the environment in zsh
. env/bin/activate
# To install the modules necessary for development
pip install -r requirements-dev.txt
```

## Development

Before any development, [file an issue](https://github.com/karlcow/ymir/issues). It happens time to time that I forget about opening issues. Life. But having an issue is usually easier for creating specific branches and understand the related

### Fork the project
### Branch naming style
### Commit style


## Tests

The testing came a bit late in the history.
In April 2020, I restarted to add a bit of tests to be able to more easily modify the code.

### Writing tests


### Running the tests

You can run the tests with `pytest`. This is an example of the output (as of May 2020):

```
(env) ~/code/ymir % pytest
============== test session starts ===============
platform darwin -- Python 3.7.6, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /Users/karl/code/ymir
plugins: cov-2.8.1
collected 17 items

tests/test_feed.py .                       [  5%]
tests/test_helper.py .......               [ 47%]
tests/test_parsing_month_index.py ..       [ 58%]
tests/test_parsing_posts.py ......         [ 94%]
tests/test_ymir.py .                       [100%]

================ warnings summary ================
env/lib/python3.7/site-packages/html5lib/_trie/_base.py:3
  /Users/karl/code/ymir/env/lib/python3.7/site-packages/html5lib/_trie/_base.py:3: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3,and in 3.9 it will stop working
    from collections import Mapping

-- Docs: https://docs.pytest.org/en/latest/warnings.html
========= 17 passed, 1 warning in 0.16s ==========
```

### Running tests coverage

If you are into checking how much of your code base is covered by the tests.

```
coverage run --omit env --source ymir -m pytest
coverage report -m
```

This gives (as of May 2020):

```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
ymir/__init__.py              0      0   100%
ymir/utils/__init__.py        0      0   100%
ymir/utils/feed.py          101     32    68%   108-149
ymir/utils/helper.py         73      0   100%
ymir/utils/indexes.py        43     43     0%   3-82
ymir/utils/make-post.py      79     79     0%   1-142
ymir/utils/parsing.py        46      0   100%
ymir/ymir.py                240    145    40%   121-128, 134-154, 160-208, 213-222, 230-249, 279-290, 296-426, 432
-------------------------------------------------------
TOTAL                       582    299    49%
```

Not glorious but better than nothing.