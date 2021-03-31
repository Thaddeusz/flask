from flask import render_template, url_for, flash, redirect
from web_app import app, db, bcrypt
from web_app.forms import RegistrationForm, LoginForm
from web_app.models import User, Post
from flask_login import login_user

@app.route("/")
@app.route("/index")
def index():
    user = { 'username' : 'Phillip'}
    posts = [
        {
            'author': "John",
            'title' : "First post",
            'date'  : "Today",
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': "Susan",
            'title' : "Second post",
            'date'  : "Today",
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',title="Home page", user=user, posts=posts)

@app.route("/admin")
def admin():
    return render_template('admin.html',title="Admin page")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("index"))
        else:
            flash("No.","danger")
    return render_template('login.html', title="Login", form=form)
