
"""The base nodes in the syntax tree and their identifiers.

There are three base node types: Node, Terminal and Nonterminal.
"""

# This has also become a tokenization stratchpad for now.


import enum
import re

from op_code import OPERATIONS


@enum.unique
class NodeSymbol(enum.Enum):
    START = ('START', False)
    INSTRUCTION = ('INSTRUCTION', False)

    Word = ('Word', True)
    Register = ('Register', True)
    Operation = ('Operation', True)
    Integer = ('Integer', True)
    Identifier = ('Identifier', True)
    Comma = ('Comma', True)

    def is_terminal(self):
        return self._is_terminal

    def is_nonterminal(self):
        return not self._is_terminal

    def __new__(cls, name, is_terminal):
        obj = object.__new__(cls)
        obj._value_ = name
        obj._is_terminal = is_terminal
        return obj


class Node:

    def __init__(self):
        if not isinstance(self.symbol, NodeSymbol):
            raise NotImplementedError

    symbol = None


class Terminal(Node):

    def __init__(self, text):
        super().__init__()
        self.text = text
        # You must define _regex on each actual class.
        # TODO: Python 3.6's __init_subclass__ solves this better.
        if not isinstance(self._regex, Terminal._regex_type):
            raise NotImplementedError

    _regex = None
    _regex_type = type(re.compile('-'))

    @classmethod
    def take_from_string(cls, string):
        try:
            match = cls._regex.match(string)
        except AttributeError:
            raise NotImplementedError
        if match:
            return cls(match.group()), string[match.end():]
        return None


class Nonterminal(Node):

    def __init__(self, symbol, children):
        self.symbol = symbol
        super().__init__()
        self._children = children

    def child(self, pos):
        return self._children[pos]


def iter_terminals_from_str(string):
    parts = string.split()
    for part in parts:
        while part:
            token, part = remove_terminal_from_str(part)
            yield token


def remove_terminal_from_str(string):
    for terminal_type in ALL_TERMINALS:
        result = terminal_type.take_from_string(string)
        if result is not None:
            return result
    raise Exception('Could not match', string)


class RegisterTerminal(Terminal):
    """The litterals reserved for regesters."""

    symbol = NodeSymbol.Register
    # This is an exact match, a r[0-9]+ with a range check might give better
    # error message. However we don't really have those yet.
    _regex = re.compile('\br([12][0-9]|3[01]|[0-9])\b')

    def __int__(self):
        return int(self.text[1:])


class OperationTerminal(Terminal):
    """The operations that start off each instruction."""

    symbol = NodeSymbol.Operation
    _regex = re.compile('|'.join(OPERATIONS), re.IGNORECASE)


class IntegerTerminal(Terminal):
    """A raw integer"""

    symbol = NodeSymbol.Integer
    _regex = re.compile('[0-9]+')

    def __int__(self):
        return int(self.text)


class IdentifierTerminal(Terminal):
    """An otherwise not special collection of letters and numbers."""

    symbol = NodeSymbol.Integer
    _regex = re.compile('[_a-zA-Z][_a-zA-Z0-9]*')


class CommaTerminal(Terminal):
    """A comma."""

    symbol = NodeSymbol.Comma
    _regex = re.compile(',')


ALL_TERMINALS = [
    RegisterTerminal,
    OperationTerminal,
    IntegerTerminal,
    IdentifierTerminal,
    CommaTerminal,
    ]
