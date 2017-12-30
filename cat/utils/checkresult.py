from enum import Enum

class CheckResult():
    comment = ''
    severity = Severity.OK


class Severity(Enum):
    OK = 0
    SUSPICIOUS = 1
    CRITICAL = 2
