"""
This module contains utility functions for doing a range of different
tasks. It acts as a catch-all adapter to various libraries, reducing
dependency on them. This module should definitely wrap all calls to the
os module, for example.

This module should be imported like this:
    import utils
OR this:
    from utils import <function1_name>, <function2_name>

NOT like this:
    from utils import *
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def join_paths(path1, path2):
    return os.path.join(path1, path2)

