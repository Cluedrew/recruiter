"""Testing for the Context-Free Grammer."""


import unittest


import cfg
import rules
import slr1


class TestCfg(unittest.TestCase):

    def test_new_action_table(self):
        self.assertEqual(0, len(cfg.ActionTable()))



class TestSLR1(unittest.TestCase):

    def test_tiny_grammer(self):
        table = slr1.generate_action_table([rules.Rule('S', 'i')], ['i'])
