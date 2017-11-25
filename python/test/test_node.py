"""Tests for the node.py file."""


import unittest

from node import (
    Node,
    NodeSymbol,
    Nonterminal,
    Terminal,
    )


class TestNode(unittest.TestCase):

    def test_node_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            Node()

    def test_terminal_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            Terminal('try')
        with self.assertRaises(NotImplementedError):
            Terminal.take_from_string('try')

    def test_nonterminal_is_abstract(self):
        with self.assertRaises(NotImplementedError):
            Nonterminal([], ())
