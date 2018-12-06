from enum import Enum


class Severity(Enum):
    OK = 0
    SUSPICIOUS = 1
    CRITICAL = 2


class CheckResult:
    def __init__(self, severity=Severity.OK, comment=""):
        self.severity = severity
        self.comment = comment
