from flask import Flask, render_template
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
# import os

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

class VideoModel(db.Model):
    video_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150), nullable=False)
    views = db.Column(db.Integer, nullable=False) 
    likes = db.Column(db.Integer, nullable=False) 

    def __repr__(self):
        return f"video(title= {self.title}, views= {self.views}, likes= {self.likes})"


# db.create_all()
# videos = [1:{"video_id":1,"title":"Test 1","views":1, "likes": 1}]
# videos = {}

#=====Put Arguement Parser=====
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("title",type=str,help="Title is required", required=True)
video_put_args.add_argument("views",type=int,help="views of the video",default=0)
video_put_args.add_argument("likes",type=int,help="likes of the video",default=0)

#=====Update Arguement Parser=====
video_upadte_args = reqparse.RequestParser()
video_upadte_args.add_argument("title",type=str,help="Title is required")
video_upadte_args.add_argument("views",type=int,help="views of the video")
video_upadte_args.add_argument("likes",type=int,help="likes of the video")

resource_fields = {
    'video_id': fields.Integer,
	'title': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}


class Video(Resource):

    @marshal_with(resource_fields)
    def get(self,video_id):
        result = VideoModel.query.filter_by(video_id=video_id).first()
        if not result:
            abort(404,message="Video Not Found")

        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        result = VideoModel.query.filter_by(video_id=video_id).first()
        if result:
            abort(409,message="Video_id already exists")

        args = video_put_args.parse_args()
        video = VideoModel(video_id=video_id,title = args['title'],views = args['views'], likes = args['likes'])
        db.session.add(video)        
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    def delete(self, video_id):
        result = VideoModel.query.filter_by(video_id=video_id).first()
        if not result:
            abort(404, message=f"Video with video id {video_id} doesn't exist. Cannot Delete!!")
    
        db.session.delete(result)
        db.session.commit()
        return result, 204

    @marshal_with(resource_fields)
    def patch(self,video_id):
        result = VideoModel.query.filter_by(video_id=video_id).first()
        if not result:
            abort(404, message=f"Video with video id {video_id} doesn't exist. Cannot Update!!")
        
        args = video_upadte_args.parse_args()
        
        if args["title"]:
            result.title= args['title']
        if args["views"]:
            result.views = args['views']
        if args["likes"]:
            result.likes = args['likes']
        
        db.session.commit()
        result = VideoModel.query.filter_by(video_id=video_id).first()
        return result

api.add_resource(Video,'/video/<int:video_id>')

if __name__ == "__main__":
    app.run(debug=False)