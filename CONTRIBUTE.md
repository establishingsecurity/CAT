# How to Contribute

## Build the Documentation

To build the documentation you need to install additional dependencies:

In a python virtualenv of your choice:

```
pip install -e '.[dev,test,doc]'
cd doc
make html
```

The doc is then available at `_build/html/index.html`.
