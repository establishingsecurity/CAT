import pytest

from cat.log import enable_logging


def pytest_addoption(parser):
    parser.addoption(
        "--slow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--enable-logs",
        "--enable-logging",
        action="store_true",
        default=False,
        help="enable logging output (use together with -s)",
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--slow"):
        # --slow given in cli: do not skip slow tests

        skip_slow = pytest.mark.skip(reason="need --slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

    if config.getoption("--enable-logs"):
        enable_logging()
