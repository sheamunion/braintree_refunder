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

    def test_POST_to_refund_redirects_to_refunding_page(self):
        dummy_file = os.path.join(settings.BASE_DIR, 'functional_tests/dummy_source.csv')
        with open(dummy_file) as fp:
            response = self.client.post('/refund', {'environment': 'sandbox', 'merchant_id': 'asdf', 'public_key': 'asdf', 'private_key': 'asdf', 'source_csv': fp})
        
        self.assertRedirects(response, '/refunding')
    
    def test_POST_to_refund_with_invalid_data_renders_new_refund_page(self):
        response = self.client.post('/refund')

        self.assertIn('What type of account is this?', (response.content).decode('utf-8'))
        self.assertIn('start_refund', (response.content).decode('utf-8'))
