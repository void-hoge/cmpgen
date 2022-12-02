#!/usr/bin/env python3

import sys
import math
import re
import parsegpc
from problem import problem

class solution(problem):
    def __init__(self, raw):
        match = re.search(r'elapsed: \[.+\]', raw)
        prob, sol = raw.split(match.group(0))
        super().__init__()
        super().parse(prob)
        if self.stagemax != self.stagemin:
            print('Invalid input. STAGEMIN and STAGEMAX must be a same values.')
        self.parse(sol)

    def parse(self, raw):
        lines = raw.split('\n')
        self.gpcusage = [[[0 for _ in range(self.gpcnum)] for _ in range(self.colnum)] for _ in range(self.stagemin-1)]
        self.stages = [[0 for _ in range(self.colnum)] for _ in range(self.stagemin)]
        for line in lines:
            vals = line.split()
            if len(vals) == 4:
                s,c,g,n = map(int, vals)
                self.gpcusage[s][c][g] = n
            elif len(vals) == 3:
                s,c,n = map(int, vals)
                self.stages[s][c] = n

    def margegpcs(self, gpcs):
        for gpc in gpcs:
            if gpc not in self.gpcs:
                self.gpcs.append(gpc)
        self.gpcnum = len(self.gpcs)
        self.gpcincolnum = max([len(gpc['src']) for gpc in self.gpcs])
        self.gpcinwidth = [len(gpc['src']) for gpc in self.gpcs]
        self.gpcin = [gpc['src'] for gpc in self.gpcs]
        self.gpcout = [gpc['dst'] for gpc in self.gpcs]
        self.gpccost = [gpc['cost'] for gpc in self.gpcs]
        gpcusage = [[[0 for _ in range(self.gpcnum)] for _ in range(self.colnum)] for _ in range(self.stagemin-1)]
        for s in range(self.stagemin-1):
            for c in range(self.colnum):
                for g in range(self.gpcnum):
                    try:
                        gpcusage[s][c][g] = self.gpcusage[s][c][g]
                    except IndexError:
                        pass
        self.gpcusage = gpcusage

    def dump(self):
        super().dump()
        print('elapsed: []')
        for s, stage in enumerate(self.gpcusage):
            for c, col in enumerate(stage):
                for g, num in enumerate(col):
                    print(s,c,g,num)
        for s, stage in enumerate(self.stages):
            for c, col in enumerate(stage):
                print(s,c,col)

    def codegen(self):
        code = ''
        code += f'STAGENUM: {self.stagemin}\n'
        code += f'COLNUM: {self.colnum}\n'
        for s, stage in enumerate(self.stages):
            code += f'stage {s}:'
            for c, column in enumerate(stage):
                code += f' {column}'
            code += '\n'
        for s, stage in enumerate(self.gpcusage):
            code += f'stage {s} -> {s+1}: '
            cnt = sum([sum([0 if gpc==0 else 1 for gpc in column]) for column in stage])
            code += f'{cnt}\n'
            for c, column in enumerate(stage):
                for g, gpc in enumerate(column):
                    if gpc != 0:
                        code += f'    (col: {c}, num: {gpc}, '
                        code += f'GPC({",".join(list(map(str,self.gpcin[g]))[::-1])};{self.gpcout[g]}))\n'
        total_cost = 0
        for s, stage in enumerate(self.gpcusage):
            for c, column in enumerate(stage):
                for g, gpc in enumerate(column):
                    total_cost += gpc*self.gpccost[g]
        code += f'total cost: {total_cost}\n'
        for g in range(self.gpcnum):
            code += f'GPC({",".join(list(map(str, self.gpcin[g]))[::-1])};{self.gpcout[g]}) '
            count = 0
            cost = 0
            for s in range(self.stagemin-1):
                for c in range(self.colnum):
                    count += self.gpcusage[s][c][g]
                    cost += self.gpcusage[s][c][g]*self.gpccost[g]
            code += f'num: {count}, cost: {cost}\n'
        return code
