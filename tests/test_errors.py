import unittest
from test_basecase import BaseCase
from PyTube import app

class TestHome(BaseCase):
    def setUp(self):
        super(TestHome, self).setUp()
 
    def test_404(self):
        result = self.client.get('/invalid_address-123zasv')
        self.assertEquals(result.status_code, 404)

    def test_404_template(self):
        result = self.client.get('/invalid_address-123zasv')
        self.assert_template_used('404.html')


