# How to Contribute

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

To build the documentation you need to install additional dependencies:

In a python virtualenv of your choice:

```
pip install -e '.[dev,test,doc]'
cd doc
make html
```

The doc is then available at `_build/html/index.html`.
