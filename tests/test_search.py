import unittest
from PyTube.models import User, Media, search
from test_basecase import BaseCase

class TestSearch(BaseCase):
    def setUp(self):
        super(TestSearch, self).setUp()
        # Files and upload forms
        # Text file
        self.textfile = open("./tests/files/upload_file.txt")
        self.upload_txt = dict(name='picture',media=self.textfile, public=True)

        # Picture file
        self.jpgfile = open("./tests/files/upload_picture.jpg", mode='rb')
        self.upload_jpg = dict(name='picture',media=self.jpgfile, public=True)
 
        # Video file
        self.mp4file = open("./tests/files/upload_video.mp4", mode='rb')
        self.upload_mp4 = dict(name='video',media=self.mp4file, public=True)

        # For extras
        self.jpgfile = open("./tests/files/upload_picture.jpg", mode='rb')
        self.extra1 = dict(name='picture',media=self.jpgfile, public=True)
        self.jpgfile = open("./tests/files/upload_picture.jpg", mode='rb')
        self.extra2 = dict(name='picture',media=self.jpgfile, public=True)
        self.jpgfile = open("./tests/files/upload_picture.jpg", mode='rb')
        self.extra3 = dict(name='picture',media=self.jpgfile, public=True)
        self.jpgfile = open("./tests/files/upload_picture.jpg", mode='rb')
        self.extra4 = dict(name='picture',media=self.jpgfile, public=True)
    
        # Logged in client
        with self.client as self.logged_in:
            self.logged_in.post('/login', data=self.loginForm)

        self.logged_in.post('/upload', data=self.upload_jpg)
        self.logged_in.post('/upload', data=self.upload_mp4)
        self.logged_in.post('/upload', data=self.extra1)
        self.logged_in.post('/upload', data=self.extra2)
        self.logged_in.post('/upload', data=self.extra3)
        self.logged_in.post('/upload', data=self.extra4)

    def test_search(self):
        result = search("picture")
        self.assertEquals(len(result), 5)
        result = search("video")
        self.assertEquals(len(result), 1)

