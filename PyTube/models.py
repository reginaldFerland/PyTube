from PyTube import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# Creating many to many 
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about = db.Column(db.String(256))
    join_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def follow(self, user):
        if self.is_following(user):
            raise Exception("already following")
        self.followed.append(user)
        db.session.commit()
        
    def unfollow(self, user):
        if not self.is_following(user):
            raise Exception("not following")
        self.followed.remove(user)
        db.session.commit()
 

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def get_followers(self):
        return self.followed.all()

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    path = db.Column(db.String(128), index=True, unique=True)
    type = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    public = db.Column(db.Boolean)
    viewcount = db.Column(db.Integer, default=0)

    def increment_viewcount(self):
        self.viewcount = self.viewcount + 1
        db.session.commit()

    def __repr__(self):
        return '<Media {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def user_exists(username):
    if User.query.filter_by(username=username).first() is None:
        return False
    else:
        return True
