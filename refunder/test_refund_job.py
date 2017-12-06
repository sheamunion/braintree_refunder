from django.conf import settings
from django.test import TestCase
import glob
import os
import tempfile

import braintree

from refunder.refund_job import RefundJob

class RefundJobTest(TestCase):

    def setUp(self):
        self.DUMMY_KEYS = ['sandbox', 'merchant_id', 'public_key', 'private_key']
        self.DUMMY_FILE = os.path.join(settings.BASE_DIR, "functional_tests/dummy_source.csv")
        _, self.DUMMY_LOG_FILE = tempfile.mkstemp(dir=os.path.join(settings.BASE_DIR, "refunder/files/"))

    def tearDown(self):
        for f in glob.glob(os.path.join(settings.BASE_DIR, 'refunder/files/*')):
            os.remove(f)

    def test_it_creates_a_log_file_with_header(self):
        job = RefundJob(self.DUMMY_KEYS)

        job.run(self.DUMMY_FILE, self.DUMMY_LOG_FILE)

        with open(self.DUMMY_LOG_FILE) as log:
            log_text = log.read()
            log.close()

        self.assertIn("transaction_id,refund_transaction_id,status,message", log_text)

    def test_it_appends_correct_data_to_log_file_when_requests_are_successful(self):
        job = RefundJob(self.DUMMY_KEYS)

        job.run(self.DUMMY_FILE, self.DUMMY_LOG_FILE)

        with open(self.DUMMY_LOG_FILE) as log:
            log_text = log.read()
            log.close()

        self.assertIn("a,ra,", log_text)
        self.assertIn("b,rb,", log_text)
        self.assertIn("c,rc,", log_text)
