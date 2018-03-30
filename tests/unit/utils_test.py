import unittest
import utils


class TestUtils(unittest.TestCase):

    def test_join_paths(self):
        self.assertEqual(utils.join_paths('foo/', 'bar/'), 'foo/bar/',
                         'The two paths were not joined correctly.')
