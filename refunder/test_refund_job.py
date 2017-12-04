from django.conf import settings
from django.test import TestCase
import glob
import os

import braintree

from refunder.refund_job import RefundJob

class RefundJobTest(TestCase):

    DUMMY_KEYS = ['sandbox', 'merchant_id', 'public_key', 'private_key']
    DUMMY_FILE = os.path.join(settings.BASE_DIR, "functional_tests/dummy_source.csv")
    
    def tearDown(self):
        for f in glob.glob(os.path.join(settings.BASE_DIR, 'refunder/files/*')):
            os.remove(f)

    def test_it_creates_a_log_file(self):
        job = RefundJob(self.DUMMY_KEYS)

        job.run(self.DUMMY_FILE)
        log_file = glob.glob(os.path.join(settings.BASE_DIR, "refunder/files/*log*.csv"))[0]
        with open(log_file) as log:
            log_text = log.read()
            log.close()

        self.assertIn("Original Txn ID,Refund Txn ID,Error Message", log_text)

