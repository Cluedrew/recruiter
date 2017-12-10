"""Definition of language's actual grammer."""


__all__ = [
    ]


import enum
import re

import cfg
from op_code import OPERATIONS
from slr1 import generate_action_table


@enum.unique
class NodeSymbol(cfg.SymbolEnum):
    START = ('START', False)
    INSTRUCTION = ('INSTRUCTION', False)

    Word = ('Word', True)
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
    (NodeSymbol.Register, re.compile('\\br([12][0-9]|3[01]|[0-9])\\b')),
    (NodeSymbol.Operation, re.compile('|'.join(OPERATIONS), re.IGNORECASE)),
    (NodeSymbol.Integer, re.compile('[0-9]+')),
    (NodeSymbol.Identifier, re.compile('[_a-zA-Z][_a-zA-Z0-9]*')),
    (NodeSymbol.Comma, re.compile(',')),
    ]


START = NodeSymbol.START
INSTRUCTION = NodeSymbol.INSTRUCTION
Operation = NodeSymbol.Operation
Register = NodeSymbol.Register
Integer = NodeSymbol.Integer
Comma = NodeSymbol.Comma


S_INST = cfg.Rule(START, (INSTRUCTION,))
INST_OP = cfg.Rule(INSTRUCTION, (Operation,))
INST_OA = cfg.Rule(INSTRUCTION, (Operation, Register))
INST_OAI = cfg.Rule(INSTRUCTION, (Operation, Register, Comma, Integer))
INST_OABC = cfg.Rule(
    INSTRUCTION, (Operation, Register, Comma, Register, Comma, Register))


ALL_RULES = (S_INST, INST_OP, INST_OA, INST_OAI, INST_OABC)


_action_table = None
# generate_action_table(NodeSymbol, NodeSymbol.START, ALL_RULES)


def parse_string(string):
    iter = iter_terminals_from_str(string)
    return cfg.parse(NodeSymbol, _action_table, iter)
