from datetime import datetime
from django.conf import settings
import os
import tempfile

import braintree

from .braintree_refund_gateway import BraintreeRefundGateway
from .transaction_loader import TransactionLoader

class RefundJob():

    def __init__(self, keys, source_file = None):
        self.gateway = BraintreeRefundGateway(keys)
        self.transaction_loader = TransactionLoader(source_file)

    def run(self, log_file = None):
        transactions = self.transaction_loader.all()
        if not log_file:
            log_file = self.__create_log_file()
        txn_refund_logs = []

        for txn in transactions:
            txn_refund_logs.append(self.gateway.find_void_or_refund(txn))

        with open(log_file, 'r+') as log_file:
            log_file.write('transaction_id,refunded_transaction_id,status,message\n')
            for log in txn_refund_logs:
                log_file.write('{},{},{},{}'.format(log[0], log[1], log[2], log[3]))

        return

    def __create_log_file(self):
        handle, file_path = tempfile.mkstemp(suffix='_log_' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv', dir=os.path.join(settings.BASE_DIR, 'refunder/files'))

        return file_path

