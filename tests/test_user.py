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
