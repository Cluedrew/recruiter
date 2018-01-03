#!/usr/bin/env python3


# TODO:
# I. Proof of Concept: Instructions with Regesters and Litterals.
# 1. Tokenization: Text to Tokens.
# 2. Grammer: Convert things into a Parse Tree
# 3. IO: Read from source, print to output
# II. Minimum Viable Product: Labels and Sections
# 1. "Instructions Printed" Counter.
# 2. Label look-up
# 2a. Scoped store for each section.
# 2b. Forward reference resolution. (mark and backtrack?)
# 3. Wrap as, feeding it a /tmp file with the processed code.
# III. Basic Replacement: "Here", Includes, Assignments and Math
# 1. Interprate here as an integer.
# 2. Support include directive.
# 2a. Parsing might require a special case to get full names.
# 2b. Splice in the code from that file.
# 3. Add assignment store along side labels.
# 4. Read and evaluate arthmatic expressions
# IV. Full Replacement: Error Messages and Imediate Substution.
# 1. Tag internal structures with source text information.
# 2. Determaine recoverable errors and how to recover.
# 3. Imediate Substution, filling in 'I' when used and check for conflicts.
# 4. Validate command input formats.
# V. New Features:
# I have ideas, but it is a bit far off right now.
# 1. Dot values, special values like "." or ".section"

# I'm just thinking about the main loop.
# Setup:
#   Create a store for definitions and any global settings.
#   Parse and handle command line arguments.
#   Open the main source file.
# Loop:
#   Get a logical line and (possibly recursively) parse it.
#   Instructions should be dumped into the approprate section.
#   Defines (labels and assignments) get added to the global definitions.
#   Includes add to the stack of files to read from.
# Cleanup:
#   Writing to the executable probably has to wait for now, to make sure
#   each section is full and all forward references are filled. Plus the
#   typical cleanup.


import argparse

from lines import SourceFile


def main(argv=None):
    args = parse_args(argv)
    # I'm going to need a stack of these.
    for line in SourceFile(args.source):
        print('New line')
        for terminal in line:
            print('', terminal.symbol, terminal.text)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description='Recuriter is a Von Neumann Standing Compiler')
    parser.add_argument('source', help='The source file to assemble.')
    parser.add_argument('output', help='The output file to write to.')
    # For II) parser.add_argument('--as', help='Underlying compiler.')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main()
