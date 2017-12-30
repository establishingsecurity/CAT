from abc import ABC
class Oracle(ABC):
    """
    Base class to be implemented by complete attacks requiring oracles

    To use such an oracle for attacks, implement the query method for your
    target
    """

    def query(self, msg: bytes):
        pass

