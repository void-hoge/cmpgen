#!/usr/bin/env python3

import sys
import re
import random
import copy

class compressor:
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

    def emulate(self, src):
        '''Emulates the operation of the circuit from the generated instruction sequence and the SRC.
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
        '''Generates the first stage SRC of the compressor randomly and execute the self.emulate.
        Returns a tuple of correct and emulated sum.
        '''
        src = {i:[] for i in range(self.colmax)}
        srctotal = 0
        for i in range(self.colmax):
            num = random.randint(0, (1<<self.stages[0][i])-1)
            src[i] = self.getbinlist(num, self.stages[0][i])
            srctotal += sum(src[i])<<i
        dst = self.emulate(src)
        dsttotal = 0
        for i in range(self.colmax):
            dsttotal += sum(dst[i])<<i
        return (srctotal, dsttotal)

    def randomtest(self, iteration):
        '''Executes self.test() ITERATION times and returns True if the all CORRECT equal to emulated sum.
        '''
        for i in range(iteration):
            correct, emulate = self.test()
            print(f'correct: {correct}, emulate: {emulate}', file=sys.stderr)
            if correct != emulate:
                return False
        return True

    def codegen(self):
        self.tab = '    '
        self.modulename = 'compressor'
        return self.gen_module()

    def gen_module(self, tablevel=0):
        '''Generates Verilog code of the compressor module.
        '''
        # beginning of the module
        code = ''
        code += self.tab*tablevel + f'module {self.modulename}(\n'
        # argument wires: inputs and outputs wires
        argwires = []
        for i, num in enumerate(self.stages[0]):
            if num != 0:
                argwires.append(self.tab*(tablevel+1)+f'input wire [{num-1}:0] src{i}')
        for i, num in enumerate(self.stages[-1]):
            if num != 0:
                argwires.append(self.tab*(tablevel+1)+f'output wire [{num-1}:0] dst{i}')
        code += ',\n'.join(argwires)+');\n'

        # calls code generation functions for other parts.
        code += self.gen_declaration(tablevel+1)
        code += self.gen_assign_src(tablevel+1)
        code += self.gen_assign_dst(tablevel+1)
        code += self.gen_gpc_instantiations(tablevel+1)

        # end of module
        code += 'endmodule\n'
        return code

    def gen_declaration(self, tablevel):
        '''Generates declaration of wires.
        '''
        code = ''
        for i, num in enumerate(self.wirelen):
            if num != 0:
                code += self.tab*tablevel + f'wire [{num-1}:0] s{i};\n'
        return code

    def gen_assign_src(self, tablevel):
        '''Generates assignment of initial values of wires.
        '''
        code = ''
        for i, num in enumerate(self.stages[0]):
            if num != 0:
                code += self.tab*tablevel + f'assign s{i}[{num-1}:0] = src{i};\n'
        return code
    
    def gen_assign_dst(self, tablevel):
        '''Generates assignment of dst.
        '''
        code = ''
        for i, (start, height) in enumerate(zip(self.stagepos[-1], self.stages[-1])):
            if height != 0:
                end = start+height-1
                code += self.tab*tablevel + f'assign dst{i} = s{i}[{end}:{start}];\n'
        return code

    def gen_gpc_instantiations(self, tablevel):
        '''Generates instantiation of GPCs from the self.instructions.
        '''
        code = ''
        for i, inst in enumerate(self.instructions):
            src = inst['src']
            dst = inst['dst']
            gpc = inst['gpc']
            gpcname = f'gpc{"".join([str(num) for num in gpc["src"].values()][::-1])}'
            gpcname += f'_{gpc["dst"]}'
            code += self.tab*tablevel
            code += f'{gpcname} {gpcname}_{i}(\n'
            args = []
            initial_place = min([place for place, wires in dst.items() if wires])
            for p, gpcnum in gpc['src'].items():
                if gpcnum == 0:
                    continue
                wires = []
                place = initial_place+p
                if place >= self.colmax:
                    wires.append(f'{gpcnum}\'h0')
                else:
                    srcnums = src[place]
                    for idx in srcnums:
                        wires.append(f's{place}[{idx}]')
                    if len(srcnums) < gpcnum:
                        wires.append(f'{gpcnum-len(srcnums)}\'h0')
                args.append(f'{{{", ".join(wires)}}}')
            wires = []
            for place, nums in dst.items():
                if nums == []:
                    continue
                else:
                    wires.append(f's{place}[{nums[0]}]')
            args.append(f'{{{", ".join(wires[::-1])}}}')
            code += self.tab*(tablevel+1)
            code += f',\n{self.tab*(tablevel+1)}'.join(args)
            code += '\n'
            code += self.tab*tablevel
            code += ');\n'
        return code

    def gen_behavioral_test(self, tablevel=0):
        '''Generates a behavioral test module
        '''
        code = ''
        # beginning of module
        code += self.tab*tablevel+f'module behavioral_tester(output wire[{self.colmax}:0] out);\n'
        # module arguments: compressor argument list
        modargs = []
        # input register declaration
        for i, num in enumerate(self.stages[0]):
            if num != 0:
                code += self.tab*(tablevel+1)+f'reg [{num-1}:0] src{i};\n'
                modargs.append(f'src{i}')
        # output wire declaration
        for i, num in enumerate(self.stages[-1]):
            if num != 0:
                code += self.tab*(tablevel+1)+f'wire [{num-1}:0] dst{i};\n'
                modargs.append(f'dst{i}')
        # sum of inputs(for test)
        code += self.tab*(tablevel+1)+f'wire [{self.colmax}:0] srcsum;\n'
        # sum of outputs(for test)
        code += self.tab*(tablevel+1)+f'wire [{self.colmax}:0] dstsum;\n'
        code += self.tab*(tablevel+1)+f'assign out = dstsum;\n'
        # assign sum of inputs
        code += self.tab*(tablevel+1)+'assign srcsum = '
        srcwires = []
        for i, num in enumerate(self.stages[0]):
            if num != 0:
                for j in range(num):
                    srcwires.append(f'(src{i}[{j}]<<{i})')
        code += f'\n{self.tab*(tablevel+2)} + '.join(srcwires)+';\n'
        # assign sum of outputs
        code += self.tab*(tablevel+1)+'assign dstsum = '
        dstwires = []
        for i, num in enumerate(self.stages[-1]):
            if num != 0:
                for j in range(num):
                    dstwires.append(f'(dst{i}[{j}]<<{i})')
        code += f'\n{self.tab*(tablevel+2)} + '.join(dstwires)+';\n'

        # compressor instantation
        code += self.tab*(tablevel+1)+f'{self.modulename} main_cmp({", ".join(modargs)});\n'

        # configuring wire monitoring
        code += self.tab*(tablevel+1)+'initial begin\n'
        code += self.tab*(tablevel+2)+'$monitor("%x => %x", srcsum, dstsum);\n'
        code += self.tab*(tablevel+1)+'end\n'

        # signal generation for testing
        code += self.tab*(tablevel+1)+'initial begin\n'
        src = {i:[] for i in range(self.colmax)}
        for i in range(20):
            code += self.tab*(tablevel+2)+f'#{i}\n'
            for j, num in enumerate(self.stages[0]):
                if num != 0:
                    rn = random.randint(0,(1<<num)-1)
                    src[j] = self.getbinlist(rn, num)
                    code += self.tab*(tablevel+2)+f'src{j}<={num}\'h{rn:x};\n'
            srctot = 0
            for i in range(self.colmax):
                srctot += sum(src[i])<<i
                dst = self.emulate(src)
                dsttot = 0
            for i in range(self.colmax):
                dsttot += sum(dst[i])<<i
        code += self.tab*(tablevel+1)+'end\n'

        # end of module
        code += self.tab*tablevel+'endmodule\n'
        return code

    def gen_implement_test(self, tablevel=0):
        '''Generate a implement test moudle using shift registers.
        This module only supports N by N square inputs.
        '''
        code = ''
        code += self.tab*tablevel+f'module implment_tester(input wire clk,\n'
        N = self.stages[0][0]
        code += self.tab*(tablevel+2)+f'input wire [{N-1}:0]src,\n'
        code += self.tab*(tablevel+2)+f'output wire[{self.colmax-1}:0] dstfirst, dstsecond);\n'
        modargs = []
        for i in range(N):
            code += self.tab*(tablevel+1)+f'reg [{N-1}:0] src{i};\n'
            modargs.append(f'src{i}')
        for i in range(self.colmax):
            code += self.tab*(tablevel+1)+f'wire [1:0] dst{i};\n'
            modargs.append(f'dst{i}')
        dstfirst = [f'dst{i}[0]' for i in range(self.colmax)]
        dstsecond = [f'dst{i}[1]' for i in range(self.colmax)]
        code += self.tab*(tablevel+1)+\
            f'assign dstfirst = {{{", ".join(dstfirst)}}};\n'
        code += self.tab*(tablevel+1)+\
            f'assign dstsecond = {{{", ".join(dstsecond)}}};\n'
        code += self.tab*(tablevel+1)+f'{self.modulename} main_cmp({", ".join(modargs)});\n'
        
        code += self.tab*(tablevel+1)+f'initial begin\n'
        for i in range(N):
            code += self.tab*(tablevel+2)+f'src{i} = 0;\n'
        code += self.tab*(tablevel+1)+f'end\n'

        code += self.tab*(tablevel+1)+'integer i;\n'
        code += self.tab*(tablevel+1)+'always @(posedge clk) begin\n'
        for i in range(N):
            code += self.tab*(tablevel+2)+f'src{i}[0] <= src[{i}];\n'
        code += self.tab*(tablevel+2)+f'for (i = {N}; i > 0; i = i-1) begin\n'
        for i in range(N):
            code += self.tab*(tablevel+3)+f'src{i}[i] <= src{i}[i-1];\n'
        code += self.tab*(tablevel+2)+f'end\n'
        
        code += self.tab*(tablevel+1)+'end\n'
        
        code += self.tab*tablevel+f'endmodule\n'
        return code

def main():
    #random.seed(a=0)
    emulator = compressor()
    emulator.parse()
    emulator.build()
    print('PASS' if emulator.randomtest(20) else 'FAIL', file=sys.stderr)
    #emulator.dump()
    print(emulator.codegen())
    # if you do not need testmodule, just commentout the next lines.
    #print(emulator.gen_implement_test())
    print(emulator.gen_behavioral_test())

if __name__ == '__main__':
    main()
