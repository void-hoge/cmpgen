#!/usr/bin/env python3

import random
import math
from cmpsim import cmpsim

class pipelined_cmpcodegen(cmpsim):
    def __init__(self, rawtxt):
        super().__init__(rawtxt)
        self.tab = '   '
        self.modulename = 'compressor'

    def gen_vars(self):
        self.maxdigit = int(math.log10(self.colnum))+1
        self.srcwires = {col:(f'src{str(col).zfill(self.maxdigit)}', num)
                         for col, num in enumerate(self.initialstage) if num > 0}
        self.dstwires = {col:(f'dst{str(col).zfill(self.maxdigit)}', num)
                         for col, num in enumerate(self.stages[-1]) if num > 0}
        self.stagewires = {col: (f'stage{str(col).zfill(self.maxdigit)}', num)
                           for col, num in enumerate(self.stagepos[-1]) if num > 0}
        self.pipelineregs = {col: (f'pipeline{str(col).zfill(self.maxdigit)}', length-start-end, start)
                             for col, (start, end, length) in enumerate(zip(self.stages[0], self.stages[-1], self.stagepos[-1])) if length-start-end > 0}
        self.clockwire = 'clock'

    def codegen(self):
        self.gen_vars()
        return self.gen_module()

    def gen_module(self, tablevel=0):
        code = ''
        code += self.tab*tablevel + f'module {self.modulename}(\n'
        code += f'{self.tab*(tablevel+2)}input wire {self.clockwire},\n'
        argwires = []
        for col, (name, length) in self.srcwires.items():
            argwires.append(f'input wire [{length-1}:0] {name}')
        for col, (name, length) in self.dstwires.items():
            argwires.append(f'output wire [{length-1}:0] {name}')
        code += self.tab*(tablevel+2)
        code += f',\n{self.tab*(tablevel+2)}'.join(argwires)
        code += '\n'
        code += self.tab*(tablevel+1) + ');\n'

        code += self.gen_stagewire_declarations(tablevel+1)
        code += self.gen_pipelinereg_declarations(tablevel+1)
        code += self.gen_srcwire_assignments(tablevel+1)
        code += self.gen_dststage_assignments(tablevel+1)
        code += self.gen_always_block(tablevel+1)
        code += self.gen_gpc_instantations(tablevel+1)

        code += self.tab*tablevel + 'endmodule\n'
        return code

    def gen_stagewire_declarations(self, tablevel):
        code = ''
        for col, (name, length) in self.stagewires.items():
            code += self.tab*tablevel + f'wire [{length-1}:0] {name};\n'
        return code

    def gen_pipelinereg_declarations(self, tablevel):
        code = ''
        for col, (name, length, offset) in self.pipelineregs.items():
            code += self.tab*tablevel + f'reg [{length-1}:0] {name};\n'
        return code

    def gen_srcwire_assignments(self, tablevel):
        code = ''
        for col, (srcname, srclen) in self.srcwires.items():
            stagename, _ = self.stagewires[col]
            code += self.tab*tablevel + f'assign {stagename}[{srclen-1}:0] = {srcname};\n'
        return code

    def gen_dststage_assignments(self, tablevel):
        code = ''
        for col, (begin, end) in enumerate(zip(self.stagepos[-2], self.stagepos[-1])):
            dstname, _ = self.dstwires[col]
            stagename, _ = self.stagewires[col]
            code += self.tab*tablevel + f'assign {dstname} = {stagename}[{end-1}:{begin}];\n'
        return code

    def get_gpcname(self, gpcin, gpcout):
        return f'gpc{"".join(map(str, gpcin[::-1]))}_{gpcout}'

    def get_gpcsrc(self, gpcsrc):
        src = []
        for wires in gpcsrc:
            if not wires:
                continue
            wireband = []
            for wire in wires:
                if wire is None:
                    wireband.append('1\'h0')
                else:
                    place = wire['place']
                    pos = wire['pos']
                    if pos < self.stages[0][place]:
                        # stage 0
                        name, length = self.stagewires[place]
                        wireband.append(f'{name}[{pos}]')
                    else:
                        # stage 1~ (pipeline regs)
                        name, length, offset = self.pipelineregs[place]
                        wireband.append(f'{name}[{pos-offset}]')
            src.append(f'{{{", ".join(wireband)}}}')
        return src

    def get_gpcdst(self, gpcdst):
        dst = []
        for wire in gpcdst:
            if wire is None:
                break
            place = wire['place']
            pos = wire['pos']
            name, length = self.stagewires[place]
            dst.append(f'{name}[{pos}]')
        return f'{{{",".join(dst[::-1])}}}'

    def gen_gpc_instantations(self, tablevel):
        code = ''
        for idx, inst in enumerate(self.instructions):
            gpcin = inst['gpcin']
            gpcout = inst['gpcout']
            srcwires = inst['src']
            dstwires = inst['dst']
            gpcname = self.get_gpcname(gpcin, gpcout)
            code += self.tab*tablevel + f'{gpcname} {gpcname}_{idx}(\n'
            code += self.tab*(tablevel+1)
            argwires = self.get_gpcsrc(srcwires)
            argwires.append(self.get_gpcdst(dstwires))
            code += f',\n{self.tab*(tablevel+1)}'.join(argwires)
            code += f'\n{self.tab*tablevel});\n'
        return code

    def gen_always_block(self, tablevel):
        code = ''
        code += self.tab*tablevel + f'always @(posedge {self.clockwire}) begin\n'
        for col, (regname, reglen, offset) in self.pipelineregs.items():
            wirename, wirelen = self.stagewires[col]
            code += self.tab*(tablevel+1)
            code += f'{regname} <= {wirename}[{offset+reglen-1}:{offset}];\n'
        code += self.tab*tablevel + 'end\n'
        return code

