#!/usr/bin/env python3

import sys
import re
import random
import copy
from cmpsim import cmpsim

class cmpcodegen(cmpsim):
    def __init__(self):
        super().__init__()
        self.parse()
        self.build()
        self.tab = '    '
        self.modulename = 'compressor'

    def codegen(self):
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
            code += self.tab*(tablevel+2)+'#10\n'
            for j, num in enumerate(self.stages[0]):
                if num != 0:
                    rn = random.randint(0,(1<<num)-1)
                    src[j] = self.getbinlist(rn, num)
                    code += self.tab*(tablevel+2)+f'src{j}<={num}\'h{rn:x};\n'
            srctot = 0
            for i in range(self.colmax):
                srctot += sum(src[i])<<i
                dst = self.simulate(src)
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
    random.seed(a=0)
    codegen = cmpcodegen()
    print('PASS' if codegen.randomtest(20) else 'FAIL', file=sys.stderr)
    #simulator.dump()
    print(codegen.codegen())
    # if you do not need testmodule, just commentout the following lines.
    #print(codegen.gen_implement_test())
    print(codegen.gen_behavioral_test())

if __name__ == '__main__':
    main()
