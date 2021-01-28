from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"
#db.create_all() #we only create it once and just after the VideoModel has been created, after that we delete it.

#names = {"nando": {"age": 29, "gender": "male"}, "Paco": {"age": 35, "gender": "male"}}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str,help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int,help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int,help="Likes on the video is required", required=True)


video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str,help="Name of the video is required")
video_update_args.add_argument("views", type=int,help="Views of the video is required")
video_update_args.add_argument("likes", type=int,help="Likes on the video is required")


#videos = {}

#def abort_if_video_id_doesnt_exist(video_id):
#    if video_id not in videos:
#        abort(404, message="Couldnt find video, please review the video_id...")

#def abort_if_video_exists(video_id):
#    if video_id in videos:
#        abort(409, message="Video already exists with that ID.")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        #abort_if_video_id_doesnt_exist(video_id)
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        return result
    @marshal_with(resource_fields)
    def put(self, video_id):
        #abort_if_video_exists(video_id)
        #args = video_put_args.parse_args()
        #videos[video_id] = args
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if result:
            abort(409, message = "Video id taken...")
        video = VideoModel(id = video_id, name = args['name'], views = args['views'], likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return result


    def delete(self, video_id):
        #abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204




#class HelloWorld(Resource):
#    def get(self, name):
#        return names[name]

#    def post(self):
#        return {"data": "Posted"} # in our test.py we could use response = requests.post(BASE + "helloworld") instead of .get

#api.add_resource(HelloWorld, "/helloworld/<string:name>")

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)