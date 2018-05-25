import unittest
#from PyTube import db
#from flask import url_for
#from PyTube.models import User, Media
from test_basecase import BaseCase
#import os.path


class TestMedia(BaseCase):
    def setUp(self):
        super(TestMedia, self).setUp()
        # Files and upload forms
        # Text file
        self.textfile = open("./tests/files/upload_file.txt")
        self.upload_txt = dict(name='picture',media=self.textfile)
        # Picture file
        self.jpgfile = open("./tests/files/upload_picture.jpg", mode='rb')
        self.upload_jpg = dict(name='picture',media=self.jpgfile)
 
        # Video file
        self.mp4file = open("./tests/files/upload_video.mp4", mode='rb')
        self.upload_mp4 = dict(name='video',media=self.mp4file)
 
    def test_media_page_loads(self):
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.upload_txt)

        result = self.client.get('/media/1')
        self.assertEqual(result.status_code, 200) 

    def test_media_page_template(self):
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.upload_txt)
            
        result = self.client.get('/media/1')
        self.assert_template_used('media.html')

    def test_media_display_jpg(self):
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.upload_jpg)
            
        result = self.client.get('/media/1')
        self.assertIn("<img", str(result.data))
        self.assertIn("</img>", str(result.data))

    def test_media_display_mp4(self):
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.upload_mp4)
            
        result = self.client.get('/media/1')
        self.assertIn("<video", str(result.data))
        self.assertIn("</video>", str(result.data))

    def test_media_uses_picture(self):
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.upload_jpg)
            
        result = self.client.get('/media/1')
        self.assertIn("<picture", str(result.data))
        self.assertIn("</picture>", str(result.data))

    def test_media_video_controls(self):
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.upload_mp4)
            
        result = self.client.get('/media/1')
        self.assertIn("controls", str(result.data))


