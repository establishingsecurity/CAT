class ResultEntry(object):
    def __init__(self, severity, docstring):
        self.severity = severity
        self.docstring = docstring

    def __repr__(self):
        if self.severity == 0:
            severity = "OK"
        if self.severity == 1:
            severity = "SUSPICIOUS"
        if self.severity == 2:
            severity = "CRITICAL"
        return "{}: {}".format(severity, self.docstring)

    def __str__(self):
        return self.__repr__()


class Result(object):
    """Used to represent the results of different checks."""

    pass


class Severity(object):
    """Represents the severity of a result."""

    OK = 0
    SUSPICIOUS = 1
    CRITICAL = 2
