# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect

import os

from controller.VideoController import VideoController 

import random

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = set(['mp4'])

# config import
from config import app_config, app_active

config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app = Flask(__name__, static_folder='static')

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    @app.route('/')
    def list_videos():
      videos = VideoController()
      data = videos.list_videos()

      return render_template('feed.html',videos= data)

    def allowed_file(filename):
      return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @app.route('/publish_video', methods=['POST'])
    def insert_video():
      video = VideoController()

      name= request.form['name']
      theme= request.form['theme']
      file = request.files['file']
      if file and allowed_file(file.filename):
        filename = str(random.getrandbits(128))+file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
      
      status = video.publish_video(name, theme, filename)

      if status:
        return redirect('/')

      return redirect('/publish')
    
    @app.route('/video')
    def apresentation_video():
      video = VideoController()
      key = request.args.get("_id")
      
      data = video.apresentation_video(key)
      print(data)
      return render_template('video.html',video=data['video'], videos=data['videos'])

    @app.route('/publish')
    def publish_videos():
      return render_template('publish_video.html')

    @app.route('/like')
    def like_video():
      video = VideoController()

      key = request.args.get("_id")
      
      video.like(key)

      return redirect('/video?_id='+key)

    @app.route('/dislike')
    def deslike_video():
      video = VideoController()
      key = request.args.get("_id")

      video.dislike(key)
      
      return redirect('/video?_id='+key)

    @app.route('/trending')
    def list_trending():
      video = VideoController()

      score = video.list_trending()

      return render_template('trending.html',videos=score)

    return app