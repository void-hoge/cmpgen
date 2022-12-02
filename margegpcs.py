#!/usr/bin/env python3

import sys
import parsegpc
from solution import solution

def main():
    solfilename = sys.argv[1]
    gpcfilename = sys.argv[2]
    rawsol = open(solfilename, 'r').read()
    rawgpcs = open(gpcfilename, 'r').read()
    sol = solution(rawsol)
    gpcs = parsegpc.parsegpcs(rawgpcs)
    sol.margegpcs(gpcs)
    sol.dump()

if __name__ == '__main__':
    main()
