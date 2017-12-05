"""Testing of the slr1 ActionTable generator."""


from collections import defaultdict
import unittest

import cfg
import slr1


class TestSlr1(unittest.TestCase):

    def do_not_test_tiny_grammer(self):
        class TinySym(cfg.SymbolEnum):
            START = ('START', False)
            integer = ('integer', True)
            _EOF = ('_EOF', None)

        table = slr1.generate_action_table(
            TinySym, TinySym.START,
            [cfg.Rule(TinySym.START, (TinySym.integer,))],
            )

    def test_repr_item(self):
        rule = cfg.Rule('S', ('4', '3'))
        item = slr1.Item(rule, 1)
        self.assertEqual(
            "Item(rule=Rule(head='S', children=('4', '3')), pos=1)",
            repr(item))

    def test_item_next_item(self):
        rule = cfg.Rule('S', ('4', '3'))
        item = slr1.Item(rule)
        self.assertEqual(slr1.Item(rule, 1), item.next_item())

    def test_new_label(self):
        rule = cfg.Rule('S', ('4', '3'))
        label = slr1.Label([slr1.Item(rule), slr1.Item(rule, 1)])


class LetterSym(cfg.SymbolEnum):
    A = ('A', True)
    B = ('B', False)
    C = ('C', False)
    D = ('D', True)


class TestMakeSymbolData(unittest.TestCase):

    def test_fill_terminals_first_set(self):
        symbol_data = slr1.SymbolData()
        slr1.fill_terminals_first_set(LetterSym, symbol_data)
        self.assertEqual({LetterSym.A}, symbol_data[LetterSym.A].first_set)
        self.assertEqual({LetterSym.D}, symbol_data[LetterSym.D].first_set)
        for letter in [LetterSym.B, LetterSym.C]:
            self.assertTrue(letter not in symbol_data
                            or not symbol_data[letter].first_set)

    def test_update_rule_nullable_empty(self):
        symbol_data = slr1.SymbolData()
        empty_rule = cfg.Rule(LetterSym.B, ())
        self.assertTrue(slr1.update_rule_nullable(empty_rule, symbol_data))
        self.assertTrue(symbol_data[LetterSym.B].nullable)

    def test_update_rule_nullable_yes(self):
        symbol_data = slr1.SymbolData()
        rule = cfg.Rule(LetterSym.C, (LetterSym.A, LetterSym.D))
        symbol_data[LetterSym.A].nullable = True
        symbol_data[LetterSym.D].nullable = True
        self.assertTrue(slr1.update_rule_nullable(rule, symbol_data))
        self.assertTrue(symbol_data[LetterSym.C].nullable)

    def test_update_rule_nullable_no(self):
        symbol_data = slr1.SymbolData()
        rule = cfg.Rule(LetterSym.C, (LetterSym.A, LetterSym.D))
        symbol_data[LetterSym.D].nullable = True
        self.assertFalse(slr1.update_rule_nullable(rule, symbol_data))
        self.assertFalse(symbol_data[LetterSym.C].nullable)

    def test_update_rule_nullable_skip(self):
        symbol_data = slr1.SymbolData()
        empty_rule = cfg.Rule(LetterSym.B, ())
        symbol_data[LetterSym.B].nullable = True
        self.assertFalse(slr1.update_rule_nullable(empty_rule, symbol_data))
        self.assertTrue(symbol_data[LetterSym.B].nullable)

    def test_rule_first_set(self):
        symbol_data = slr1.SymbolData()
        rule = cfg.Rule(LetterSym.B, (LetterSym.C, LetterSym.A, LetterSym.D))
        symbol_data[LetterSym.C].nullable = True
        symbol_data[LetterSym.C].first_set = {'ceta'}
        symbol_data[LetterSym.A].first_set = {'alpha'}
        symbol_data[LetterSym.D].first_set = {'delta'}
        self.assertEqual({'ceta', 'alpha'},
                         slr1.rule_first_set(rule, symbol_data))

    def test_rule_follow_set(self):
        symbol_data = slr1.SymbolData()
        rule = cfg.Rule(LetterSym.B, (LetterSym.A, LetterSym.C, LetterSym.D))
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
            slr1.rule_follow_set(rule, symbol_data))
