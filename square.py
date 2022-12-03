#!/usr/bin/env python3

import sys
import math
import parsegpc
from problem import problem

STAGEMIN, STAGEMAX = 2, 10
FINALSTAGE = 2

class square(problem):
    def __init__(self, size, gpcs, stagemin, stagemax, finalstage):
        super().__init__()
        self.size = size
        self.gpcs = gpcs
        self.stagemin = stagemin
        self.stagemax = stagemax
        self.colnum = int(math.log2(((1<<self.size)-1)*self.size))+1
        self.finalstage = finalstage
        self.gpcnum = len(self.gpcs)
        try:
            self.gpcincolnum = max([len(gpc['src']) for gpc in self.gpcs])
        except ValueError:
            self.gpcincolnum = 0
        self.gpcinwidth = [len(gpc['src']) for gpc in self.gpcs]
        self.gpcin = [gpc['src'] for gpc in self.gpcs]
        self.gpcout = [gpc['dst'] for gpc in self.gpcs]
        self.gpccost = [gpc['cost'] for gpc in self.gpcs]
        self.initialstage = [self.size for _ in range(self.size)] + \
            [0 for _ in range(self.colnum-self.size)]
        self.gpclimit = max(self.initialstage)
        self.collimit = max(self.initialstage)

def main():
    try:
        gpclist = sys.argv[1]
        size = int(sys.argv[2])
        stagemin = int(sys.argv[3])
        stagemax = int(sys.argv[4])
    except IndexError:
        print(f'Usage: {sys.argv[0]} <gpclist filename> <compressor size> <stagemin> <stagemax>',file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print(f'Failed to parse \'{sys.argv[2]}\'. Compressor size, stagemin and stagemax have to be an integer.',
              file=sys.stderr)
        sys.exit(1)
    raw = open(gpclist,'r').read()
    gpcs = parsegpc.parsegpcs(raw)
    prob = square(size, gpcs, stagemin, stagemax, FINALSTAGE)
    prob.dump()

if __name__ == "__main__":
    main()
