# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect

from bson import ObjectId

import os

import random

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = set(['mp4'])

# config import
from config import app_config, app_active

config = app_config[app_active]

from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/deepersystemstube") #host uri
db = client.deepersystemstube                           #Select the database
todos = db.videos

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app = Flask(__name__, static_folder='static')

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    @app.route('/')
    def list_videos():
      data = todos.find()

      return render_template('videos.html',videos= data)

    def allowed_file(filename):
      return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @app.route('/register_video', methods=['POST'])
    def insert_video():
      name= request.form['name']
      theme= request.form['theme']
      file = request.files['file']
      if file and allowed_file(file.filename):
        #filename = secure_filename(file.filename)
        filename = str(random.getrandbits(128))+file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

      todos.insert({"name": name, "theme": theme, "like": 0, "deslike": 0, "url_video": filename})

      return redirect('/')
    
    @app.route('/video')
    def view_video():
      key = request.args.get("_id")
      video = todos.find_one({"_id": ObjectId(key)})
      data = todos.find({"_id": { "$ne":  ObjectId(key)}})
      print(data)
      #data = todos.find(ne)

      return render_template('video.html',video=video, videos= data)

    @app.route('/publish')
    def publish_videos():
      data = todos.find()
      print(data)

      return render_template('publish_video.html')

    @app.route('/like')
    def like_video():
      key = request.args.get("_id")
      id = {"_id":  ObjectId(key)}

      video = todos.find_one(id)
      like = { "$set": { "like": video['like'] + 1 } }

      todos.update_one(id, like)
      return redirect('/video?_id='+key)

    @app.route('/deslike')
    def deslike_video():
      key = request.args.get("_id")
      id = {"_id":  ObjectId(key)}

      video = todos.find_one(id)
      deslike = { "$set": { "deslike": video['deslike'] + 1 } }

      todos.update_one(id, deslike)
      return redirect('/video?_id='+key)

    return app
