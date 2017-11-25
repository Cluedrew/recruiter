"""Test the tokenization process."""


import unittest

from node import (
    iter_terminals_from_str,
    NodeSymbol,
    )


def list_terminals_from_str(text):
    return list(iter_terminals_from_str(text))


class TestToken(unittest.TestCase):

    def assertTokenMatch(self, symbol, text, token):
        if symbol != token.symbol or text != token.text:
            self.fail('<{}, {}> != {}'.format(symbol, text, token))

    def test_parse_operation_upper(self):
        tokens = list_terminals_from_str('ADD')
        self.assertEqual(1, len(tokens))
        self.assertTokenMatch(NodeSymbol.Operation, 'ADD', tokens[0])
