#!/usr/bin/env python3

import sys
import math
import parsegpc

class problem:
    def __init__(self):
        self.order = [
            'stagemin',
            'stagemax',
            'colnum',
            'finalstage',
            'gpcnum',
            'gpcincolnum',
            'gpcinwidth',
            'gpcin',
            'gpcout',
            'gpccost',
            'initialstage',
            'gpclimit',
            'collimit',
        ]
        self.size = 0
        self.gpcs = []
        self.stagemin = 2
        self.stagemax = 2
        self.colnum = 0
        self.finalstage = 2
        self.gpcnum = 0
        self.gpcincolnum = 0
        self.gpcinwidth = []
        self.gpcin = []
        self.gpcout = []
        self.gpccost = []
        self.initialstage = []
        self.gpclimit = 0
        self.collimit = 0

    def dump(self, ost=sys.stdout):
        for content in self.order:
            val = getattr(self, content, None)
            if val != None:
                print(f'{content}: ', file=sys.stderr, end='')
                sys.stderr.flush()
                print(f'{val}', file=ost)
                ost.flush()
            else:
                print(f'{content} is not defined.', file=sys.stderr)
                sys.exit(1)

    def parse(self, raw):
        lines = raw.split('\n')
        values = ''
        for line in lines:
            if line == '':
                continue
            values += line.replace(' ', '')+','
        values = values.replace(',,', ',')
        values = values[:-1]
        variables = ','.join([f'self.{content}' for content in self.order])
        expr = variables + '=' + values
        exec(expr)
        self.gpcs = self.gengpcs()

    def gengpcs(self):
        gpcs = []
        for i in range(self.gpcnum):
            src = self.gpcin[i]
            dst = self.gpcout[i]
            cost = self.gpccost[i]
            gpcs.append({'src':src, 'dst':dst, 'cost':cost})
        return gpcs
