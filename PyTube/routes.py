from PyTube import app, db
from flask import render_template, redirect, url_for, flash, send_from_directory, send_file
from PyTube.forms import RegistrationForm, LoginForm, UploadForm
from PyTube.models import User, Media, browse, get_most_recent, get_most_viewed, get_most_liked
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os.path

# Error handling, will eventually be refactored into seporate file
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/')
@app.route('/index')
def index():
    user = None
    if current_user.is_authenticated:
        user = current_user
    recent_uploads = get_most_recent(user=user)
    most_viewed = get_most_viewed(user=user)
    most_liked = get_most_liked(user=user) 
    return render_template('index.html', recent_uploads=recent_uploads, most_viewed=most_viewed, most_liked=most_liked)

@app.route('/recent_uploads')
def view_recent_uploads():
    user = None
    if current_user.is_authenticated:
        user = current_user
    return render_template('view_all.html', header="Recent Uploads", media=get_most_recent(user, limit=None))

@app.route('/most_viewed')
def view_most_viewed():
    user = None
    if current_user.is_authenticated:
        user = current_user
    return render_template('view_all.html', header="Most Viewed", media=get_most_viewed(user, limit=None))

@app.route('/most_liked')
def view_most_liked():
    user = None
    if current_user.is_authenticated:
        user = current_user
    return render_template('view_all.html', header="Most Liked", media=get_most_liked(user, limit=None))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # User doesn't exist or password wrong, flash error
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        # Handle upload logic
        newFile = form.media.data
        path = app.config['UPLOAD_FOLDER']
        name = form.name.data
        userID = current_user.id
        public = form.public.data
        media = Media(name=name, type=newFile.mimetype, user_id=current_user.id, public=public, description=form.description.data)
        media.save()
        
        ext = os.path.splitext(newFile.filename)[1]

        fullpath = path + str(media.id) + ext
        media.path = fullpath

        # Save media
        newFile.save(media.path)
        media.save() # Save after newFile so that only saves if no exceptions/crash 

        # Flash sucessful upload
        flash('Media Uploaded!')
        
        # Redirect to uploaded file
        return redirect(url_for('media', mediaID=media.id))
    return render_template('upload.html', form=form)

@app.route('/media/<int:mediaID>')
def media(mediaID):
    media = Media.query.filter_by(id=mediaID).first_or_404()
    path = media.path
    type = media.type
    if 'image' in type:
        type = 'image'
    elif 'video' in type:
        type = 'video'
    elif 'text' in type:
        type = 'text'

    user = User.query.filter_by(id=media.user_id).first()
    media.increment_viewcount()
    likes = media.get_likes()
    return render_template('media.html', media=media, username=user.username, likes=likes)

@app.route('/files/<int:mediaID>')
def files(mediaID):
    media = Media.query.filter_by(id=mediaID).first_or_404()
    path = media.path
    return send_file(path) # send_from_directory(media.path)

@app.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html', user=user)

@app.route('/like/<int:mediaID>', methods=['POST'])
@login_required
def like(mediaID):
    media = Media.query.filter_by(id=mediaID).first()
    if media.is_liked(user=current_user):
        media.unlike(user=current_user)
    else:
        media.like(user=current_user)
    return redirect(url_for('media', mediaID=media.id))
