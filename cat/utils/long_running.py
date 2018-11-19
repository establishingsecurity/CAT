from functools import wraps
from pickle import dumps, load

from cat.config import snapshots_path

class Snapshot():
    def __init__(self, args, kwargs, value):
        self.value = value
        self.args = args
        self.kwargs = kwargs

def long_running(fun):
    @wraps(fun)
    def with_state(*args, **kwargs):
        # TODO: distinguish snaps with arguments
        snap_file = snapshots_path/fun.__name__

        # Check if we cached the result
        if snap_file.is_file():
            with snap_file.open('rb') as f:
                snap = load(f)
            if snap.args == args and snap.kwargs == kwargs:
                return snap.value

        # Really run the function
        value = fun(*args, **kwargs)
        snap = dumps(Snapshot(args, kwargs, value))
        # Cache the result
        with snap_file.open('wb') as f:
            f.write(snap)
        return value
    return with_state
