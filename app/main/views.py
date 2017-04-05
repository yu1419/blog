from . import main
from ..models import PostModel
a = PostModel()


@main.route("/")
def index():
    result = a.breif_post()
    return str(result)


@main.route("/user=<int:user_id>")
def user_post(user_id):
    result = a.by_user(user_id)
    return str(result)


@main.route("/post_id=<int:post_id>")
def post_byID(post_id):
    result = a.by_postID(post_id)
    return str(result)
