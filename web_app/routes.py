from flask import render_template, url_for, flash, redirect, request, abort
from web_app import app, db, bcrypt
from web_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from web_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image # external library to decrease size of pictures 

@app.route("/")
@app.route("/index")
def index():
    page = request.args.get("page", 1, type=int) # get the first page when index loads
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # DB QUERY, object creation and setting up pages, and ordering by latest post
    return render_template('index.html', title="Home page", posts=posts)

@app.route("/admin")
def admin():
    return render_template('admin.html',title="Admin page")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
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
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("No.","danger")
    return render_template('login.html', title="Login", form=form)

@app.route("/logout")
def logout():
        if current_user.is_authenticated:
            logout_user()
            return redirect(url_for("index"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # generates random name for pictures
    _, f_ext = os.path.splitext(form_picture.filename) # split filename and extension
    picture_fn = random_hex + f_ext # combine random and extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # creates a variable to store the pictures
    output_size = (125, 125) # sets avatar size, pixel
    i = Image.open(form_picture) # create object for Pillow to decrease size
    i.thumbnail(output_size) # creates new picture in Pillow
    i.save(picture_path) # saves picture to profile_pics
    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title="Your Account", image_file=image_file, form = form)

@app.route("/new/post", methods=['GET', 'POST']) # show this html and allow http requests
@login_required # import function that makes the user required to be logged in
def new_post():
    form = PostForm() # creating new object from the forms.py's postform Class
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) # create a DB entry with the data following
        db.session.add(post)
        db.session.commit()
        flash(f"Post has been successfully created", "success") # this is a Bootstrap thing
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")

@app.route("/post/<int:post_id>") # getting a variable from a DB, in this case the ID of the post
def post(post_id):
    post = Post.query.get_or_404(post_id) #creating a object from a database variable, if no post return template 404
    return render_template("post.html", title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id): # MODIFY POST
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # check if the user want to modify is the author
        abort(403)
    form = PostForm()
    if form.validate_on_submit(): # insert into DB
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f"Post has been successfully modified", "success") # this is a Bootstrap thing
        return redirect(url_for('index'))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post', form=form, legend="Update Post")

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id): #DELETE POST
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # check if the user want to modify is the author
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post has been successfully deleted", "alert")
    return redirect(url_for('index'))


@app.route("/user/<string:username>") # dynamic url from a variable
def user_posts(username):
    page = request.args.get("page", 1, type=int) # get the first page when index loads
    user = User.query.filter_by(username=username).first_or_404() # query the User DB and get the first item
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2) # DB QUERY, object creation and setting up pages, and ordering by latest post
    return render_template('user_posts.html', posts=posts, user=user)