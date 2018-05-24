import unittest
from PyTube import db
from flask import url_for
from PyTube.models import User, Media
from test_basecase import BaseCase

class UploadPage(BaseCase):
    def test_upload_page_loads(self):
        with self.client:
            self.client.post('/login', data=self.loginForm)
            result = self.client.get('/upload')
        self.assertEqual(result.status_code, 200) 

    def test_upload_page_template(self):
        with self.client:
            self.client.post('/login', data=self.loginForm)
            result = self.client.get('/upload')
        self.assert_template_used('upload.html')

    def test_upload_requires_login(self):
        result = self.client.get('/upload')
        self.assertEqual(result.status_code, 302)

    def test_upload_redirects_to_media(self):
        filename = open("./file.txt")
        uploadForm = dict(name='picture',media=filename)
        with self.client:
            self.client.post('/login', data=self.loginForm)
            result = self.client.post('/upload', data=uploadForm)
            self.assertRedirects(result, url_for('media')) 

#    def test_upload_creates_media(self):
#        result = self.client.post('/upload', data=self.uploadForm)
#        media = Media.query.filter_by(name=self.uploadForm['name']).first()
#        self.assertIsNotNone(media)
 
