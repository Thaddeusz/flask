from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from web_app import db, bcrypt
from web_app.models import User, Post
from web_app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from web_app.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            bcrypt
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.index"))
        else:
            flash("No.","danger")
    return render_template('login.html', title="Login", form=form)

@users.route("/logout")
def logout():
        if current_user.is_authenticated:
            logout_user()
            return redirect(url_for("main.index"))


@users.route("/account", methods=['GET', 'POST'])
@login_required # calls the login_required decorator (function)
def account(): # this is the func that the base html for_url calls
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title="Your Account", image_file=image_file, form = form)


@users.route("/user/<string:username>") # dynamic url from a variable
def user_posts(username):
    page = request.args.get("page", 1, type=int) # get the first page when index loads
    user = User.query.filter_by(username=username).first_or_404() # query the User DB and get the first item
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2) # DB QUERY, object creation and setting up pages, and ordering by latest post
    return render_template('user_posts.html', posts=posts, user=user)



@users.route("/reset_password", methods=['GET', 'POST']) # this is the password reset request page, where you put in your email
def reset_request():
    if current_user.is_authenticated: # check if a pw reset request is valid (user not logged in already)
        return redirect(url_for("main.index"))
    form = RequestResetForm() # if valid, creates request reset form object and pass it to the html
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Check your email inbox", "info")
        return redirect(url_for("main.index"))
    return render_template('reset_request.html', title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST']) # creates a dynamic url based on a token
def reset_token(token):
    if current_user.is_authenticated: 
        return redirect(url_for("main.index"))
    user = User.verify_reset_token(token) # this is a function in the models.py, the actual token generation and user check
    if user is None:
        flash("Invalid token", 'warning')
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm() # if token is right, creates a reset password form object
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_pw
        db.session.commit()
        flash(f"Your password has been updated!", "success")
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)



@users.route("/admin")
def admin():
    return render_template('admin.html',title="Admin page")