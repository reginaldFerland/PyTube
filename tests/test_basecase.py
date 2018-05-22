#! venv/bin/python3
from datetime import datetime, timedelta
import unittest
from PyTube import app, db
from flask_testing import TestCase
from flask import url_for
from PyTube.models import User

class BaseCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        self.client = app.test_client()
        # Register data
        self.registerForm = dict(username='tester', email='e@e.com', password='pass', password2='pass')
        
        # Existing user
        user = User(username='user', email='user@email.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        self.loginForm = dict(username='user', email='user@email.com', password='password')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class HomePage(BaseCase):
    def test_home_page_loads(self):
        result = self.client.get('/') 
        self.assertEqual(result.status_code, 200) 

    def test_home_page_template(self):
        result = self.client.get('/')
        self.assert_template_used('index.html')


if __name__ == '__main__':
    unittest.main(verbosity=2)
