#!/usr/bin/env python3

from solution import solution

def main():
    raw = ''
    while True:
        try:
            raw += input() + '\n'
        except EOFError:
            break
    sol = solution(raw)
    print(sol.codegen())

if __name__ == '__main__':
    main()
