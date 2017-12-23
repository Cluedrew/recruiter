"""Testing of the slr1 ActionTable generator."""


from collections import defaultdict
import unittest
from unittest.mock import (
    call,
    patch,
    )


from cfg import (
    Action,
    ActionTable,
    Rule,
    SymbolEnum,
    )
from slr1 import (
    add_reduce_operations,
    add_shift_and_done_operations,
    generate_action_table,
    fill_kernal_label,
    fill_state_graph,
    fill_terminals_first_set,
    insert_starting_state,
    Item,
    Label,
    make_imaginary_rule,
    rule_first_set,
    rule_follow_set,
    shift_all,
    StateGraph,
    SymbolData,
    update_rule_nullable,
    )


class TestSlr1(unittest.TestCase):

    def do_not_test_tiny_grammer(self):
        class TinySym(SymbolEnum):
            START = ('START', False)
            integer = ('integer', True)
            _EOF = ('_EOF', None)

        table = generate_action_table(
            TinySym, TinySym.START,
            [Rule(TinySym.START, (TinySym.integer,))],
            )

    def test_repr_item(self):
        rule = Rule('S', ('4', '3'))
        item = Item(rule, 1)
        self.assertEqual(
            "Item(rule=Rule(head='S', children=('4', '3')), pos=1)",
            repr(item))

    def test_item_next_item(self):
        rule = Rule('S', ('4', '3'))
        item = Item(rule)
        self.assertEqual(Item(rule, 1), item.next_item())

    def test_new_label(self):
        rule = Rule('S', ('4', '3'))
        label = Label([Item(rule), Item(rule, 1)])


class LetterSym(SymbolEnum):
    A = ('A', True)
    B = ('B', False)
    C = ('C', False)
    D = ('D', True)


class TestMakeSymbolData(unittest.TestCase):

    def test_fill_terminals_first_set(self):
        symbol_data = SymbolData()
        fill_terminals_first_set(LetterSym, symbol_data)
        self.assertEqual({LetterSym.A}, symbol_data[LetterSym.A].first_set)
        self.assertEqual({LetterSym.D}, symbol_data[LetterSym.D].first_set)
        for letter in [LetterSym.B, LetterSym.C]:
            self.assertTrue(letter not in symbol_data
                            or not symbol_data[letter].first_set)

    def test_update_rule_nullable_empty(self):
        symbol_data = SymbolData()
        empty_rule = Rule(LetterSym.B, ())
        self.assertTrue(update_rule_nullable(empty_rule, symbol_data))
        self.assertTrue(symbol_data[LetterSym.B].nullable)

    def test_update_rule_nullable_yes(self):
        symbol_data = SymbolData()
        rule = Rule(LetterSym.C, (LetterSym.A, LetterSym.D))
        symbol_data[LetterSym.A].nullable = True
        symbol_data[LetterSym.D].nullable = True
        self.assertTrue(update_rule_nullable(rule, symbol_data))
        self.assertTrue(symbol_data[LetterSym.C].nullable)

    def test_update_rule_nullable_no(self):
        symbol_data = SymbolData()
        rule = Rule(LetterSym.C, (LetterSym.A, LetterSym.D))
        symbol_data[LetterSym.D].nullable = True
        self.assertFalse(update_rule_nullable(rule, symbol_data))
        self.assertFalse(symbol_data[LetterSym.C].nullable)

    def test_update_rule_nullable_skip(self):
        symbol_data = SymbolData()
        empty_rule = Rule(LetterSym.B, ())
        symbol_data[LetterSym.B].nullable = True
        self.assertFalse(update_rule_nullable(empty_rule, symbol_data))
        self.assertTrue(symbol_data[LetterSym.B].nullable)

    def test_rule_first_set(self):
        symbol_data = SymbolData()
        rule = Rule(LetterSym.B, (LetterSym.C, LetterSym.A, LetterSym.D))
        symbol_data[LetterSym.C].nullable = True
        symbol_data[LetterSym.C].first_set = {'ceta'}
        symbol_data[LetterSym.A].first_set = {'alpha'}
        symbol_data[LetterSym.D].first_set = {'delta'}
        self.assertEqual({'ceta', 'alpha'},
                         rule_first_set(rule, symbol_data))

    def test_rule_follow_set(self):
        symbol_data = SymbolData()
        rule = Rule(LetterSym.B, (LetterSym.A, LetterSym.C, LetterSym.D))
        symbol_data[LetterSym.C].nullable = True
        symbol_data[LetterSym.C].first_set = {'ceta'}
        symbol_data[LetterSym.A].first_set = {'alpha'}
        symbol_data[LetterSym.D].first_set = {'delta'}
        symbol_data[LetterSym.B].follow_set = {'beta'}
        self.assertEqual(defaultdict(set, {
                LetterSym.A: {'ceta', 'delta'},
                LetterSym.C: {'delta'},
                LetterSym.D: {'beta'},
                }),
            rule_follow_set(rule, symbol_data))


class TestStateGraph(unittest.TestCase):

    def small_state_graph(self, label=Label('a')):
        graph = StateGraph()
        graph._states.append((label, {}))
        return graph

    def test_lookup(self):
        graph = self.small_state_graph()
        self.assertEqual(0, graph.lookup(Label('a')))

    def test_lookup_miss(self):
        graph = self.small_state_graph()
        with self.assertRaises(KeyError):
            graph.lookup(Label('b'))


