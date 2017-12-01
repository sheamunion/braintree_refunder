from django.test import TestCase
import os

from refunder.configuration_utility import ConfigurationUtility

class ConfigurationUtilityTest(TestCase):

    def test_it_sets_api_keys_as_env_variables(self):
        keys = ['merchant_id', 'public_key', 'private_key']
        config_util = ConfigurationUtility(keys)
        config_util.store_keys()

        self.assertEqual(os.environ['BT_MERCHANT_ID'], keys[0])
        self.assertEqual(os.environ['BT_PUBLIC_KEY'], keys[1])
        self.assertEqual(os.environ['BT_PRIVATE_KEY'], keys[2])

    # def test_it_creates_a_braintree_gateway_object(self):
    #     config_util = ConfigurationUtil()

    #     config_util.load(keys)

    #     assert(
