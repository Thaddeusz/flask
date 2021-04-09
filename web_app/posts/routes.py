from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from web_app import db
from web_app.models import Post
from web_app.posts.forms import PostForm

posts = Blueprint("posts", __name__)

@posts.route("/new/post", methods=['GET', 'POST']) # show this html and allow http requests
@login_required # import function that makes the user required to be logged in
def new_post():
    form = PostForm() # creating new object from the forms.py's postform Class
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) # create a DB entry with the data following
        db.session.add(post)
        db.session.commit()
        flash(f"Post has been successfully created", "success") # this is a Bootstrap thing
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")

@posts.route("/post/<int:post_id>") # getting a variable from a DB, in this case the ID of the post
def post(post_id):
    post = Post.query.get_or_404(post_id) #creating a object from a database variable, if no post return template 404
    return render_template("post.html", title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post', form=form, legend="Update Post")

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id): #DELETE POST
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # check if the user want to modify is the author
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post has been successfully deleted", "alert")
    return redirect(url_for('main.index'))
