import shutil

from .utils.fs_utils import TEMP_DIR


def pytest_sessionfinish(session, exitstatus):
    """Runs after all tests have completed."""

    shutil.rmtree(TEMP_DIR, True)
