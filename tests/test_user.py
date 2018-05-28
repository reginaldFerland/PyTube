import unittest
from PyTube import db
from flask import url_for
from PyTube.models import User, user_exists, followers
from test_basecase import BaseCase

class TestUser(BaseCase):
    def setUp(self):
        super(TestUser, self).setUp()

    def test_user_exists(self):
        self.assertTrue(user_exists("user"))
        self.assertFalse(user_exists("bob"))
       
    def test_user_save(self):
        user = User(username="bob", email="bob@bob.com")
        user.set_password("hunter2")
        self.assertFalse(user_exists("bob"))
        user.save()

        self.assertTrue(user_exists("bob"))

    def test_user_follow(self):
        bob = User(username="bob", email="bob@bob.com")
        bob.set_password("hunter2")
        bob.save()
        bob.follow(self.user)
        
        self.assertTrue(bob.followed.filter(followers.c.followed_id == self.user.id).count() > 0)
        self.assertTrue(bob.followed.all()[0].username == "user")

    def test_user_follow_duplicate(self):
        bob = User(username="bob", email="bob@bob.com")
        bob.set_password("hunter2")
        bob.save()
        bob.follow(self.user)
        
        with self.assertRaises(Exception):
            bob.follow(self.user)

    def test_user_is_following(self):
        bob = User(username="bob", email="bob@bob.com")
        bob.set_password("hunter2")
        bob.save()

        self.assertFalse(bob.is_following(self.user))
        bob.follow(self.user)
        self.assertTrue(bob.is_following(self.user))
 
    def test_user_unfollow(self):
        bob = User(username="bob", email="bob@bob.com")
        bob.set_password("hunter2")
        bob.save()

        bob.follow(self.user)
        self.assertTrue(bob.is_following(self.user))
        bob.unfollow(self.user)
        self.assertFalse(bob.is_following(self.user))
        
    def test_user_unfollow_error(self):
        bob = User(username="bob", email="bob@bob.com")
        bob.set_password("hunter2")
        bob.save()
        
        with self.assertRaises(Exception):
            bob.unfollow(self.user)

    def test_user_get_followers(self):
        bob = User(username="bob", email="bob@bob.com")
        bob.set_password("hunter2")
        bob.save()

        user2 = User(username="user2", email="user2@email.com")
        user2.set_password("hunter2")
        user2.save()
  
        bob.follow(self.user)
        bob.follow(user2)
        
        self.assertTrue(bob.get_followers() == [self.user, user2])
             

    def test_user_page_loads(self):
        result = self.client.get('/user/{}'.format(self.user.username))
        self.assertEqual(result.status_code, 200) 

    def test_user_page_template(self):
        result = self.client.get('/user/{}'.format(self.user.username))
        self.assert_template_used('user_profile.html')

    def test_user_about(self):
        self.user.about = "ABOUT STUFF"
        db.session.commit()
        result = self.client.get('/user/{}'.format(self.user.username))
        self.assertIn(self.user.about, str(result.data))

       
