"""Testing for the Context-Free Grammer."""


import unittest


import cfg


class TestSymbolEnum(unittest.TestCase):

    class Enum1(cfg.SymbolEnum):
        A = ('A', True)
        B = ('B', False)
        D = ('D', None)

    def test_is_terminal(self):
        self.assertIs(True, self.Enum1.A.is_terminal())
        self.assertIs(False, self.Enum1.B.is_terminal())
        self.assertIs(False, self.Enum1.D.is_terminal())

    def test_is_nonterminal(self):
        self.assertIs(False, self.Enum1.A.is_nonterminal())
        self.assertIs(True, self.Enum1.B.is_nonterminal())
        self.assertIs(False, self.Enum1.D.is_nonterminal())

    def test_repr(self):
        self.assertEqual('<Enum1.D: None>', repr(self.Enum1.D))


class TestActionTable(unittest.TestCase):

    def test_new_action_table(self):
        self.assertEqual(0, len(cfg.ActionTable()))
