"""Context-Free Grammar Parser."""

# New Possible Design:
# cfg - Central logic and shared class definitions.
# slr1 - ActionTable generation and all its support code.
#   from cfg import ActionTable, Rule
# grammar - Grammar definition and wrapper for external code.
#   from cfg import SymbolEnum, Rule, parse
#   from slr1 import generate_action_table
#   from ... import <might define string to token elsewhere>


from collections import namedtuple
from collections.abc import Mapping

from node import Nonterminal


# TODO: On Python 3.6: typing.NamedTuple is prettier and typed.
Rule = namedtuple('Rule', ['head', 'children'])


def parse(action_table, token_iterable):
    stack = ParsingStack()
    current_state = action_table.starting_state
    stream = PushBackStream(token_iterable)

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
    assert next(stream, None) is None
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

    return state, Nonterminal(map(lambda x: x[1], reversed(popped)))


class ActionTable(Mapping):
    """An action table stores shift/reduce rules."""

    def __init__(self):
        self._data = {}
        self.starting_state = 0

    def add_action(self, state, symbol, action):
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

    def __init__(self, iterable):
        self._iter = iterable
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
