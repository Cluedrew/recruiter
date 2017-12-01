"""Testing for the Context-Free Grammer."""


import unittest


import cfg


class TestCfg(unittest.TestCase):

    def test_new_action_table(self):
        self.assertEqual(0, len(cfg.ActionTable()))
