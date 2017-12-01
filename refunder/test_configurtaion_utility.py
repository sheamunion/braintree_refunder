from django.test import TestCase
import os

from refunder.configuration_utility import ConfigurationUtility

class ConfigurationUtilityTest(TestCase):

    DUMMY_KEYS = ['merchant_id', 'public_key', 'private_key']

    def test_it_sets_api_DUMMY_KEYS_as_env_variables(self):
        config_util = ConfigurationUtility(self.DUMMY_KEYS)

        self.assertEqual(os.environ['BT_MERCHANT_ID'], self.DUMMY_KEYS[0])
        self.assertEqual(os.environ['BT_PUBLIC_KEY'], self.DUMMY_KEYS[1])
        self.assertEqual(os.environ['BT_PRIVATE_KEY'], self.DUMMY_KEYS[2])

    # def test_it_creates_a_braintree_gateway_object(self):
    #     config_util = ConfigurationUtility(self.DUMMY_KEYS)

    #     config_util.load(self.DUMMY_KEYS)

    #     assert(
