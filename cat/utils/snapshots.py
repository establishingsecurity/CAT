import shutil
from functools import wraps
from pickle import dumps, load
from hashlib import sha256

from cat.config import snapshots_path

class SnapshotHeader():
    def __init__(self, name, args, kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        h = sha256()
        h.update(dumps(self))
        return h.hexdigest()


class Snapshot():
    def __init__(self, header, value):
        self.header = header
        self.value = value


def long_running(fun):
    @wraps(fun)
    def with_state(*args, **kwargs):
        # Check if we cached the result
        snap = load_snapshot(fun.__name__, args, kwargs)
        if snap and snap.header.args == args and snap.header.kwargs == kwargs:
            return snap.value

        # Really run the function
        value = fun(*args, **kwargs)
        save_snapshot(fun.__name__, args, kwargs, value)
        return value
    return with_state


def load_snapshot(name, args, kwargs={}):
    """
    Loads a snapshot
    """
    snap_header = SnapshotHeader(name, args, kwargs)
    snap_file = snapshots_path/str(snap_header)
    print("Loading from {}".format(snapshots_path))
    if snap_file.is_file():
        with snap_file.open('rb') as f:
            snap = load(f)
            return snap

def save_snapshot(name, args, kwargs, value):
    """
    Stores a snapshot
    """
    snap_header = SnapshotHeader(name, args, kwargs)
    snap_file = snapshots_path/str(snap_header)
    snapshots_path.mkdir(exist_ok=True, parents=True)
    print("Saving to {}".format(snapshots_path))
    snap = dumps(Snapshot(snap_header, value))
    with snap_file.open('wb') as f:
        f.write(snap)

def clear_snapshots():
    shutil.rmtree(snapshots_path)
