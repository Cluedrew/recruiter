"""Simple Left/Right Lookahead 1 Action Table Generator."""


__all__ = [
    'generate_action_table',
    ]


from collections import defaultdict, namedtuple

from cfg import (
    Action,
    ActionTable,
    get_eof_symbol,
    Rule,
    )


def generate_action_table(symbols, starting_symbol, rules):
    symbol_data = make_symbol_data(symbols, starting_symbol, rules)
    state_graph = make_state_graph(
        symbols, starting_symbol, rules, symbol_data)
    return make_action_table(state_graph, symbols, symbol_data)


class SymbolData(defaultdict):

    def __init__(self, *args, **kwargs):
        super().__init__(SymbolDataEntry, *args, **kwargs)


class SymbolDataEntry:

    def __init__(self):
        self.nullable = False
        self.first_set = set()
        self.follow_set = set()


def make_symbol_data(symbols, starting_symbol, rules):
    symbol_data = SymbolData()
    fill_terminals_first_set(symbols, symbol_data)
    #? symbol_data[starting_symbol].follow_set.add(get_eof_symbol(symbols))
    over_rules_until_false(update_rule_nullable, rules, symbol_data)
    over_rules_until_false(update_rule_first_set, rules, symbol_data)
    over_rules_until_false(update_rule_follow_set, rules, symbol_data)
    return symbol_data


def fill_terminals_first_set(symbols, symbol_data):
    for symbol in symbols:
        if symbol.is_terminal():
            symbol_data[symbol].first_set.add(symbol)


def update_rule_nullable(rule, symbol_data):
    if symbol_data[rule.head].nullable:
        return False
    value = is_rule_nullable(rule, symbol_data)
    symbol_data[rule.head].nullable = value
    return value


def is_rule_nullable(rule, symbol_data):
    return all(symbol_data[symbol].nullable for symbol in rule.children)


def update_rule_first_set(rule, symbol_data):
    return does_update_set(
        symbol_data[rule.head].first_set,
        rule_first_set(rule, symbol_data))


def rule_first_set(rule, symbol_data):
    first_set = set()
    for symbol in rule.children:
        first_set.update(symbol_data[symbol].first_set)
        if not symbol_data[symbol].nullable:
            break
    return first_set


def update_rule_follow_set(rule, symbol_data):
    new_follow_sets = rule_follow_set(rule, symbol_data)
    return any(does_update_set(symbol_data[symbol].follow_set, new_set)
               for symbol, new_set in new_follow_sets.items())


def rule_follow_set(rule, symbol_data):
    follow_sets = defaultdict(set)
    for pos, symbol in enumerate(rule.children):
        for follow_symbol in rule.children[pos+1:]:
            follow_sets[symbol].update(symbol_data[follow_symbol].first_set)
            if not symbol_data[follow_symbol].nullable:
                break
        else:
            follow_sets[symbol].update(symbol_data[rule.head].follow_set)
    return follow_sets


def does_update_set(dst_set, src_set):
    if dst_set.issuperset(src_set):
        return False
    dst_set.update(src_set)
    return True


def over_rules_until_false(callable, rules, symbol_data):
    while any(callable(rule, symbol_data) for rule in rules):
        pass


# TODO: Python3.6's typing.NamedTuple
_Item = namedtuple('_Item', ['rule', 'pos'])
class Item(_Item):

    def __new__(cls, rule, pos=0):
        assert pos <= len(rule.children)
        return super().__new__(cls, rule, pos)

    @property
    def head(self):
        return self.rule.head

    @property
    def children(self):
        return self.rule.children

    def next_symbol(self):
        if self.is_finished():
            return None
        return self.children[self.pos]

    def next_item(self):
        if self.is_finished():
            raise ValueError('Finished item has no next')
        return Item(self.rule, self.pos + 1)

    def is_finished(self):
        return self.pos == len(self.children)


class StateGraph:
    """A graph that shows the structure of a state machine."""

    def __init__(self):
        # : Sequence[Tuple[Label, MutableMapping[Symbol, int]]]
        self._states = []

    def default_lookup(self, label):
        try:
            return self.lookup(label)
        except KeyError:
            id = len(self._states)
            self._states.append((label, {}))
            return id

    def lookup(self, label):
        for state_id, state_label in enumerate(self._states):
            if state_label == label:
                return state_id
        raise KeyError(label)

    def label_of(self, state):
        return self._states[state][0]

    def add_transition(self, src_id, symbol, dst_id):
        transitions = self._states[src_id][1]
        if symbol in transitions:
            assert transitions[symbol] == dst_id
        else:
            transitions[symbol] = dst_id

    def iter_state_ids(self):
        # range(len(self._states)) will not account for new states.
        yield from map(lambda x: x[0], enumerate(self._states))

    def iter_states(self):
        yield from enumerate(self._states)

    def follow_transition(self, state, edge):
        return self._states[state][1][edge]


def make_state_graph(symbols, starting_symbol, rules, symbol_data):
    graph = StateGraph()
    imaginary_rule = make_imaginary_rule(symbols, starting_symbol)
    initial_label = fill_kernal_label(rules, Label([Item(imaginary_rule)]))
    graph.default_lookup(initial_label)

    for state in graph.iter_state_ids():
        for symbol in symbols:
            if symbol.is_terminal() or symbol.is_nonterminal():
                build_transition(graph, rules, state, symbol)
    return graph


def make_imaginary_rule(symbols, starting_symbol):
    eof = get_eof_symbol(symbols)
    return Rule(eof, (starting_symbol, eof))


def build_transition(graph, rules, state, symbol):
    dst_label = find_destination_label(rules, graph.label_of(state), symbol)
    if dst_label:
        dst_state = graph.default_lookup(dst_label)
        graph.add_transition(state, symbol, dst_state)


def find_destination_label(rules, source_label, symbol):
    return fill_kernal_label(rules, shift_all(source_label, symbol))


def shift_all(label, symbol):
    return Label(
        item.next_item() for item in label if item.next_symbol() is symbol)


def fill_kernal_label(rules, kernal_label):
    new_label_rules = list(kernal_label)
    for item in new_label_rules:
        symbol = item.next_symbol()
        if symbol is not None and symbol.is_nonterminal():
            for rule in filter(lambda r: r.head == symbol, rules):
                if rule not in new_label_rules:
                    new_label_rules.append(Item(rule))
    return Label(new_label_rules)


class Label(frozenset):
    """A set of Items."""


def make_action_table(graph, symbols, symbol_data):
    action_table = ActionTable()
    add_shift_and_done_operations(action_table, graph, symbols)
    add_reduce_operations(action_table, graph, symbol_data)
    return action_table


def add_shift_and_done_operations(table, graph, symbols):
    eof = get_eof_symbol(symbols)
    for state, label in graph.iter_states():
        for symbol in symbols:
            if shift_all(label, symbol):
                if symbol is not eof:
                    dst = graph.follow_transition(state, symbol)
                    table[state, symbol] = Action.shift(dst)
                else:
                    table[state, symbol] = Action.done()


def add_reduce_operations(table, graph, symbol_data):
    for state, label in graph.iter_states():
        for item in label:
            if item.is_full():
                for symbol in symbol_data[item.head].follow_set:
                    table[state, symbol] = Action.reduce(item.rule)
