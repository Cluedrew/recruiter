"""Tests for the grammar.py file."""


import unittest

from cfg import (
    TerminalNode,
    )
from grammar import (
    iter_terminals_from_str,
    NodeSymbol,
    )


def list_terminals_from_str(text):
    return list(iter_terminals_from_str(text))


class TestNode(unittest.TestCase):

    def test_iter_terminals_from_str(self):
        target = [
            (NodeSymbol.Register, 'r4'),
            (NodeSymbol.Comma, ','),
            (NodeSymbol.Identifier, 'hi'),
            ]
        self.assertEqual(target, list_terminals_from_str('r4 ,hi'))

    def test_iter_terminals_no_match(self):
        with self.assertRaisesRegex(Exception, '@@'):
            list_terminals_from_str(',@@')


    def test_parse_operation_upper(self):
        tokens = list_terminals_from_str('ADD')
        self.assertEqual([(NodeSymbol.Operation, 'ADD')], tokens)
