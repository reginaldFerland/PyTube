from PyTube import app, db
from flask import render_template, redirect, url_for, flash, send_from_directory, send_file
from PyTube.forms import RegistrationForm, LoginForm, UploadForm
from PyTube.models import User, Media, browse
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os.path

@app.route('/')
@app.route('/index')
def index():
    user = None
    if current_user.is_authenticated:
        user = current_user
    media_list = browse(user=user)
    return render_template('index.html', media_list=media_list)

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
        db.session.add(media)
        db.session.commit()
        
        ext = os.path.splitext(newFile.filename)[1]

        fullpath = path + str(media.id) + ext
        media.path = fullpath
        db.session.add(media)
        db.session.commit()
        # Save media
        newFile.save(media.path)

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
    return render_template('media.html', media=media, username=user.username)

@app.route('/files/<int:mediaID>')
def files(mediaID):
    media = Media.query.filter_by(id=mediaID).first_or_404()
    path = media.path
    return send_file(path) # send_from_directory(media.path)

@app.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html', user=user)