class pipelined_cmpbehavioraltestgen(pipelined_cmpcodegen):
    def __init__(self, rawtxt):
        super().__init__(rawtxt)
        self.testmodulename = 'behavioral_tester'

    def gen_vars(self):
        super().gen_vars()
        self.testsrcregs = self.srcwires
        self.testdstwires = self.dstwires
        self.sumlen = self.colnum + math.ceil(math.log2(self.finalstage))
        self.srcsum = ('srcsum', self.sumlen)
        self.dstsum = ('dstsum', self.sumlen)
        self.testwire = 'test'
        self.srcsumlist = 'srcsumlist'
        self.cmpinstname = 'main_cmp'

    def codegen(self):
        self.gen_vars()
        return self.gen_module()

    def gen_module(self, tablevel=0):
        code = ''
        code += self.tab*tablevel + f'module {self.testmodulename}();\n'

        code += self.gen_srcreg_declarations(tablevel+1)
        code += self.gen_dstwire_declarations(tablevel+1)
        code += self.gen_testvar_declarations(tablevel+1)
        code += self.gen_srcsum_assignment(tablevel+1)
        code += self.gen_dstsum_assignment(tablevel+1)
        code += self.gen_testwire_assignment(tablevel+1)
        code += self.gen_compressor_instantiation(tablevel+1)
        code += self.gen_test_block(tablevel+1)
        code += self.gen_test_sequence_block(tablevel+1)
        
        code += self.tab*tablevel + 'endmodule\n'
        return code

    def gen_srcreg_declarations(self, tablevel):
        code = ''
        for col, (name, length) in self.testsrcregs.items():
            code += self.tab*tablevel + f'reg [{length-1}:0] {name};\n'
        return code

    def gen_dstwire_declarations(self, tablevel):
        code = ''
        for col, (name, length) in self.testdstwires.items():
            code += self.tab*tablevel + f'wire [{length-1}:0] {name};\n'
        return code

    def gen_testvar_declarations(self, tablevel):
        code = ''
        srcname, srclen = self.srcsum
        code += self.tab*tablevel + f'wire [{srclen-1}:0] {srcname};\n'
        dstname, dstlen = self.dstsum
        code += self.tab*tablevel + f'wire [{dstlen-1}:0] {dstname};\n'
        code += self.tab*tablevel + f'reg {self.clockwire};\n'
        code += self.tab*tablevel + f'reg [{srclen-1}:0] {self.srcsumlist} [{self.stagemin-3}:0];\n'
        code += self.tab*tablevel + f'wire {self.testwire};\n'
        
        return code

    def gen_srcsum_assignment(self, tablevel):
        code = ''
        name, length = self.srcsum
        code += self.tab*tablevel + f'assign {name} =\n'
        terms = []
        for col, (name, length) in self.testsrcregs.items():
            for i in range(length):
                terms.append(f'({name}[{i}] << {col})')
        code += self.tab*(tablevel+1)
        code += f' +\n{self.tab*(tablevel+1)}'.join(terms)
        code += ';\n'
        return code

    def gen_dstsum_assignment(self, tablevel):
        code = ''
        name, _ = self.dstsum
        code += self.tab*tablevel + f'assign {name} =\n'
        terms = []
        for col, (name, length) in self.testdstwires.items():
            for i in range(length):
                terms.append(f'({name}[{i}] << {col})')
        code += self.tab*(tablevel+1)
        code += f' +\n{self.tab*(tablevel+1)}'.join(terms)
        code += ';\n'
        return code

    def gen_testwire_assignment(self, tablevel):
        code = ''
        dstname, dstlen = self.dstsum
        code += self.tab*tablevel + f'assign {self.testwire} = {self.srcsumlist}[{self.stagemin-3}] == {dstname};\n'
        return code

    def gen_compressor_instantiation(self, tablevel):
        code = ''
        code += self.tab*tablevel + f'{self.modulename} {self.cmpinstname}('
        args = [self.clockwire]
        for col, (name, length) in self.testsrcregs.items():
            args.append(name)
        for col, (name, length) in self.testdstwires.items():
            args.append(name)
        code += ', '.join(args)
        code += ');\n'
        return code

    def gen_test_block(self, tablevel):
        code = ''
        dstname, length = self.dstsum
        code += self.tab*tablevel + f'always @(negedge {self.clockwire}) begin\n'
        srcname, length = self.srcsum
        code += self.tab*(tablevel+1) + f'{self.srcsumlist}[0] <= {srcname};\n'
        for i in range(1, self.stagemin-2):
            code += self.tab*(tablevel+1) + f'{self.srcsumlist}[{i}] <= {self.srcsumlist}[{i-1}];\n'
        code += self.tab*(tablevel+1) + f'$display(\"src: 0x%x, dst: 0x%x, test: %b\", {srcname}, {dstname}, {self.testwire});\n'
        code += self.tab*tablevel + 'end\n'
        return code

    def gen_test_sequence_block(self, tablevel, iteration=10):
        code = ''
        code += self.tab*tablevel + 'initial begin\n'
        code += self.tab*(tablevel+1) + f'{self.clockwire} <= 0;\n'
        code += self.tab*(tablevel+1) + '#1;\n'
        for col, (name, length) in self.testsrcregs.items():
            code += self.tab*(tablevel+1) + f'{name} <= {length}\'h{0:x};\n'
        code += self.tab*(tablevel+1) + f'{self.clockwire}<= 1;\n'
        code += self.tab*(tablevel+1) + '#1;\n'
        code += self.tab*(tablevel+1) + f'{self.clockwire} <= 0;\n'
        code += self.tab*(tablevel+1) + '#1;\n'
        for col, (name, length) in self.testsrcregs.items():
            code += self.tab*(tablevel+1) + f'{name} <= {length}\'h{(1<<length)-1:x};\n'            
        for _ in range(iteration):
            code += self.tab*(tablevel+1) + f'{self.clockwire} <= 1;\n'
            code += self.tab*(tablevel+1) + '#1;\n'
            code += self.tab*(tablevel+1) + f'{self.clockwire} <= 0;\n'
            code += self.tab*(tablevel+1) + '#1;\n'
            for col, (name, length) in self.testsrcregs.items():
                code += self.tab*(tablevel+1) + f'{name} <= {length}\'h{random.randint(0, (1<<length)-1):x};\n'
        for _ in range(self.stagemin-1):
            code += self.tab*(tablevel+1) + f'{self.clockwire} <= 1;\n'
            code += self.tab*(tablevel+1) + '#1;\n'
            code += self.tab*(tablevel+1) + f'{self.clockwire} <= 0;\n'
            code += self.tab*(tablevel+1) + '#1;\n'
        code += self.tab*tablevel + 'end\n'
        return code

def main():
    random.seed(a=0)
    rawtxt = ''
    while True:
        try:
            rawtxt += input() + '\n'
        except EOFError:
            break
    codegen = pipelined_cmpcodegen(rawtxt)
    print(codegen.codegen())
    testgen = pipelined_cmpbehavioraltestgen(rawtxt)
    print(testgen.codegen())

if __name__ == '__main__':
    main()