class TestMakeStateGraph(unittest.TestCase):

    class StartEnd(SymbolEnum):
        START = ('START', False)
        END = ('END', None)

    def test_make_imaginary_rule(self):
        Simple = self.StartEnd
        self.assertEqual(Rule(Simple.END, (Simple.START, Simple.END)),
                         make_imaginary_rule(Simple, Simple.START))

    def test_insert_starting_state(self):
        graph = StateGraph()
        Sym = self.StartEnd
        rule = make_imaginary_rule(Sym, Sym.START)
        insert_starting_state(graph, rule, [])
        self.assertEqual(1, len(graph._states))
        self.assertEqual((Label([Item(rule)]), {}), graph._states[0])

    def test_fill_state_graph(self):
        class Sym(SymbolEnum):
            START = ('START', False)
            MIDDLE = ('MIDDLE', True)
            END = ('END', None)

        Rules = (Rule(Sym.START, (Sym.MIDDLE, Sym.MIDDLE)),)

        graph = StateGraph()
        with patch.object(graph, 'iter_state_ids', return_value=range(3)):
            with patch('slr1.build_transition') as mock_bt:
                fill_state_graph(graph, Sym, Rules)
        self.assertEqual(9, mock_bt.call_count)
        self.assertEqual(
            mock_bt.call_args_list, [
                call(graph, Rules, 0, Sym.START),
                call(graph, Rules, 0, Sym.MIDDLE),
                call(graph, Rules, 0, Sym.END),
                call(graph, Rules, 1, Sym.START),
                call(graph, Rules, 1, Sym.MIDDLE),
                call(graph, Rules, 1, Sym.END),
                call(graph, Rules, 2, Sym.START),
                call(graph, Rules, 2, Sym.MIDDLE),
                call(graph, Rules, 2, Sym.END),
                ])

    class Sym1(SymbolEnum):
        HEAD = ('HEAD', False)
        A = ('A', False)
        B = ('B', False)
        X = ('X', False)
        Y = ('Y', False)
        c = ('c', True)
        x = ('x', True)
        y = ('y', True)

    def test_shift_all(self):
        Sym = self.Sym1
        rule = Rule(Sym.HEAD, (Sym.A, Sym.B))
        items = (
            Item(Rule(Sym.HEAD, (Sym.A,)), 1),
            Item(Rule(Sym.HEAD, (Sym.A, Sym.B)), 1),
            Item(Rule(Sym.HEAD, (Sym.A, Sym.A)), 1),
            )
        expect_items = (
            Item(Rule(Sym.HEAD, (Sym.A, Sym.A)), 2),
            )
        self.assertEqual(
            Label(expect_items),
            shift_all(Label(items), Sym.A))

    def small_label(self, head, children, place):
        return Label([Item(Rule(head, children), place)])

    def test_shift_all_match(self):
        Sym = self.Sym1
        self.assertEqual(
            self.small_label(Sym.HEAD, (Sym.A,), 1),
            shift_all(self.small_label(Sym.HEAD, (Sym.A,), 0), Sym.A))

    def test_shift_all_mismatch(self):
        Sym = self.Sym1
        self.assertEqual(
            Label(),
            shift_all(self.small_label(Sym.HEAD, (Sym.A,), 0), Sym.B))

    def test_shift_all_end(self):
        Sym = self.Sym1
        self.assertEqual(
            Label(),
            shift_all(self.small_label(Sym.HEAD, (Sym.A,), 1), Sym.A))

    def test_fill_kernal_label(self):
        Sym = self.Sym1
        rules = (
            Rule(Sym.HEAD, (Sym.A, Sym.B)),
            Rule(Sym.A, (Sym.A, Sym.B)),
            Rule(Sym.B, (Sym.X, Sym.Y)),
            Rule(Sym.X, (Sym.x,)),
            Rule(Sym.Y, (Sym.y, Sym.y)),
            Rule(Sym.B, ()),
            )
        items = (
            Item(Rule(Sym.HEAD, (Sym.A, Sym.B)), 1),
            Item(Rule(Sym.HEAD, (Sym.A, Sym.c)), 1),
            )
        expect_item = (
            Item(Rule(Sym.HEAD, (Sym.A, Sym.c)), 1),
            Item(rules[0], 1),
            Item(rules[2]),
            Item(rules[3]),
            Item(rules[5]),
            )
        self.assertEqual(
            Label(expect_item), fill_kernal_label(rules, Label(items)))


class TestMakeActionTable(unittest.TestCase):

    class Symbols(SymbolEnum):
        START = ('START', False)
        MIDDLE = ('MIDDLE', True)
        END = ('END', None)

    def test_add_shift_and_done_operations(self):
        Symbols = self.Symbols
        table = ActionTable()
        graph = StateGraph()
        graph._states.append((None, {Symbols.MIDDLE: 1, Symbols.END: 2}))
        add_shift_and_done_operations(table, graph, Symbols)
        self.assertEqual(Action('shift', 1), table[0, Symbols.MIDDLE])
        self.assertEqual(Action('done', None), table[0, Symbols.END])

    def test_add_reduce_operations(self):
        Symbols = self.Symbols
        rule = Rule(Symbols.START, (Symbols.MIDDLE,))
        table = ActionTable()
        graph = StateGraph()
        graph._states.append((Label.from_rule(rule, 1), {}))
        data = SymbolData()
        data[Symbols.START].follow_set.add(Symbols.END)
        add_reduce_operations(table, graph, data)
        self.assertEqual(Action('reduce', rule), table[0, Symbols.END])
