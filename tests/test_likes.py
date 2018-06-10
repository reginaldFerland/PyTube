import unittest
from PyTube.models import User, Media
from test_basecase import BaseCase
from flask import url_for

class TestLikes(BaseCase):
    def setUp(self):
        super(TestLikes, self).setUp()
        # Files and upload forms
        # Text file
        self.textfile = open("./tests/files/upload_file.txt")
        self.upload_txt = dict(name='picture',media=self.textfile, description="A description", public=True)
        # Picture file
        self.jpgfile = open("./tests/files/upload_picture.jpg", mode='rb')
        self.upload_jpg = dict(name='picture',media=self.jpgfile, public=True)
 
        # Video file
        self.mp4file = open("./tests/files/upload_video.mp4", mode='rb')
        self.upload_mp4 = dict(name='video',media=self.mp4file, public=True)
    
        # Logged in client
        with self.client as self.logged_in:
            self.logged_in.post('/login', data=self.loginForm)

        self.logged_in.post('/upload', data=self.upload_mp4)

    def test_media_likes(self):      
        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        self.assertEquals(media.get_likes(), 0)
        self.logged_in.post('/like/1')
        result = self.client.get('/media/1')
        self.assertEquals(media.get_likes(), 1)

    def test_media_likes_display(self):      
        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        result = self.client.get('/media/1')
        self.assertIn("Likes: ", str(result.data))
        self.assertIn(str(media.viewcount), str(result.data))

    def test_like_route(self):
        result = self.logged_in.post('/like/1')
        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        self.assertRedirects(result, url_for('media', mediaID=media.id)) 

    def test_like_requires_login(self):
        self.client.get('/logout')
        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        pre_like = media.get_likes()
        result = self.client.post('/like/1')
        self.assertEqual(pre_like, media.get_likes())

    def test_double_likes(self):
        self.logged_in.post('/like/1')
        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        self.assertEqual(media.get_likes(), 1)
        with self.assertRaises(Exception):
            self.logged_in.post('/like/1')

    # Unlike
    def test_unlike(self):
        self.logged_in.post('/like/1')
        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        self.assertEqual(media.get_likes(), 1)
        media.unlike(self.user)
        self.assertEqual(media.get_likes(), 0)
