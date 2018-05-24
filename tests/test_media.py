import unittest
#from PyTube import db
#from flask import url_for
#from PyTube.models import User, Media
from test_basecase import BaseCase
#import os.path


class TestMedia(BaseCase):
    def test_media_page_loads(self):
        filename = open("./tests/upload_file.txt")
        self.uploadForm = dict(name='picture',media=filename)
 
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.uploadForm)
            result = self.client.get('/media/1')
        self.assertEqual(result.status_code, 200) 

    def test_media_page_template(self):
        filename = open("./tests/upload_file.txt")
        self.uploadForm = dict(name='picture',media=filename)
 
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.uploadForm)
            result = self.client.get('/media/1')
        self.assert_template_used('media.html')


