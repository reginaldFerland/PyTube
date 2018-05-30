import unittest
from PyTube import db
from flask import url_for
from PyTube.models import User, Media
from test_basecase import BaseCase
import os.path

class UploadPage(BaseCase):
    def setUp(self):
        super(UploadPage, self).setUp()
        # Logged in client
        with self.client as self.logged_in:
            self.logged_in.post('/login', data=self.loginForm)
 
    def test_upload_page_loads(self):
        result = self.client.get('/upload')
        self.assertEqual(result.status_code, 200) 

    def test_upload_page_template(self):
        result = self.client.get('/upload')
        self.assert_template_used('upload.html')

    def test_upload_requires_login(self):
        self.client.get('/logout')
        result = self.client.get('/upload')
        self.assertEqual(result.status_code, 302)

    def test_upload_redirects_to_media(self):
        filename = open("./tests/files/upload_file.txt")
        uploadForm = dict(name='picture',media=filename, public=True)
        result = self.client.post('/upload', data=uploadForm)
        media = Media.query.filter_by(name=uploadForm['name']).first() 
        self.assertRedirects(result, url_for('media', mediaID=media.id)) 

    def test_upload_creates_media(self):
        filename = open("./tests/files/upload_file.txt")
        uploadForm = dict(name='text',media=filename, public=True)
        result = self.client.post('/upload', data=uploadForm)
        media = Media.query.filter_by(name=uploadForm['name']).first() 
        self.assertIsNotNone(media)
           
    def test_upload_uses_correct_name(self):
        filename = open("./tests/files/upload_file.txt")
        uploadForm = dict(name='text',media=filename, public=True)
        result = self.client.post('/upload', data=uploadForm)
        media = Media.query.filter_by(name=uploadForm['name']).first() 
        self.assertEquals(media.name, uploadForm['name'])

    def test_upload_creates_file(self):
        filename = open("./tests/files/upload_file.txt")
        uploadForm = dict(name='text',media=filename, public=True)
        result = self.client.post('/upload', data=uploadForm)
        media = Media.query.filter_by(name=uploadForm['name']).first() 
        self.assertTrue(os.path.exists(media.path))
        self.assertTrue(os.path.isfile(media.path))

    def test_upload_flash_message(self):
        filename = open("./tests/files/upload_file.txt")
        uploadForm = dict(name='text',media=filename, public=True)
        result = self.client.post('/upload', data=uploadForm)
            
        with self.client.session_transaction() as sess:
            flash_message = dict(sess['_flashes'])

        expected_message = 'Media Uploaded!' 
        self.assertEqual(flash_message['message'], expected_message)


