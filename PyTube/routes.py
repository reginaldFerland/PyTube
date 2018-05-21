from PyTube import app
from flask import render_template, redirect, url_for
from PyTube.forms import RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
