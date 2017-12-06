from datetime import datetime
from django.conf import settings
import os
import tempfile

import braintree

from .braintree_refund_gateway import BraintreeRefundGateway
from .transaction_loader import TransactionLoader

class RefundJob():

    def __init__(self, keys):
        self.__configure(keys)

    def __configure(self, keys):
        if keys[0] == "sandbox":
            return braintree.Environment.Sandbox
        else:
            return braintree.Environment.Production

        braintree.Configuration.configure(
            bt_environment,
            merchant_id = os.environ["BT_MERCHANT_ID"],
            public_key = os.envrion["BT_PUBLIC_KEY"],
            private_key = os.environ["BT_PRIVATE_KEY"],
        )

    def run(self, source_file, log_file = None):
        transactions = TransactionLoader(source_file).all()
        if not log_file:
            log_file = self.__create_log_file()
        txn_refund_logs = []

        for txn in transactions:
            txn_refund_logs.append(BraintreeRefundGateway.refund(txn))

        with open(log_file, "r+") as log_file:
            log_file.write("transaction_id,refund_transaction_id,status,message")
            for log in txn_refund_logs:
                log_file.write("{},{},{},{}".format(log["transaction_id"], log["refund_transaction_id"], log["status"], log["message"]))
                log_file.close()

    def __create_log_file(self):
        handle, file_path = tempfile.mkstemp(suffix="_log_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv", dir=os.path.join(settings.BASE_DIR, "refunder/files"))

        return file_path

