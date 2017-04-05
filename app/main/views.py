from . import main
from ..models import PostModel
a = PostModel()


@main.route("/")
def index():
    result = str(a.breif_post())
    return "<p>hello%s</p>" % (result)


@main.route("/<int:user_id>")
def user_post(user_id):
    result = a.by_user(user_id)
    return str(result)
