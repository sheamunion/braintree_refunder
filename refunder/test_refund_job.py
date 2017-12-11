from django.conf import settings
from django.test import TestCase
from unittest.mock import Mock
import glob, os, tempfile

import braintree

from refunder.braintree_refund_gateway import BraintreeRefundGateway
from refunder.refund_job import RefundJob

class RefundJobTest(TestCase):

    def setUp(self):
        self.VALID_KEYS = [os.getenv('BT_ENVIRONMENT'), os.getenv('BT_MERCHANT_ID'), os.getenv('BT_PUBLIC_KEY'), os.getenv('BT_PRIVATE_KEY')]        
        _, self.DUMMY_LOG_FILE = tempfile.mkstemp(dir=os.path.join(settings.BASE_DIR, 'refunder/files/'))

    def tearDown(self):
        for f in glob.glob(os.path.join(settings.BASE_DIR, 'refunder/files/*')):
            os.remove(f)

    def test_it_creates_a_log_file_with_header(self):
        transaction_loader_mock = Mock()
        transaction_loader_mock.all.return_value = [{'txn_id': 'a1', 'amount': ''}]

        braintree_refunder_gateway_mock = Mock() 
        braintree_refunder_gateway_mock.find_void_or_refund.return_value = ['a','ra','SUCCESS','Transaction refunded.\n']
        
        job = RefundJob(self.VALID_KEYS)
        job.transaction_loader = transaction_loader_mock
        job.gateway = braintree_refunder_gateway_mock 

        job.run(self.DUMMY_LOG_FILE)

        with open(self.DUMMY_LOG_FILE) as log:
            log_text = log.read()
            log.close()

        self.assertIn('transaction_id,refunded_transaction_id,status,message\n', log_text)

    def test_it_appends_correct_data_to_log_file_when_requests_are_successful(self):
        DUMMY_FILE_PATH = os.path.join(settings.BASE_DIR, 'functional_tests/dummy_source.csv')
        with open(DUMMY_FILE_PATH) as source_file:
            DUMMY_FILE = source_file.read().splitlines()

        braintree_refunder_gateway_mock = Mock() 
        braintree_refunder_gateway_mock.find_void_or_refund.side_effect = [['a','ra','SUCCESS','Transaction refunded.\n'],
                                                                           ['b','rb','SUCCESS','Transaction refunded.\n'],
                                                                           ['c','rc','SUCCESS','Transaction refunded.\n']]

        job = RefundJob(self.VALID_KEYS, DUMMY_FILE)
       	job.gateway = braintree_refunder_gateway_mock 
        
        job.run(self.DUMMY_LOG_FILE)

        with open(self.DUMMY_LOG_FILE) as log:
            log_text = log.read()
            log.close()

        self.assertIn('a,ra,SUCCESS,Transaction refunded.\n', log_text)
        self.assertIn('b,rb,SUCCESS,Transaction refunded.\n', log_text)
        self.assertIn('c,rc,SUCCESS,Transaction refunded.\n', log_text)
