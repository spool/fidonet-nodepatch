"""
Take a nodelile and a nodediff and apply the nodediff
"""

def patch(nodefile, nodediff):
    """
    Applies the nodediff file to the nodefile, returning the final string.
    """
    s = []
    nfl_counter = 0 # keeps track of the nodefile line
    add_counter = 0 # keeps track of the nodediff lines to add

    with open(nodefile) as nf:
        nfl = nf.readlines()
        with open(nodediff) as nd:
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

def check_nodefile(generated, original):
    gen  =  [l.strip() for l in open(generated).readlines()]
    orig =  [l.strip() for l in open(original).readlines()]
    return gen == orig

