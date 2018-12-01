from setuptools import find_packages, setup
from codecs import open
from os import path

version = '0.0.1'

# here = path.abspath(path.dirname(__file__))

# # Get the long description from the README file
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#     readme = f.read()
readme = ''

REQUIRES = [
    'gmpy2',
    'pycryptodomex',
    'typing',
    'hashpumpy @ https://github.com/bwall/HashPump/tarball/master'
]

setup(
    name='cat',
    version=version,
    description='',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='random-access',
    author_email='random-access@invalid',
    maintainer='random-access',
    maintainer_email='random-access@invalid',
    url='https://github.com/random-access/cat',
    license='BSD',

    keywords=[
        'crypto', 'ctf', 'pentesting', 'cryptanalyis'
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    packages=find_packages(),

    install_requires=REQUIRES,

    extras_require={
        'dev': ['ipython'],
        'test': ['pytest', 'hypothesis',  'tox', 'pytest-benchmark'],
        'doc': ['sphinx', 'recommonmark', 'sphinx_rtd_theme']
    }
)
