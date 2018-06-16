import unittest
from PyTube.models import User, Media, browse, get_most_recent, get_most_viewed, get_most_liked
from test_basecase import BaseCase

class TestHome(BaseCase):
    def setUp(self):
        super(TestHome, self).setUp()
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

    def test_recent_uploads_page_loads(self):
        result = self.client.get('/recent_uploads') 
        self.assertEqual(result.status_code, 200) 

    def test_recent_uploads_page_template(self):
        result = self.client.get('/recent_uploads')
        self.assert_template_used('view_all.html')

    def test_most_viewed_page_loads(self):
        result = self.client.get('/most_viewed') 
        self.assertEqual(result.status_code, 200) 

    def test_most_viewed_page_template(self):
        result = self.client.get('/most_viewed')
        self.assert_template_used('view_all.html')

    def test_most_liked_page_loads(self):
        result = self.client.get('/most_liked') 
        self.assertEqual(result.status_code, 200) 

    def test_most_liked_page_template(self):
        result = self.client.get('/most_liked')
        self.assert_template_used('view_all.html')

     

