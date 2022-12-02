#!/usr/bin/env python3

import re
import sys

def parse(line):
    m = re.search(r'\((.+);([0-9]+)\) (.)', line)
    src = list(reversed(list(map(int, m.group(1).split(',')))))
    dst = int(m.group(2))
    cost = int(m.group(3))
    return {'src':src, 'dst':dst, 'cost':cost}

def parsegpcs(raw):
    lines = raw.split('\n')
    gpcs = []
    for line in lines:
        if line != '':
            gpcs.append(parse(line))
    return gpcs

def gensimplegpc(gpc):
    src = gpc['src']
    dst = gpc['dst']
    tab = '    '
    tablevel = 0
    code = ''
    code += f'module gpc{"".join(list(map(str, src))[::-1])}_{dst}(\n'
    args = []
    for i, s in enumerate(src):
        if s != 0:
            args.append(tab*2+f'input wire [{s-1}:0] src{i}')
    args.append(tab*2+f'output wire [{dst-1}:0] dst')
    code += f',\n'.join(args)+');\n'
    code += tab+f'assign dst[{dst-1}:0] = \n'
    terms = []
    for i, s in enumerate(src):
        if s != 0:
            place = []
            for j in range(s):
                place.append(f'(src{i}[{j}]<<{i})')
            terms.append(tab*2+'+'.join(place))
    code += '+\n'.join(terms) + ';\n'
    code += f'endmodule\n'
    return code
