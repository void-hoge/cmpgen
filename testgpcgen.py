#!/usr/bin/env python3

import sys
import parsegpc

def main():
    gpclist = sys.argv[1]
    raw = open(gpclist, 'r').read()
    gpcs = parsegpc.parsegpcs(raw)
    for gpc in gpcs:
        print(parsegpc.gensimplegpc(gpc))

if __name__ == '__main__':
    main()
