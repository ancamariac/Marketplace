import unittest


class TestMarketplace(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')