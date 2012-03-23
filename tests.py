import unittest
import difflib
import sys
from __init__ import patch

class TestDiff(unittest.TestCase):

    def setUp(self):
        self.nodefile_path = 'data/nodelist.362'
        self.nodediff_path = 'data/nodediff.003'
        self.comparison_path = 'data/nodelist.003'

    def test_diff(self):
        s = patch(self.nodefile_path, self.nodediff_path)
        diff = difflib.unified_diff(s, open(self.comparison_path, "rU").readlines(),
                fromfile='calculated', tofile='actual')
        if diff:
            for line in diff:
                sys.stdout.write(line)
            open('error.list', 'w').writelines(s)
            self.assertIsNone(diff)
