"""The base nodes in the syntax tree and their identifiers."""


import enum


@enum.unique
class NodeSymbol(enum.Enum):
    START = ('START', False)

    Word = ('Word', True)
    Regester = ('Regester', True)
    Operation = ('Operation', True)

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

    def __init__(self, symbol, *, _do_not_invoke=True):
        assert not _do_not_invoke
        self.symbol = symbol


class Terminal(Node):

    def __init__(self, symbol, string):
        super().__init__(symbol, _do_not_invoke=False)
        self.string = string


class Nonterminal(Node):

    def __init__(self, symbol, children, rule):
        super().__init__(symbol, _do_not_invoke=False)
        self._children = children
        self.rule = rule

    def child(self, pos):
        return self._children[pos]
