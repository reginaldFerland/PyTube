#! venv/bin/python3
from datetime import datetime, timedelta
import unittest
from PyTube import app, db
from flask_testing import TestCase

class BaseCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page_loads(self):
        result = self.client.get('/') 
        self.assertEqual(result.status_code, 200) 

    def test_home_page_template(self):
        result = self.client.get('/')
        self.assert_template_used('index.html')

#    def test_register(self):

#    def test_login(self):

#    def test_logout(self):



if __name__ == '__main__':
    unittest.main(verbosity=2)
