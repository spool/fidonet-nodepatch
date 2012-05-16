import unittest
from __init__ import patch, diff_nodelists
import pdb
import os
import datetime
import shutil
import contextlib

@contextlib.contextmanager
def chdir(dirname=None):
    curdir = os.getcwd()
    try:
        if dirname is not None:
              os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)

class TestSimpleDiff(unittest.TestCase):

    def setUp(self):
        self.nodefile_path = os.path.join('data','nodelist.362')
        self.nodediff_path = os.path.join('data', 'nodediff.003')
        self.comparison_path = os.path.join('data','nodelist.003')

    def test_diff(self):
        s = patch(self.nodefile_path, self.nodediff_path)
        diff = diff_nodelists(s, self.comparison_path)
        diff_lines = ''.join(diff)
        self.assertEqual(len(diff_lines), 0)

if os.path.exists(os.path.join('data', 'fidonet-on-the-internet')):
    class TestSimpleDiffs(unittest.TestCase):

        def setUp(self):
            nodefile_root_path = os.path.join('data', 'fidonet-on-the-internet')
            nodefile_folder_prefix = 'n'
            d = {}
            self.years = range(1993, 2004)
            for y in self.years:
                path = os.path.join(nodefile_root_path, nodefile_folder_prefix + str(y))
                nodelists = [nf for nf in sorted(os.listdir(path)) if nf.startswith('nodel')]
                for n in nodelists:
                    d[datetime.datetime.strptime(str(y) + ',' + n.split('.')[1], '%Y,%j')] = os.path.join(path, n)
            dates = sorted(d.keys())
            nodelist_pairs = []
            for i, date in enumerate(dates[:-1]):
                if dates[i+1] - date == datetime.timedelta(days=7):
                    nodelist_pairs.append((date, dates[i+1]))
                    
            self.nodelist_pairs = nodelist_pairs
            self.nodelist_paths = d
            self.nodediff_paths = {k: v.replace('nodelist.', 'nodediff.') for k, v in d.iteritems()}
            print self.nodelist_pairs

            #for p in self.nodelist_pairs:
            #    test = self.diff_test(self.nodelist_paths[p[0]], self.nodediff_paths[p[1]], self.nodelist_paths[p[1]])
            #    test.__name__ = 'test_%s' % p[0].strftime('%j, %y')
            #    print test.__name__
            #    setattr(self, test.__name__, test)

        def testDiffs(self):
            for p in self.nodelist_pairs:
                print p
                s = patch(self.nodelist_paths[p[0]], self.nodediff_paths[p[1]])
                diff = diff_nodelists(s, self.nodelist_paths[p[1]])
                diff_lines = ''.join(diff)
                if len(diff_lines) != 0: 
                    if not os.path.isdir('errors'): os.mkdir('errors')
                    open(os.path.join('errors', 'error.diff'), 'w').writelines(diff_lines)
                    open(os.path.join('errors', 'error.nodelist'), 'w').writelines(s)
                    shutil.copy(self.nodelist_paths[p[0]], os.path.join('errors', 'original.nodelist'))
                    shutil.copy(self.nodelist_paths[p[1]], os.path.join('errors', 'correct.nodelist'))
                    shutil.copy(self.nodediff_paths[p[1]], os.path.join('errors', 'original.nodediff'))
                self.assertEqual(len(diff_lines), 0)

        def diff_test(list_path, diff_path, comparison_path):
            def test_diff(self):
                s = patch(list_path, diff_path)
                diff_lines = ''.join(diff)
                self.assertEqual(len(diff_lines), 0)
            return test_diff

if __name__ == '__main__':
    unittest.main()



