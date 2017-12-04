from datetime import datetime
from django.conf import settings
import os
import tempfile

import braintree

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

    def run(self, source_file):
        source_file = source_file
        log_file = self.create_log_file()
        return

    def create_log_file(self):
        handle, file_path = tempfile.mkstemp(suffix="_log_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv", dir=os.path.join(settings.BASE_DIR, "refunder/files"))
        with open(file_path, 'r+') as log_file:
            log_file.write('Original Txn ID,Refund Txn ID,Error Message')
        log_file.close()
        return file_path

