from abc import ABCMeta


class Oracle():
    """
    Base class to be implemented by complete attacks requiring oracles

    To use such an oracle for attacks, implement the query method for your
    target
    """
    __metaclass__ = ABCMeta

    def query(self, msg):
        # type: bytes
        pass

