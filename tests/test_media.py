import unittest
from PyTube.models import User, Media
from test_basecase import BaseCase

class TestMedia(BaseCase):
    def setUp(self):
        super(TestMedia, self).setUp()
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
    
        # Logged in client
        with self.client as self.logged_in:
            self.logged_in.post('/login', data=self.loginForm)
 
    def test_media_page_loads(self):
        self.logged_in.post('/upload', data=self.upload_txt)

        result = self.client.get('/media/1')
        self.assertEqual(result.status_code, 200) 

    def test_media_page_template(self):
        self.logged_in.post('/upload', data=self.upload_txt)
            
        result = self.client.get('/media/1')
        self.assert_template_used('media.html')

    def test_media_page_display_username(self):
        self.logged_in.post('/upload', data=self.upload_txt)
            
        result = self.client.get('/media/1')
        self.assertIn(self.user.username, str(result.data))

    def test_media_page_display_name(self):
        self.logged_in.post('/upload', data=self.upload_txt)
            
        result = self.client.get('/media/1')
        self.assertIn(self.upload_txt['name'], str(result.data))

    def test_media_display_jpg(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
            
        result = self.client.get('/media/1')
        self.assertIn("<img", str(result.data))
        self.assertIn("</img>", str(result.data))

    def test_media_display_mp4(self):
        self.logged_in.post('/upload', data=self.upload_mp4)
            
        result = self.client.get('/media/1')
        self.assertIn("<video", str(result.data))
        self.assertIn("</video>", str(result.data))

    def test_media_uses_picture(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
            
        result = self.client.get('/media/1')
        self.assertIn("<picture", str(result.data))
        self.assertIn("</picture>", str(result.data))

    def test_media_video_controls(self):
        self.logged_in.post('/upload', data=self.upload_mp4)
            
        result = self.client.get('/media/1')
        self.assertIn("controls", str(result.data))

    def test_media_username(self):
        self.logged_in.post('/upload', data=self.upload_mp4)

        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        self.assertEquals(media.user_id, self.user.id)

    def test_media_public(self):
        self.logged_in.post('/upload', data=self.upload_mp4)

        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        self.assertTrue(media.public)

    def test_media_public_set_false(self):
        upload_false = dict(name='false',media=self.mp4file, public=False)
        self.logged_in.post('/upload', data=upload_false)

        media = Media.query.filter_by(name=upload_false['name']).first()
        self.assertFalse(media.public)

    def test_media_viewcount(self):      
        self.logged_in.post('/upload', data=self.upload_mp4)

        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        self.assertEquals(media.viewcount, 0)
        result = self.client.get('/media/1')
        self.assertEquals(media.viewcount, 1)
        result = self.client.get('/media/1')
        self.assertEquals(media.viewcount, 2)

    def test_media_viewcount_display(self):      
        self.logged_in.post('/upload', data=self.upload_mp4)

        media = Media.query.filter_by(name=self.upload_mp4['name']).first()
        result = self.client.get('/media/1')
        self.assertIn("Views: ", str(result.data))
        self.assertIn(str(media.viewcount), str(result.data))

