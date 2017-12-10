"""Testing for the Context-Free Grammer."""


import itertools
import unittest


import cfg
from cfg import (
    Rule,
    RuleListing,
    RuleMap,
    SymbolEnum,
    )


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


class TestRule(unittest.TestCase):

    def test_new_rule(self):
        rule = cfg.Rule(0, (1, 2))
        self.assertEqual(0, rule.head)
        self.assertEqual((1, 2), rule.children)


# Can I make this one work?
class TestRuleListing(unittest.TestCase):

    def do_not_test_new_rule_listing(self):
        class Enum1(SymbolEnum):
            N = ('N', False)
            T = ('T', True)

        class Rules(RuleListing, symbols_from=Enum1):
            TWO = 'N', ['T', 'T']

        self.assertIsInstance(Rules.TWO, Rule)
        self.assertEqual(Rule(Enum1.N, (Enum1.T, Enum1.T)), Rules.TWO)


class TestRuleMap(unittest.TestCase):

    def test_new_rule_map(self):
        class Enum1(SymbolEnum):
            N = ('N', False)
            T = ('T', True)

        rule_map = RuleMap(
            Enum1,
            TWO=('N', ('T', 'T')),
            )
        self.assertEqual(rule_map['TWO'], Rule(Enum1.N, (Enum1.T, Enum1.T)))


class TestNode(unittest.TestCase):

    def test_terminal_node_repr(self):
        self.assertEqual("TerminalNode(symbol='sym', text='str')",
                         repr(cfg.TerminalNode('sym', 'str')))


class TestActionTable(unittest.TestCase):

    def test_new_action_table(self):
        self.assertEqual(0, len(cfg.ActionTable()))


class TestPasingStack(unittest.TestCase):

    def test_pasing_stack(self):
        stack = cfg.ParsingStack()
        stack.push('state', 'node')
        self.assertEqual('state', stack.peek_state())
        self.assertEqual('node', stack.peek_node())
        self.assertEqual(1, len(stack))
        self.assertEqual(('state', 'node'), stack.pop())
        self.assertEqual(0, len(stack))


class TestNodeStream(unittest.TestCase):

    def test_node_stream(self):
        raw = [(0, 'alpha'), (1, 'first'), (2, 'second'), (3, 'third')]
        terminals = list(itertools.starmap(cfg.TerminalNode, raw))
        stream = cfg.NodeStream(raw[1:], 'eof')
        self.assertEqual(terminals[1], next(stream.in_place()))
        stream.push_back(terminals[0])
        self.assertEqual(terminals[0], next(stream.in_place()))
        rest = list(stream)
        self.assertEqual(terminals, rest[:-1])
        self.assertEqual('eof', rest[-1].symbol)
