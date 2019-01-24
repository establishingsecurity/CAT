import threading
from . import Path


class Context:
    def __init__(self, snapshots_path=None):
        try:
            dc = DefaultContext
        except NameError:
            pass
        self.snapshots_path = (
            Path(snapshots_path) if snapshots_path else dc.snapshots_path
        )


DefaultContext = Context(snapshots_path=Path(".") / "__catcache__")


local = threading.local()
if hasattr(local, "__cat_context__"):
    del local.__cat_context__


def getcontext(_local=local):
    """Returns this thread's context.

    If this thread does not yet have a context, returns
    a new context and sets this thread's context.
    New contexts are copies of DefaultContext.
    """
    if hasattr(_local, "__cat_context__"):
        return _local.__cat_context__
    else:
        context = Context()
        _local.__cat_context__ = context
        return context


def setcontext(context, _local=local):
    """Set this thread's context to context."""
    _local.__cat_context__ = context
