import cat.config
from cat.utils.snapshots import long_running, load_snapshot


def test_long_running():
    @long_running
    def f(a, b, c=None):
        if c == None:
            return a + b
        else:
            return a + b + c

    v = f(1,2,3)

    snap = load_snapshot(f.__name__, (1,2), {'c': 3})
    # DAFUQ: This is None
    print(snap)

    assert snap
    assert snap.value == v
