"""Testing of the slr1 ActionTable generator."""


from collections import defaultdict
import unittest


from cfg import (
    Rule,
    SymbolEnum,
    )
from slr1 import (
    generate_action_table,
    fill_kernal_label,
    fill_terminals_first_set,
    Item,
    Label,
    rule_first_set,
    rule_follow_set,
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


class TestMakeStateGraph(unittest.TestCase):

    def test_fill_kernal_label(self):
        class Sym(SymbolEnum):
            HEAD = ('HEAD', False)
            A = ('A', False)
            B = ('B', False)
            X = ('X', False)
            Y = ('Y', False)
            c = ('c', True)
            x = ('x', True)
            y = ('y', True)

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
    pass
