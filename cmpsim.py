#!/usr/bin/env python3

import random
from copy import copy
from solution import solution

class cmpsim(solution):
    def __init__(self, rawtxt):
        super().__init__(rawtxt)
        self.build()

    def build(self):
        self.remove_unnecessary_wires()
        self.build_stages()
        self.build_gpcs()

    def remove_unnecessary_wires(self):
        currentstagebits = copy(self.initialstage)
        for s, gpcstage in enumerate(self.gpcusage):
            nextstagebits = [0 for _ in range(self.colnum)]
            for c, gpccol in enumerate(gpcstage):
                for g, gpcnum in enumerate(gpccol):
                    if self.gpcout[g] == 1:
                        continue
                    for place, num in enumerate(self.gpcin[g]):
                        try:
                            currentstagebits[c + place] -= num*gpcnum
                        except IndexError:
                            pass
                    for place in range(self.gpcout[g]):
                        try:
                            nextstagebits[c + place] += gpcnum
                        except IndexError:
                            pass
            wireidx = self.gpcout.index(1)
            for place, wirenum in enumerate(currentstagebits):
                if wirenum > 0:
                    nextstagebits[place] += wirenum
                    self.gpcusage[s][place][wireidx] = wirenum
                if wirenum <= 0:
                    self.gpcusage[s][place][wireidx] = 0
            currentstagebits = copy(nextstagebits)
            self.stages[s+1] = copy(nextstagebits)

    def build_stages(self):
        for stage in self.stages:
            for num in stage:
                if num < 0:
                    raise 'invalid stage height detected'
        wirelens = [sum([stage[col] for stage in self.stages])
                    for col in range(self.colnum)]
        for s, length in enumerate(wirelens[::-1]):
            if length == 0:
                for stage in self.stages:
                    stage.pop()
                self.colnum -= 1
            else:
                break
        self.stagepos = [[0 for _ in range(self.colnum)]
                         for _ in range(self.stagemin+1)]
        for s in range(self.stagemin):
            for c in range(self.colnum):
                self.stagepos[s+1][c] = \
                    self.stagepos[s][c] + self.stages[s][c]

    def build_gpcs(self):
        self.instructions = []
        for s, gpcstage in enumerate(self.gpcusage):
            srcpos = copy(self.stagepos[s])
            dstpos = copy(self.stagepos[s+1])
            for c, gpccol in enumerate(gpcstage):
                for g, gpcnum in enumerate(gpccol):
                    for i in range(gpcnum):
                        src = [[None for _ in range(self.gpcin[g][place])]
                               for place in range(self.gpcinwidth[g])]
                        for place in range(self.gpcinwidth[g]):
                            if c+place >= self.colnum:
                                continue
                            maxheight = min(self.gpcin[g][place],
                                            self.stagepos[s+1][c+place]-srcpos[c+place])
                            for num in range(maxheight):
                                src[place][num] = {
                                    'place':c+place,
                                    'pos':srcpos[c+place]+num
                                }
                            srcpos[c+place] += maxheight
                        dst = [None for _ in range(self.gpcout[g])]
                        for place in range(self.gpcout[g]):
                            try:
                                dst[place] = {
                                    'place':c+place,
                                    'pos':dstpos[c+place]
                                }
                                dstpos[c+place] += 1
                            except IndexError:
                                pass
                        self.instructions.append({
                            'gpcin': self.gpcin[g],
                            'gpcout': self.gpcout[g],
                            'src': src,
                            'dst': dst,
                        })

    def int2bin(self, num, width):
        rslt = [0 for _ in range(width)]
        for i in range(width):
            rslt[i] = (num>>i)&1
        return rslt

    def bin2int(self, bits):
        return sum([bit<<p for p, bit in enumerate(bits)])

    def gpcsim(self, srcbits, outwidth):
        num = 0
        for place, bits in srcbits.items():
            num += sum(bits) << place
        return self.int2bin(num, outwidth)

    def simulate(self, srcbits):
        stagebits = {c:[0 for _ in range(self.stagepos[-1][c])]
                     for c in range(self.colnum)}
        for col in range(self.colnum):
            stagebits[col][0:self.initialstage[col]] = srcbits[col]
        for inst in self.instructions:
            gpcsrcbits = {c: [0 for _ in range(num)]
                          for c, num in enumerate(inst['gpcin'])}
            for c, bits in enumerate(inst['src']):
                for idx, bit in enumerate(bits):
                    if bit == None:
                        continue
                    place, pos = bit['place'], bit['pos']
                    gpcsrcbits[c][idx] = stagebits[place][pos]
            gpcdstbits = self.gpcsim(gpcsrcbits, inst['gpcout'])
            for c, bit in enumerate(inst['dst']):
                if bit == None:
                    continue
                place, pos = bit['place'], bit['pos']
                try:
                    stagebits[place][pos] = gpcdstbits[c]
                except IndexError:
                    pass
        return {c: stagebits[c][self.stagepos[-2][c]:self.stagepos[-1][c]] for c in range(self.colnum)}

    def randomtest(self, iteration=20):
        for _ in range(iteration):
            srcbits = {col: [random.randint(0,1)
                             for i in range(self.initialstage[col])]
                       for col in range(self.colnum)}
            srcsum = sum([sum(colbits)<<place for place, colbits in srcbits.items()])
            dstbits = self.simulate(srcbits)
            dstsum = sum([sum(colbits)<<place for place, colbits in dstbits.items()])
            srcstr = f'{srcsum:x}'.zfill(int(self.colnum/4)+1)
            dststr = f'{dstsum:x}'.zfill(int(self.colnum/4)+1)
            print(f'src: 0x{srcstr}, dst: 0x{dststr}')
            if srcsum != dstsum:
                return False
        return True

def main():
    random.seed(a=0)
    rawtxt = ''
    while True:
        try:
            rawtxt += input() + '\n'
        except EOFError:
            break
    sim = cmpsim(rawtxt)
    print('PASS' if sim.randomtest(iteration=1<<10) else 'FAIL')


if __name__ == '__main__':
    main()
