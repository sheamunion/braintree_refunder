from django.test import TestCase

from .forms import RefunderForm

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class RefundingPageTest(TestCase):

    def test_uses_refunding_template(self):
        response = self.client.post('/refunding')
        self.assertTemplateUsed(response, 'refunding.html')
