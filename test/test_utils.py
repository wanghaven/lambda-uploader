import os

from os import path
from shutil import rmtree
from lambda_uploader import utils

TESTING_TEMP_DIR = '.testing_temp'

TEST_TREE = [
    'foo.py',
    'bar/foo.py',
    'bar/bar/foo.py',
    'ignore/foo.py',
    'ignore-me.py',
]
PATHS_TO_BE_IGNORED = [
    'ignore/foo.py',
    'ignore-me.py',
]

TEST_IGNORE = [
    'ignore/*',
    'ignore-me.py',
    # The one below would exclude all the files if files to be ignored were
    # matched based on the full path, rather than the path relative to the
    # source directory, since the source directory contains 'test' in its path.
    'test',
]


def test_copy_tree():
    os.mkdir(TESTING_TEMP_DIR)
    for fil in TEST_TREE:
        dir = path.dirname(fil)
        test_pth = path.join(TESTING_TEMP_DIR, dir)
        if dir is not None and not path.isdir(test_pth):
            os.makedirs(test_pth)
        with open(path.join(TESTING_TEMP_DIR, fil), 'w') as tfile:
            tfile.write(fil)

    copy_dir = '.copy_of_test'
    utils.copy_tree(TESTING_TEMP_DIR, copy_dir, TEST_IGNORE)
    for fil in TEST_TREE:
        pth = path.join(copy_dir, fil)
        assert path.isfile(pth) is (fil not in PATHS_TO_BE_IGNORED)

    rmtree(TESTING_TEMP_DIR)
    rmtree(copy_dir)


def test_ignore_file():
    result = utils._ignore_file('ignore/foo.py', TEST_IGNORE)
    assert result

    res = utils._ignore_file('bar/foo.py', TEST_IGNORE)
    assert res is False
