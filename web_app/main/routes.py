from flask import render_template, request, Blueprint
from web_app.models import Post


main = Blueprint("main", __name__)

@main.route("/")
@main.route("/index")
def index():
    page = request.args.get("page", 1, type=int) # get the first page when index loads
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) # DB QUERY, object creation and setting up pages, and ordering by latest post
    return render_template('index.html', title="Home page", posts=posts)