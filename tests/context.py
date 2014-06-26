import sys
import os
from contextlib import contextmanager



sys.path.insert(0, os.path.abspath('../src/'))


# Following two are borrowed from:
# http://stackoverflow.com/questions/1809958/hide-stderr-output-in-unit-tests

@contextmanager
def nostderr():
    savestderr = sys.stderr

    class Devnull(object):
        def write(self, _):
            pass
    sys.stderr = Devnull()
    try:
        yield
    finally:
        sys.stderr = savestderr


@contextmanager
def nostdout():
    savestdout = sys.stdout

    class Devnull(object):
        def write(self, _):
            pass
    sys.stdout = Devnull()
    try:
        yield
    finally:
        sys.stdout = savestdout


from BanzaiDB import converters
