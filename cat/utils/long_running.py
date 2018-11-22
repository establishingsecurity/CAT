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
        # TODO: distinguish snaps with arguments
        snap_header = SnapshotHeader(fun.__name__, args, kwargs)
        snap_file = snapshots_path/str(snap_header)

        # Check if we cached the result
        if snap_file.is_file():
            with snap_file.open('rb') as f:
                snap = load(f)
            if snap.args == args and snap.kwargs == kwargs:
                return snap.value

        # Really run the function
        value = fun(*args, **kwargs)
        snap = dumps(Snapshot(snap_header, value))
        # Cache the result
        snapshots_path.mkdir(exist_ok=True, parents=True)
        with snap_file.open('wb') as f:
            f.write(snap)
        return value
    return with_state
