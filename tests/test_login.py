import unittest
from test_basecase import BaseCase
#from PyTube import db
#from flask import url_for
#from PyTube.models import User

class LoginPage(BaseCase):
    def test_login_loads(self):
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200) 


