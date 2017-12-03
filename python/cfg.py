"""Context-Free Grammar Parser."""

from collections import namedtuple
from collections.abc import Mapping
import enum
import itertools


class SymbolEnum(enum.Enum):

    def __new__(cls, name, is_terminal):
        obj = object.__new__(cls)
        obj._value_ = name
        # TODO: Maybe story a more general 'kind'
        obj._is_terminal = is_terminal
        return obj

    # TODO: __init_subclass__ to add a hidden _EOF and
    # check uniqueness would be great.

    def is_terminal(self):
        return self._is_terminal is True

    def is_nonterminal(self):
        return self._is_terminal is False

    def __repr__(self):
        return '<{}.{}: {!r}>'.format(
            self.__class__.__name__, self.name, self._is_terminal)


# TODO: On Python 3.6: typing.NamedTuple is prettier and typed.
Rule = namedtuple('Rule', ['head', 'children'])


class Node:

    def __init__(self, symbol):
        self.symbol = symbol


class Terminal(Node):

    def __init__(self, symbol, text):
        super().__init__(symbol)
        self.text = text

    def __eq__(self, other):
        if isinstance(other, Terminal):
            return self.symbol == other.symbol and self.text == other.text
        return NotImplemented

    def __repr__(self):
        return 'Terminal(symbol={!r}, text={!r})'.format(
            self.symbol, self.text)


class Nonterminal(Node):

    def __init__(self, symbol, children, rule=None):
        super().__init__(symbol)
        self.children = children
        if rule is None:
            rule = Rule(symbol, map(lambda child: child.symbol, children))
        self.rule = rule

    def __repr__(self):
        return 'Nonterminal(symbol={!r}, children=<...>, rule={!r})'.format(
            self.symbol, self.rule)


def parse(action_table, terminal_iterable, eof_symbol):
    stack = ParsingStack()
    current_state = action_table.starting_state
    stream = PushBackStream(terminal_iterable, eof_symbol)

    for token in stream.in_place():
        action = action_table[current_state, token]
        if 'shift' == action.kind:
            stack.push(current_state, next(stream))
            current_state = action.data
        elif 'reduce' == action.kind:
            stream.push_back(token)
            current_state, new_node = preform_reduce(stack, action.data)
            stream.push_back(new_node)
        elif 'done' == action.kind:
            break
    else:
        raise Exception('Ran out of input symbols.')
    if stack:
        raise AssertionError('Extra symbols on the stack.')
    final_node = next(stream)
    assert next(stream).symbol == eof_symbol
    return final_node


def preform_reduce(stack, rule):
    popped = []
    for target_symbol in reversed(rule.children):
        if stack.peek_node().symbol == target_symbol:
            popped.append(stack.pop())
        else:
            # TODO: Better error messages and recovery.
            # This should only ever be an internal error though.
            raise AssertionError()
    state = popped[-1][0]
    node = Nonterminal(rule.head, map(lambda x: x[1], reversed(popped)), rule)
    return (state, node)


class ActionTable(Mapping):
    """An action table stores shift/reduce rules."""

    def __init__(self):
        self._data = {}
        self.starting_state = 0

    def __setitem__(self, key, value):
        state, symbol = key
        section = self._data.setdefault(state, {})
        if symbol in section:
            raise Exception('Conflict found:', state, symbol)
        section[symbol] = action

    def __getitem__(self, key):
        state, symbol = key
        try:
            return self._data[state][symbol]
        except KeyError as error:
            raise KeyError(state, symbol) from error

    def __len__(self):
        sum = 0
        for value in self._data.values():
            sum += len(value)
        return sum

    def __iter__(self):
        yield from map(lambda pair: pair[0], self.items())

    def items(self):
        for state, value in self._data.items():
            for symbol, rule in value.items():
                yield (state, symbol), rule


class Action:

    def __init__(self, kind, data):
        self.kind = kind
        self.data = data

    @classmethod
    def shift(cls, to_state):
        return cls('shift', to_state)

    @classmethod
    def reduce(cls, rule):
        return cls('reduce', rule)

    @classmethod
    def done(cls):
        return cls('done', None)


class ParsingStack:

    def __init__(self):
        self._data = []

    def push(self, state, node):
        self._data.append((state, node))

    def peek_state(self):
        return self._data[-1][0]

    def peek_node(self):
        return self._data[-1][1]

    def pop(self):
        return self._data.pop()

    def __len__(self):
        return len(self._data)


class PushBackStream:

    def __init__(self, iterable, eof_symbol):
        self._iter = itertools.chain(iterable, [Node(eof_symbol)])
        self._back = []

    def __iter__(self):
        return self

    def __next__(self):
        if self._back:
            return self._back.pop()
        else:
            return next(self._iter)

    def push_back(self, value):
        self._back.append(value)

    def in_place(self):
        yield from self._in_place_back()
        for value in self._iter:
            self.push_back(value)
            yield from self._in_place_back()

    def _in_place_back(self):
        while self._back:
            yield self._back[-1]
