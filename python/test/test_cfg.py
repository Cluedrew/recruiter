"""Testing for the Context-Free Grammer."""


import unittest


import cfg
import rules
import slr1


class TestCfg(unittest.TestCase):

    def test_new_action_table(self):
        self.assertEqual(0, len(cfg.ActionTable()))



class TestSlr1(unittest.TestCase):

    def test_tiny_grammer(self):
        table = slr1.generate_action_table([rules.Rule('S', ('i'))], ['i'])


    def test_repr_item(self):
        rule = rules.Rule('S', ('4', '3'))
        item = slr1.Item(rule, 1)
        self.assertEqual(
            "Item(rule=Rule(head='S', children=('4', '3')), pos=1)",
            repr(item))

    def test_item_next_item(self):
        rule = rules.Rule('S', ('4', '3'))
        item = slr1.Item(rule)
        self.assertEqual(slr1.Item(rule, 1), item.next_item())

    def test_new_label(self):
        rule = rules.Rule('S', ('4', '3'))
        label = slr1.Label([slr1.Item(rule), slr1.Item(rule, 1)])
