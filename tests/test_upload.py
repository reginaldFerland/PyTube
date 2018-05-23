import unittest
from PyTube import db
from flask import url_for
from PyTube.models import User, Media
from test_basecase import BaseCase

class UploadPage(BaseCase):
    def test_upload_page_loads(self):
        result = self.client.get('/upload')
        self.assertEqual(result.status_code, 200) 

    def test_upload_page_template(self):
        result = self.client.get('/upload')
        self.assert_template_used('upload.html')


