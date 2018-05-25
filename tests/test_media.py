import unittest
#from PyTube import db
#from flask import url_for
#from PyTube.models import User, Media
from test_basecase import BaseCase
#import os.path


class TestMedia(BaseCase):
    def test_media_page_loads(self):
        filename = open("./tests/files/upload_file.txt")
        self.uploadForm = dict(name='picture',media=filename)
 
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.uploadForm)

        result = self.client.get('/media/1')
        self.assertEqual(result.status_code, 200) 

    def test_media_page_template(self):
        filename = open("./tests/files/upload_file.txt")
        self.uploadForm = dict(name='picture',media=filename)
 
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.uploadForm)
            
        result = self.client.get('/media/1')
        self.assert_template_used('media.html')

    def test_media_display_jpg(self):
        filename = open("./tests/files/upload_picture.jpg", mode='rb')
        self.uploadForm = dict(name='picture',media=filename)
 
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.uploadForm)
            
        result = self.client.get('/media/1')
        self.assertIn("<img", str(result.data))
        self.assertIn("</img>", str(result.data))

    def test_media_display_mp4(self):
        filename = open("./tests/files/upload_video.mp4", mode='rb')
        self.uploadForm = dict(name='video',media=filename)
 
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.uploadForm)
            
        result = self.client.get('/media/1')
        self.assertIn("<video", str(result.data))
        self.assertIn("</video>", str(result.data))

    def test_media_uses_picture(self):
        filename = open("./tests/files/upload_picture.jpg", mode='rb')
        self.uploadForm = dict(name='picture',media=filename)
 
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.uploadForm)
            
        result = self.client.get('/media/1')
        self.assertIn("<picture", str(result.data))
        self.assertIn("</picture>", str(result.data))

    def test_media_video_controls(self):
        filename = open("./tests/files/upload_video.mp4", mode='rb')
        self.uploadForm = dict(name='video',media=filename)
 
        with self.client:
            self.client.post('/login', data=self.loginForm)
            self.client.post('/upload', data=self.uploadForm)
            
        result = self.client.get('/media/1')
        self.assertIn("controls", str(result.data))


