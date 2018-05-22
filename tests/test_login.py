import unittest
from test_basecase import BaseCase
#from PyTube import db
from flask import url_for
#from PyTube.models import User
from flask_login import current_user

class LoginPage(BaseCase):
    def test_login_loads(self):
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200) 

    def test_login_template(self):
        result = self.client.get('/login')
        self.assert_template_used('login.html')

    def test_login_redirects(self):
        result = self.client.post('/login', data=self.loginForm)
        self.assertRedirects(result, url_for('index')) 

    def test_login_works(self):
        with self.client:
            result = self.client.post('/login', data=self.loginForm)
            self.assertEquals(current_user.username, "user")

    def test_login_rejects(self):
        loginForm_wrong_password = dict(username='user', email='user@email.com', password='hunter2')
        with self.client:
            result = self.client.post('/login', data=loginForm_wrong_password)
            self.assertTrue(current_user.is_anonymous)

    def test_login_flash_error(self):
        loginForm_wrong_password = dict(username='user', email='user@email.com', password='hunter2')
        result = self.client.post('/login', data=loginForm_wrong_password)
        with self.client.session_transaction() as sess:
            flash_message = dict(sess['_flashes'])

        expected_message = 'Invalid username or password'
        self.assertEqual(flash_message['message'], expected_message)

    def test_redirect_logged_in(self):
        with self.client:
            self.client.post('/login', data=self.loginForm)
            result = self.client.get('/login')
            self.assertRedirects(result, url_for('index')) 


      
