from PyTube import app, db
from flask import render_template, redirect, url_for, flash
from PyTube.forms import RegistrationForm
from PyTube.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login')
def login():
    return render_template('login.html')
