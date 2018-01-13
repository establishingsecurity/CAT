from io import open

from setuptools import find_packages, setup

version = '0.0.1'

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

REQUIRES = ["gmpy2==2.0.8", "pycryptodomex==3.4.7"]

setup(
    name='cat',
    version=version,
    description='',
    long_description=readme,
    author='random-access',
    author_email='random-access@invalid',
    maintainer='random-access',
    maintainer_email='random-access@invalid',
    url='https://github.com/random-access/cat',
    license='BSD',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    packages=find_packages(),
)
