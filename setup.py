from codecs import open
from os import path

from setuptools import find_packages, setup

version = "0.2.0"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

REQUIRES = [
    "gmpy2>=2,<3",
    "pycryptodomex>=3,<4",
    "typing>=3,<4",
    "hashpumpy @ https://github.com/bwall/HashPump/tarball/master",
    "dask[bag]>=2,<3",
    "distributed>=2,<3",
    "bitstring>=3,<4",
    "flint-py>=0,<1",
    "sympy>=1,<2",
]

setup(
    name="cat",
    version=version,
    description="",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="random-access",
    author_email="random-access@invalid",
    maintainer="random-access",
    maintainer_email="random-access@invalid",
    url="https://github.com/random-access/cat",
    license="BSD",
    keywords=["crypto", "ctf", "pentesting", "cryptanalyis"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=find_packages(),
    install_requires=REQUIRES,
    extras_require={
        "dev": ["ipython>=7,<8"],
        "doc": ["sphinx>=2,<3", "sphinx_rtd_theme>=0,<1", "sphinxcontrib-apidoc>=0,<1"],
        "test": [
            "pytest>=5,<6",
            "hypothesis>=5,<6",
            "tox>=3,<4",
        ],
        "format": ["black", "isort", "pytest-black", "pytest-isort"],
    },
)
