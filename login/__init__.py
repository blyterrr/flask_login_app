
import os
from flask import Flask, request, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)
from flask import render_template, redirect, url_for
from login.forms import LoginForm, RegistrationForm
from login.db_helper import insert_user, check_exists, check_password


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if check_exists(form.username.data):
            if check_password(form.username.data, form.password.data):
                flash(
                    f'You are now logged in as {form.username.data}', 'success')
                return redirect(url_for('home'))
            else:  # password is incorrect
                flash(f'Incorrect password. Try again.', 'danger')
                return redirect(url_for('login'))
        else:
            flash(f'There is no user by that name.', 'danger')
            return redirect(url_for('login'))
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print('NOT VALIDATED YET')
    if form.validate_on_submit():
        if check_exists(form.username.data):
            flash(
                f'There is already a user created with the username {form.username.data}', 'danger')
            return redirect(url_for('register'))
        else:
            insert_user(form.username.data,
                        form.email.data, form.password.data)
            flash(
                f'Account created with username {form.username.data}', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)
