from flask import Flask
from flask_restx import Resource, Api
from app.models import User, Post
from app.api_models import new_user_parser, new_post_parser
from app.database import db_session


app = Flask(__name__)
api = Api(app)

@api.route("/user")
class UserView(Resource):
    def get(self):
        users = User.query.all()
        result = []
        for user in users: 
            result.append(user.to_dict())

        return result

    @api.expect(new_user_parser)
    def post(self):
        payload = new_user_parser.parse_args()
        user = User(
            name=payload["name"],
            email=payload["email"]
        )
        db_session.add(user)
        db_session.commit()
        return {
            "message": f"User {user.name} created!"
        }


@api.route("/post")
class PostView(Resource):
    def get(self):
        posts = Post.query.all()
        result = []
        for post in posts: 
            result.append(post.to_dict())

        return result

    @api.expect(new_post_parser)
    def post(self):
        payload = new_post_parser.parse_args()
        post = Post(
            title=payload["title"],
            text=payload["text"]
        )
        db_session.add(post)
        db_session.commit()
        return {
            "message": f"Post {post.title} created!"
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
