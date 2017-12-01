import os

class ConfigurationUtility:

    def __init__(self, keys):
        self.keys = keys
    
    def store_keys(self):
        os.environ["BT_MERCHANT_ID"] = self.keys[0]
        os.environ["BT_PUBLIC_KEY"]  = self.keys[1]
        os.environ["BT_PRIVATE_KEY"] = self.keys[2]
        return
