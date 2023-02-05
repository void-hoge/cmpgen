#!/usr/bin/env python3

import sys
import re
import random
import copy

class cmpsim:
    def __init__(self):
        self.stagemax = 0
        self.colmax = 0
        self.gpcs = []
        self.wirelen = []
        self.stages = []
        self.instructions = []
        self.stagepos = []

    def parse(self):
        '''Recieves and parses circuit configuration from standard input.
        Circuit configuration is standard output of cmpgen.
        '''
        tmp = input()
        m = re.search(r'STAGENUM: ([0-9]+)', tmp)
        self.stagemax = int(m.group(1))
        self.gpcs = [[] for _ in range(self.stagemax-1)]
        self.stages = [[] for _ in range(self.stagemax)]
        tmp = input()
        m = re.search(r'COLNUM: ([0-9]+)', tmp)
        self.colmax = int(m.group(1))
        for i in range(self.stagemax):
            tmp = input()
            m = re.search(r'stage {}: (.+)'.format(i), tmp)
            self.stages[i] = list(list(map(int, m.group(1).split())))
        self.stagepos = [[0 for _ in range(self.colmax)]
                         for _ in range(self.stagemax)]
        for i in range(self.stagemax):
            for j in range(self.colmax):
                self.stagepos[i][j] = sum([self.stages[k][j]
                                           for k in range(i)])
        self.wirelen = [sum([self.stages[i][j] for i in range(self.stagemax)])
                        for j in range(self.colmax)]
        for i in range(self.stagemax-1):
            tmp = input()
            m = re.search(r'stage {} -> {}: ([0-9]+)'.format(i, i+1), tmp)
            src = i
            dst = i+1
            count = int(m.group(1))
            for j in range(count):
                tmp = input()
                m = re.search(r' +\(col: ([0-9]+), num: ([0-9]+), GPC(.+)\)', tmp)
                col = int(m.group(1))
                num = int(m.group(2))
                gpc = m.group(3)
                m = re.search(r'\((.+);([0-9]+)\)', gpc)
                src = {i:int(numstr) for i, numstr in
                       enumerate(m.group(1).split(',')[::-1])}
                dst = int(m.group(2))
                self.gpcs[i].append({'col':col, 'num':num, 'src':src, 'dst':dst})

    def dump(self, ost=sys.stderr):
        for inst in self.instructions:
            src = inst['src']
            dst = inst['dst']
            gpc = inst['gpc']
            print(f'({",".join(map(str,list(gpc["src"].values())[::-1]))};{gpc["dst"]})',
                  file=ost)
            print('    src', file=ost)
            for i, nums in src.items():
                if nums != []:
                    print(f'        {i}: {nums}', file=ost)
            print('    dst', file=ost)
            for i, nums in dst.items():
                if nums != []:
                    print(f'        {i}: {nums}', file=ost)

    def build(self):
        '''Generates a sequence of instructions from the parsed information.
        The instructions stored in the self.instructions.
        '''
        for stg, gpcs in enumerate(self.gpcs):
            srcpos = copy.deepcopy(self.stagepos[stg])
            dstpos = copy.deepcopy(self.stagepos[stg+1])
            for gpc in gpcs:
                col, num, src, dst =\
                    gpc['col'], gpc['num'], gpc['src'], gpc['dst']
                for idx in range(num):
                    srcwires = {i: [] for i in range(self.colmax)}
                    dstwires = {i: [] for i in range(self.colmax)}
                    for i, num in src.items():
                        place = i+col
                        if place >= self.colmax:
                            break
                        srcwires[place] = [srcpos[place]+j
                                          for j in range(num)
                                          if srcpos[place]+j <
                                          self.stagepos[stg+1][place]]
                        srcpos[place] += len(srcwires[place])
                    for i in range(dst):
                        if col+i >= self.colmax:
                            break
                        dstwires[col+i].append(dstpos[col+i])
                        dstpos[col+i]+=1
                    self.instructions.append({'src':srcwires, 'dst':dstwires,
                                              'gpc':{'src':src, 'dst':dst}})

    def simulate(self, src):
        '''Simulates the operation of the circuit from the generated instruction sequence and the SRC.
        Returns the final stage of the compressor as the same format as as SRC.
        '''
        wire = [[0 for _ in range(self.wirelen[i])] for i in range(self.colmax)]
        for i in range(self.colmax):
            wire[i][0:len(src[i])] = src[i]
        for inst in self.instructions:
            gsrc = inst['src']
            gdst = inst['dst']
            total = 0
            for i in range(self.colmax):
                total += sum([wire[i][j] for j in gsrc[i]
                              if j < self.wirelen[i]])<<i
            dstbinlist = self.getbinlist(total, self.colmax)
            for i in range(self.colmax):
                if len(gdst[i]) != 0:
                    pos = gdst[i][0]
                    wire[i][pos] = dstbinlist[i]
        dst = {i:[] for i in range(self.colmax)}
        for i in range(self.colmax):
            dst[i] = wire[i][self.wirelen[i]-self.stages[self.stagemax-1][i]:self.wirelen[i]]
        return dst

    def getbinlist(self, num, width):
        '''Returns binary list of NUM width of WIDTH.
        '''
        result = []
        for i in range(width):
            if num&(1<<i)==0:
                result.append(0)
            else:
                result.append(1)
        return result

    def test(self):
        '''Generates the first stage SRC of the compressor randomly and execute the self.simulate.
        Returns a tuple of correct and simulated sum.
        '''
        src = {i:[] for i in range(self.colmax)}
        srctotal = 0
        for i in range(self.colmax):
            num = random.randint(0, (1<<self.stages[0][i])-1)
            src[i] = self.getbinlist(num, self.stages[0][i])
            srctotal += sum(src[i])<<i
        dst = self.simulate(src)
        dsttotal = 0
        for i in range(self.colmax):
            dsttotal += sum(dst[i])<<i
        return (srctotal, dsttotal)

    def randomtest(self, iteration):
        '''Executes self.test() ITERATION times and returns True if the all CORRECT equal to simulated sum.
        '''
        for i in range(iteration):
            correct, simulate = self.test()
            print(f'correct: {correct}, simulate: {simulate}', file=sys.stderr)
            if correct != simulate:
                return False
        return True
