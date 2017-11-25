#!/usr/bin/env python3


import argparse
from pathlib import Path


def main(argv=None):
    args = parse_args(argv)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description='Recuriter is a Von Neumann Standing Compiler'
    parser.add_argument('source', help='The source file to assemble.')
    parser.add_argument('output', help='The output file to write to.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main()
