import unittest
from PyTube import db
from flask import url_for
from PyTube.models import User, user_exists, followers
from test_basecase import BaseCase
from datetime import datetime

class TestProfile(BaseCase):
    def setUp(self):
        super(TestProfile, self).setUp()

        with self.client as self.logged_in:
            self.logged_in.post('/login', data=self.loginForm)
 
    def test_profile_form(self):
        result = self.logged_in.get('/user/user') 
        self.assertIn('textarea', str(result.data))
        self.client.get('/logout')
        result = self.client.get('/user/user')
        self.assertNotIn('textarea', str(result.data))
