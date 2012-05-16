#!/usr/bin/env python
"""
Take a nodefile and a nodediff and apply the nodediff
"""
import difflib
import optparse

def patch(nodefile, nodediff):
    """
    Applies the nodediff file to the nodefile, returning the final string.
    """
    s = []
    nfl_counter = 0 # keeps track of the nodefile line
    add_counter = 0 # keeps track of the nodediff lines to add

    with open(nodefile, "rU") as nf:
        nfl = nf.readlines()
        with open(nodediff, "rU") as nd:
            for ndl in nd.readlines()[1:]:
                if add_counter:
                    s.append(ndl)
                    add_counter -= 1
                elif ndl.startswith('A'):
                    add_counter = int(ndl[1:])
                elif ndl.startswith('D'):
                    nfl_counter += int(ndl[1:])
                elif ndl.startswith('C'):
                    s += nfl[nfl_counter:nfl_counter + int(ndl[1:])]
                    nfl_counter += int(ndl[1:])
    return s

def diff_nodelists(s, path):
    return difflib.unified_diff(s, filter_ctrlz(path), 'calculated', 'actual')

def filter_ctrlz(path):
    s = open(path, "rU").readlines()
    if s[-1] == chr(26):
        print 'Filtered out ctrl-z'
        return s[:-1]
    return s

def main():
    p = optparse.OptionParser()
    p.add_option('--patch', '-p', nargs=2, dest="patch_file_paths",
            help="patch a file with a nodediff and output resulting nodelist to standard out.")
    p.add_option('--diff', '-d', nargs=2, dest="diff_file_paths",
            help="diff two nodefiles and output the results in unified diff format to standard out.")
    (options, arguments) = p.parse_args()
    if options.patch_file_paths:
        print ''.join(patch(options.patch_file_paths[0], options.patch_file_paths[1]))
    if options.diff_file_paths:
        print ''.join(diff_nodelists(open(options.diff_file_paths[0], 'rU').read(), options.diff_file_paths[1]))

if __name__ == '__main__':
        main()
