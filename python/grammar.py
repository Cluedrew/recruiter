"""Definition of language's actual grammer."""


__all__ = [
    'iter_terminals_from_str',
    ]


import enum
import re

import cfg
from op_code import OPERATIONS
from slr1 import generate_action_table


@enum.unique
class VNSSymbols(cfg.SymbolEnum):
    START = ('START', False)
    INSTRUCTION = ('INSTRUCTION', False)
    OPERATION = ('OPERATION', False)
    ARGS = ('ARGS', False)
    ARG_TAIL = ('ARG_TAIL', False)
    ARGUMENT = ('ARGUMENT', False)

    Register = ('Register', True)
    Operation = ('Operation', True)
    Integer = ('Integer', True)
    Identifier = ('Identifier', True)
    Comma = ('Comma', True)

    _EOF = ('_EOF', None)


def iter_terminals_from_str(string):
    for part in string.split():
        while part:
            symbol, text, part = remove_terminal_from_str(part)
            yield symbol, text


def remove_terminal_from_str(string):
    for symbol, pattern in TERMINAL_PATTERNS:
        match = pattern.match(string)
        if match:
            return symbol, match.group(), string[match.end():]
    raise Exception('Could not match', string)


TERMINAL_PATTERNS = [
    (VNSSymbols.Register, re.compile('\\br([12][0-9]|3[01]|[0-9])\\b')),
    (VNSSymbols.Operation, re.compile('|'.join(OPERATIONS), re.IGNORECASE)),
    (VNSSymbols.Integer, re.compile('[0-9]+')),
    (VNSSymbols.Identifier, re.compile('[_a-zA-Z][_a-zA-Z0-9]*')),
    (VNSSymbols.Comma, re.compile(',')),
    ]


class VNSRules(cfg.RuleListing, symbol_type=VNSSymbols):
    LINE = 'START', ['OPERATION', 'ARGS']
    NO_ARG = 'ARGS', []
    ONE_ARG = 'ARGS', ['ARGUMENT']
    MULTI_ARG = 'ARGS', ['ARGUMENT', 'ARG_TAIL']
    MORE_ARGS = 'ARG_TAIL', ['Comma', 'ARGUMENT', 'ARG_TAIL']
    ARG_REGISTER = 'ARGUMENT', ['Register']
    ARG_IMEDIATE = 'ARGUMENT', ['Integer']
    ARG_IDENTIFIER = 'ARGUMENT', ['Identifier']


_action_table = generate_action_table(VNSSymbols, VNSSymbols.START, VNSRules)


def parse_string(string):
    iter = iter_terminals_from_str(string)
    return cfg.parse(VNSSymbols, _action_table, iter)
