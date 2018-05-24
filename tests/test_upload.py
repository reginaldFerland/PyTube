import unittest
from PyTube import db
from flask import url_for
from PyTube.models import User, Media
from test_basecase import BaseCase
import os.path

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
        filename = open("./tests/upload_file.txt")
        uploadForm = dict(name='picture',media=filename)
        with self.client:
            self.client.post('/login', data=self.loginForm)
            result = self.client.post('/upload', data=uploadForm)
            self.assertRedirects(result, url_for('media')) 

    def test_upload_creates_media(self):
        filename = open("./tests/upload_file.txt")
        uploadForm = dict(name='text',media=filename)
        with self.client:
            self.client.post('/login', data=self.loginForm)
            result = self.client.post('/upload', data=uploadForm)
            media = Media.query.filter_by(name=uploadForm['name']).first() 
            self.assertIsNotNone(media)
           
    def test_upload_uses_correct_name(self):
        filename = open("./tests/upload_file.txt")
        uploadForm = dict(name='text',media=filename)
        with self.client:
            self.client.post('/login', data=self.loginForm)
            result = self.client.post('/upload', data=uploadForm)
            media = Media.query.filter_by(name=uploadForm['name']).first() 
            self.assertEquals(media.name, uploadForm['name'])

    def test_upload_creates_file(self):
        filename = open("./tests/upload_file.txt")
        uploadForm = dict(name='text',media=filename)
        with self.client:
            self.client.post('/login', data=self.loginForm)
            result = self.client.post('/upload', data=uploadForm)
            media = Media.query.filter_by(name=uploadForm['name']).first() 
        self.assertTrue(os.path.exists(media.path))
        self.assertTrue(os.path.isfile(media.path))



