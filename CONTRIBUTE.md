# How to Contribute

## Installing for development

1. Install non-Python dependencies:

    - flint http://flintlib.org/
    - arb http://arblib.org/

2. Install Python dependencies into a venv:

    Note: to be able to run tests without docker, you should install
    Python3.6 and/or Python 2.7

    Note: to be able to follow the coding style guidelines, the
    virtual environment should be installed exactly as below.

    ```
    virtualenv --python=/usr/bin/python3.6 ~/.virtualenvs/cat
    source ~/.virtualenvs/cat/bin/activate
    pip install --upgrade pip
    pip install cython numpy
    ```

3. Install the library (with all optional requirements):

    Note: python setup.py install will not install optional
    dependencies which are required for development. Use:

    ```
    pip install -r requirements.txt
    ```

## Conforming to the coding style

`cat` uses [black](https://github.com/ambv/black) and [isort](https://github.com/timothycrosley/isort) to enforce a common code style for the code base.
A git pre-commit hook can be found in the `git_hooks` directory which simply runs `black` and `isort` on your staged files before committing.
If you want to use it, you need to add a symlink to your virtual environment with the name `.venv` at the top level of your repository, e.g. something like:

```bash
lrwxrwxrwx. 1 user user 23 Nov 26 18:31 .venv -> /home/user/.venvs/cat/
```

If you're running Linux you can install the git hook via `git_hooks/install.sh`.
The script creates a backup of your current `hooks` directory and symlinks it to the `git_hooks` directory inside the repository.

## Build the Documentation

To build the documentation, make sure that you have installed all optional dependenices:

```
pip install -r requirements.txt
cd doc && make html
```

The doc is then available at `_build/html/index.html`.
