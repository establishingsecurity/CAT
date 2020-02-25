import shutil
from functools import wraps
from hashlib import sha256
from pickle import dumps, load

import logging

from cat.config import getcontext

from cat.log.log import LIB_ROOT_LOGGER_NAME as LOGGER

class SnapshotHeader:
    def __init__(self, name, args, kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        h = sha256()
        h.update(dumps(self))
        return h.hexdigest()


class Snapshot:
    def __init__(self, header, value):
        self.header = header
        self.value = value


def long_running(fun):
    """
    A word of warning: This is not temporally hyper context sensitive
    """

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
    snapshots_path = getcontext().snapshots_path
    snap_header = SnapshotHeader(name, args, kwargs)
    snap_file = snapshots_path / str(snap_header)
    logger = logging.getLogger(LOGGER)
    logger.info("Loading from {}".format(snapshots_path))
    if snap_file.is_file():
        with snap_file.open("rb") as f:
            snap = load(f)
            return snap


def save_snapshot(name, args, kwargs, value):
    """
    Stores a snapshot
    """
    snapshots_path = getcontext().snapshots_path
    snap_header = SnapshotHeader(name, args, kwargs)
    snap_file = snapshots_path / str(snap_header)
    snapshots_path.mkdir(exist_ok=True, parents=True)
    logger = logging.getLogger(LOGGER)
    logger.info("Saving to {}".format(snapshots_path))
    snap = dumps(Snapshot(snap_header, value))
    with snap_file.open("wb") as f:
        f.write(snap)


def clear_snapshots():
    snapshots_path = getcontext().snapshots_path
    shutil.rmtree(str(snapshots_path))
