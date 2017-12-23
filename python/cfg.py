"""Context-Free Grammar Parser."""


__all__ = [
    'Action',
    'ActionTable',
    'get_eof_symbol',
    'Node',
    'NonterminalNode',
    'parse',
    'Rule',
    'RuleListing',
    'SymbolEnum',
    'TerminalNode',
    ]


from collections import namedtuple
from collections.abc import Mapping
import enum
import itertools


class SymbolEnum(enum.Enum):

    def __new__(cls, name, symbol_kind):
        obj = object.__new__(cls)
        obj._value_ = name
        obj._symbol_kind = symbol_kind
        return obj

    # TODO: __init_subclass__ to add a hidden _EOF and
    # check uniqueness would be great.

    def is_terminal(self):
        return self._symbol_kind is True

    def is_nonterminal(self):
        return self._symbol_kind is False

    def __repr__(self):
        return '<{}.{}: {!r}>'.format(
            self.__class__.__name__, self.name, self._symbol_kind)


def get_eof_symbol(symbol_enum):
    """Get the End-Of-File symbol for a SymbolEnum."""
    eofs = [symbol for symbol in symbol_enum if symbol._symbol_kind is None]
    return eofs[0]


# TODO: On Python 3.6: typing.NamedTuple is prettier and typed.
Rule = namedtuple('Rule', ['head', 'children'])


# Like Enum, have a dummy so _RuleListingMeta knows if it has been made.
RuleListing = None


class _RuleListingMeta(enum.EnumMeta):

    # Stores the symbol_type of the current RuleListing. As long as we don't
    # have concurrent code loading, it should be fine.
    _current_symbol_type = None

    @classmethod
    def __prepare__(meta, class_name, bases, *, symbol_type=None):
        return super().__prepare__(class_name, bases)

    def __new__(meta, class_name, bases, namespace, *, symbol_type=None):
        if RuleListing is not None and symbol_type is None:
            raise RuntimeError('Must provide symbol_type.')
        else:
            meta._current_symbol_type = symbol_type

        return super().__new__(meta, class_name, bases, namespace)

    def __init__(meta, cls, bases, namespace, *, symbol_type=None):
        super().__init__(cls, bases, namespace)


class RuleListing(Rule, enum.Enum, metaclass=_RuleListingMeta):
    """A convenience class for defining sets of rules.

    If you want to define a immutable set of rules, that all draw from
    the same SymbolEnum subclass (most grammar defintions should). Then
    you can use this to do so.

    class MySymbols(SymbolEnum):
        PLUS = ('PLUS', False)
        NUMBER = ('NUMBER', True)
        _EOF = ('_EOF', None)

    class MyRules(RuleListing, symbol_type=MySymbols):
        ADD = 'PLUS', ['NUMBER', 'NUMBER']

    This is mostly to save explicately calling the Rule constructor and
    going through the symbol_type to access the symbol every time.
    """

    def __new__(cls, head, children):
        symbol_type = type(cls)._current_symbol_type
        return super().__new__(cls,
            symbol_type(head), tuple(map(symbol_type, children)))


class Node:

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return '{}(symbol={!r})'.format(
            self.__class__.__name__, self.symbol)


class TerminalNode(Node):

    def __init__(self, symbol, text):
        super().__init__(symbol)
        self.text = text

    def __eq__(self, other):
        if isinstance(other, TerminalNode):
            return self.symbol == other.symbol and self.text == other.text
        return NotImplemented

    def __repr__(self):
        return '{}(symbol={!r}, text={!r})'.format(
            self.__class__.__name__, self.symbol, self.text)


class NonterminalNode(Node):

    def __init__(self, symbol, children, rule=None):
        super().__init__(symbol)
        self.children = children
        if rule is None:
            rule = Rule(symbol, tuple(child.symbol for child in children))
        self.rule = rule

    def __repr__(self):
        return '{}(symbol={!r}, children=<...>, rule={!r})'.format(
            self.__class__.__name__, self.symbol, self.rule)


def parse(symbol_enum, action_table, base_iterable):
    """Parse in input

    symbol_enum: The SymbolEnum subclass that symbols for the grammar
        are drawn from.
    action_table: ActionTable stating what action to take at any given
        point.
    base_iterable: Produces (symbol, text) pairs for every token in
        the input file.

    return: A Node is the root of all other nodes in input.
    """
    stack = ParsingStack()
    current_state = action_table.starting_state
    eof_symbol = get_eof_symbol(symbol_enum)
    stream = NodeStream(base_iterable, eof_symbol)

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
    node = NonterminalNode(
        rule.head, map(lambda x: x[1], reversed(popped)), rule)
    return (state, node)


class ActionTable(Mapping):
    """An action table stores shift/reduce rules."""

    def __init__(self):
        self._data = {}
        self.starting_state = 0

    def __setitem__(self, key, action):
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

    def __eq__(self, other):
        if not isinstance(other, Action):
            raise TypeError('Not comparable with Action.', other)
        return self.kind == other.kind and self.data == other.data

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


class NodeStream:

    def __init__(self, iterable, eof_symbol):
        self._iter = self._wrap_iter(iterable, eof_symbol)
        self._back = []

    @staticmethod
    def _wrap_iter(iterable, eof_symbol):
        for symbol, text in iterable:
            yield TerminalNode(symbol, text)
        yield Node(eof_symbol)

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
