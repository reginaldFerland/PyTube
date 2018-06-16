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
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()

        result = browse(user=self.user, limit=1)
        self.assertEquals(len(result), 1)

    def test_get_most_recent_default(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        test = [media2 , media1]

        result = get_most_recent()
        self.assertEquals(result, test)

    def test_get_most_recent_private(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        test = [media2]

        result = get_most_recent()
        self.assertEquals(result, test)

    def test_get_most_recent_user(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        test = [media2, media1]

        result = get_most_recent(user=self.user)
        self.assertEquals(result, test)

    def test_get_most_recent_limit(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()

        result = get_most_recent(user=self.user, limit=1)
        self.assertEquals(len(result), 1)

    def test_get_most_recent_all(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        self.logged_in.post('/upload', data=self.extra1)
        media3 = Media.query.filter_by(id=3).first()
        self.logged_in.post('/upload', data=self.extra2)
        media4 = Media.query.filter_by(id=4).first()
        self.logged_in.post('/upload', data=self.extra3)
        media5 = Media.query.filter_by(id=5).first()
        expected = [media5, media4, media3, media2, media1]

        result = get_most_recent(user=self.user, limit=None)
        
        self.assertEquals(result, expected)

    def test_get_most_viewed_default(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        media2.increment_viewcount()
        test = [media2 , media1]

        result = get_most_viewed()
        self.assertEquals(result, test)

    def test_get_most_viewed_private(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        media1.increment_viewcount()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        test = [media2]

        result = get_most_viewed()
        self.assertEquals(result, test)

    def test_get_most_viewed_user(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        media2.increment_viewcount()
        test = [media2, media1]

        result = get_most_viewed(user=self.user)
        self.assertEquals(result, test)

    def test_get_most_viewed_limit(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        media2.increment_viewcount()

        result = get_most_viewed(user=self.user, limit=1)
        self.assertEquals(len(result), 1)
        self.assertEquals(result, [media2])

    def test_get_most_liked_default(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        media2.like(self.user)
        test = [media2 , media1]

        result = get_most_liked()
        self.assertEquals(result, test)

    def test_get_most_liked_private(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        media1.like(self.user)
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        test = [media2]

        result = get_most_liked()
        self.assertEquals(result, test)

    def test_get_most_liked_user(self):
        self.upload_jpg['public'] = False
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        media2.like(self.user)
        test = [media2, media1]

        result = get_most_liked(user=self.user)
        self.assertEquals(result, test)

    def test_get_most_liked_limit(self):
        self.logged_in.post('/upload', data=self.upload_jpg)
        media1 = Media.query.filter_by(id=1).first()
        self.logged_in.post('/upload', data=self.upload_mp4)
        media2 = Media.query.filter_by(id=2).first()
        media2.like(self.user)

        result = get_most_liked(user=self.user, limit=1)
        self.assertEquals(len(result), 1)
        self.assertEquals(result, [media2])

