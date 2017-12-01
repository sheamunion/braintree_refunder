import os

class ConfigurationUtility:

    def __init__(self, keys):
        os.environ["BT_MERCHANT_ID"] = keys[0]
        os.environ["BT_PUBLIC_KEY"]  = keys[1]
        os.environ["BT_PRIVATE_KEY"] = keys[2]
        
