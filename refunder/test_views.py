from django.conf import settings
from django.test import TestCase
import glob
import os

from .forms import RefunderForm

class NewRefundPageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_uses_refunder_from(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], RefunderForm)

class RefundPageTest(TestCase):

    def tearDown(self):
        for f in glob.glob(os.path.join(settings.BASE_DIR, 'refunder/files/*')):
            os.remove(f)
    
    def test_POST_to_refund_with_invalid_data_renders_new_refund_page(self):
        response = self.client.post('/refund')

        self.assertIn('What type of account is this?', (response.content).decode('utf-8'))
        self.assertIn('start_refund', (response.content).decode('utf-8'))

    def test_POST_with_invalid_keys_redirects_to_home_page(self):
        dummy_file = os.path.join(settings.BASE_DIR, 'functional_tests/dummy_source.csv')

        with open(dummy_file) as fp:
            response = self.client.post('/refund', {'environment': 'sandbox', 'merchant_id': 'asdf', 'public_key': 'asdf', 'private_key': 'asdf', 'source_csv': fp})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('start_refund', (response.content).decode('utf-8'))

    def test_POST_to_refund_with_valid_data_redirects_to_refunding_page(self):
        dummy_file = os.path.join(settings.BASE_DIR, 'functional_tests/dummy_source.csv')
        VALID_KEYS = [os.getenv("BT_ENVIRONMENT"), os.getenv("BT_MERCHANT_ID"), os.getenv("BT_PUBLIC_KEY"), os.getenv("BT_PRIVATE_KEY")]        

        with open(dummy_file) as fp:
            response = self.client.post('/refund', {'environment': VALID_KEYS[0], 'merchant_id': VALID_KEYS[1], 'public_key': VALID_KEYS[2], 'private_key': VALID_KEYS[3], 'source_csv': fp})

        self.assertRedirects(response, '/refunding')


