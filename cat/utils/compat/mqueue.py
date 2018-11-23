import sys

if sys.version_info.major < 3:
    from multiprocessing import Queue
    import Queue as _Q

    Full = _Q.Full
    Empty = _Q.Empty
else:
    from multiprocessing import Queue
    from queue import Full, Empty
