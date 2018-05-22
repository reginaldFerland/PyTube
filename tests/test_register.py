#! venv/bin/python3
import unittest
from PyTube import db
from flask import url_for
from PyTube.models import User
from tests import BaseCase

class RegisterPage(BaseCase):
    def test_register_loads(self):
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200) 

    def test_register_template(self):
        result = self.client.get('/register')
        self.assert_template_used('register.html')

    def test_register_redirects(self):
        result = self.client.post('/register', data=self.registerForm)
        self.assertRedirects(result, url_for('index')) 

    def test_register_creates_account(self):
        result = self.client.post('/register', data=self.registerForm)
        user = User.query.filter_by(username=self.registerForm['username']).first()
        self.assertIsNotNone(user)
        
    def test_password_hash(self):
        user = User(username="tester", email="email@email.com")
        user.set_password("password")
        self.assertFalse(user.check_password("hunter12"))
        self.assertTrue(user.check_password("password"))

    def test_flash_success(self):
        result = self.client.post('/register', data=self.registerForm, follow_redirects=True)
        with self.client.session_transaction() as sess:
            flash_message = dict(sess['_flashes'])

        expected_message = 'Congratulations, you are now a registered user!' 
        self.assertEqual(flash_message['message'], expected_message)

    #def test_duplicate_username(self):

    #def test_duplicate_email(self):


if __name__ == '__main__':
    unittest.main(verbosity=2)
