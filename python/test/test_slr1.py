"""Testing of the slr1 ActionTable generator."""


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
