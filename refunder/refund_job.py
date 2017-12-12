from datetime import datetime
from django.conf import settings
import csv, os, tempfile

import braintree

from .braintree_refund_gateway import BraintreeRefundGateway
from .transaction_loader import TransactionLoader

class RefundJob():

    def __init__(self, keys, source_file = None):
        self.gateway = BraintreeRefundGateway(keys)
        self.transaction_loader = TransactionLoader(source_file)

    def run(self, merchant_id, log_file = None):
        transactions = self.transaction_loader.all()
        if not log_file:
            log_file = self.__create_log_file(merchant_id)
        txn_refund_logs = []

        for txn in transactions:
            txn_refund_logs.append(self.gateway.find_void_or_refund(txn))

        with open(log_file, 'w', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(['transaction_id','refunded_transaction_id','status','message'])
            for log in txn_refund_logs:
                log_writer.writerow([log[0],log[1],log[2],log[3]])
            log_file.close()
    
        log_file_name = os.path.basename(log_file.name)
        return log_file_name

    def __create_log_file(self, merchant_id):
        _, file_path = tempfile.mkstemp(prefix=merchant_id + '_', suffix='_log_' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.csv', dir=os.path.join(settings.BASE_DIR, 'refunder/files'))

        return file_path

