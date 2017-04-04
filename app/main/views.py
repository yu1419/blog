from . import main
from ..models import PostModel

@main.route("/")
def index():
    a = PostModel()
    result = str(a.get_post())
    return "<p>hello%s</p>" %(result)
