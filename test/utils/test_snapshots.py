import tempfile
import shutil
from pathlib import Path

import pytest

import cat.config
from cat.utils.snapshots import long_running, load_snapshot

@pytest.fixture()
def testdir():
    tmpdir = Path(tempfile.mkdtemp())
    cat.config.snapshots_path = tmpdir
    yield tmpdir
    shutil.rmtree(tmpdir)


def test_long_running_kwargs(testdir):
    @long_running
    def f(a, b, c=None):
        if c == None:
            return a + b
        else:
            return a + b + c

    v = f(1,2,c=3)

    snap = load_snapshot(f.__name__, (1,2), {'c':3})
    print(cat.config.snapshots_path)

    assert snap
    assert snap.value == v



def test_long_running_no_kwargs(testdir):
    @long_running
    def f(a, b, c=None):
        if c == None:
            return a + b
        else:
            return a + b + c

    v = f(1,2,3)

    snap = load_snapshot(f.__name__, (1,2,3))

    assert snap
    assert snap.value == v

# @pytest.mark.xfail(reason="Testdir is not used by cat")
def test_long_running_fail(testdir):
    @long_running
    def f(a, b, c=None):
        if c == None:
            return a + b
        else:
            return a + b + c

    v = f(1,2,3)

    snap = load_snapshot(f.__name__, (1,2), {'c':3})

    assert snap == None
