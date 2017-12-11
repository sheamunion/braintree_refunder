from django.conf import settings
from django.test import TestCase
import os

from .transaction_loader import TransactionLoader

class TestTransactionLoader(TestCase):

    def test_all_returns_transaction_ids_and_amounts(self):
        txns_mock = [{'id': 'a', 'amount': ''},
                     {'id': 'b', 'amount': '1'},
                     {'id': 'c', 'amount': '3.50'}]
        self.DUMMY_FILE = bytes(os.path.join(settings.BASE_DIR, 'functional_tests/dummy_source.csv'), encoding='UTF-8')

        with open(self.DUMMY_FILE) as source_file:
            loader = TransactionLoader(source_file.read().splitlines())

        self.assertEqual(loader.all(), txns_mock)
