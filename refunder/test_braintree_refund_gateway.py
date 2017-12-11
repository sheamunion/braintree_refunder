from django.test import TestCase

import braintree

from .braintree_refund_gateway import BraintreeRefundGateway

class TestBraintreeRefundGateway(TestCase):

    def test_it_raises_when_invalid_keys_are_provided(self):
        DUMMY_KEYS = ['sandbox', 'merchant_id', 'public_key', 'private_key']

        try:
            gateway = BraintreeRefundGateway(DUMMY_KEYS)
        except TypeError as e:
            gateway = e

        self.assertIsInstance(gateway, TypeError)

    def test_it_configures_the_braintree_module(self):
        DUMMY_KEYS = ['sandbox', 'merchant_id', 'public_key', 'private_key']

        try:
            gateway = BraintreeRefundGateway(DUMMY_KEYS)
        except TypeError as e:
            gateway = e

        self.assertEqual(braintree.Configuration.environment, braintree.Environment.Sandbox) 
        self.assertEqual(braintree.Configuration.merchant_id, DUMMY_KEYS[1]) 
        self.assertEqual(braintree.Configuration.public_key, DUMMY_KEYS[2]) 
        self.assertEqual(braintree.Configuration.private_key, DUMMY_KEYS[3]) 
    

