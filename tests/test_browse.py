import unittest
from PyTube.models import User, Media, browse, get_most_recent
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
    
        # Logged in client
        with self.client as self.logged_in:
            self.logged_in.post('/login', data=self.loginForm)

    def test_home_page_loads(self):
        result = self.client.get('/') 
        self.assertEqual(result.status_code, 200) 

    def test_home_page_template(self):
        result = self.client.get('/')
        self.assert_template_used('index.html')

    def test_browse_default(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        test = [media1 , media2]

        result = browse()
        self.assertEquals(result, test)

    def test_browse_private(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        test = [media2]

        result = browse()
        self.assertEquals(result, test)

    def test_browse_user(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        test = [media1, media2]

        result = browse(user=self.user)
        self.assertEquals(result, test)

    def test_browse_limit(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()

        result = browse(user=self.user, limit=1)
        self.assertEquals(len(result), 1)

    def test_get_most_recent(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        test = [media2, media1]

        result = get_most_recent(user=self.user)
        self.assertEquals(result, test)


    #def test_get_most_recent_limit(self):
