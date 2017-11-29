"""Simple Left/Right Lookahead 1 Action Table Generator."""


from collections import defaultdict, namedtuple

import cfg


class SymbolData:

    def __init__(self):
        self.nullable = False
        self.first_set = set()
        self.follow_set = set()


def generate_action_table(rules, terminal_symbols):
    symbol_data = defaultdict(SymbolData)
    fill_terminals_first(terminal_symbols, symbol_data)
    over_rules_until_false(update_rule_nullable, rules, symbol_data)
    over_rules_until_false(update_rule_first_set, rules, symbol_data)
    over_rules_until_false(update_rule_follow_set, rules, symbol_data)


def update_rule_nullable(rule, symbol_data):
    if symbol_data[rule.head].nullable:
        return False
    value = is_rule_nullable(rule, symbol_data)
    symbol_data[rule.head].nullable = value
    return value


def is_rule_nullable(rule, symbol_data):
    value = all(symbol_data[symbol].nullable for symbol in rule.children)


def fill_terminals_first(terminals, symbol_data):
    for symbol in terminals:
            symbol_data[symbol].first_set.update(symbol)


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
        if self.pos < len(self.children):
            return self.children[self.pos]
        return None

    def next_item(self):
        if self.pos < len(self.children):
            return Item(self.rule, self.pos + 1)
        raise ValueError('Finished item has no next')


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
        for state_id, state_label in enumerate(self._state):
            if state_label == label:
                return state_id
        raise KeyError(label)

    def add_transition(self, src_id, symbol, dst_id):
        transitions = self._states[src_id][1]
        if symbol in transitions:
            assert transitions[symbol] == dst_id
        else:
            transitions[symbol] = dst_id

    def iter_state_ids(self):
        # range(len(self._states)) will not account for new states.
        yield from map(lambda x: x[0], enumerate(self._states))


def generate_state_graph(rules, symbol_data):
    # If I use the imaginary EOF -> S EOF rule I need the EOF.
    graph = StateGraph()
    # Set up with imaginary rule as the starting state.
    imaginary_rule = Rule(
        cfg.NodeSymbol._EOF,
        (cfg.NodeSymbol.START, cfg.NodeSymbol._EOF))
    initial_label = fill_kernal_label(Label([Item(imaginary_rule)]))
    graph.default_lookup(initial_label)

    for state in graph.iter_state_ids():
        for symbol in symbols_not_eof:
            build_transition(graph, state, symbol)
    return graph


def build_transition(graph, state, symbol):
    dst_label = find_destination_label(graph.lookup(state), symbol)
    if not dst_label:
        return None
    dst_state = graph.default_lookup()
    graph.add_transition(state, symbol, dst_state)
    return dst_state


def find_destination_label(source_label, symbol):
    return fill_kernal_label(shift_all(source_label, symbol))


def shift_all(label, symbol):
    return Label(
        item.next_item() for item in label if item.next_symbol() is symbol)


def fill_kernal_label(rules, kernal_label):
    new_label_rules = list(kernal_label)
    for item in new_label_rules:
        symbol = item_next_symbol(item)
        if symbol is not None and symbol.is_nonterminal():
            for rule in filter(lambda r: r.head == symbol, rules):
                if rule not in new_label_rules:
                    new_label_rules.append(Item(rule))
    return Label(new_label_rules)


class Label(frozenset):
    """A set of Items."""
