from bson import ObjectId, SON
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/deepersystemstube") #host uri
db = client.deepersystemstube                           #Select the database
todos = db.videos

class VideoController():
  def list_videos(self):
    try:
      return todos.find()
    except Exception as e:
      print(e)
  
  def publish_video(self, name, theme, url_video):
    try:
      todos.insert({"name": name, "theme": theme, "like": 0, "deslike": 0, "url_video": url_video})

      return True
    except Exception as e:
      print(e)

  def apresentation_video(self, _id):
    try:
      video = todos.find_one({"_id": ObjectId(_id)})
      videos = todos.find({"_id": { "$ne":  ObjectId(_id)}})

      return {"video": video, "videos": videos}
    except Exception as e:
      print(e)

  def like(self, _id):
    try:
      _id = {"_id":  ObjectId(_id)}

      video = todos.find_one(_id)
      like = { "$set": { "like": video['like'] + 1 } }

      todos.update_one(_id, like)

      return True
    except Exception as e:
      print(e)
  
  def dislike(self, _id):
    try:
      _id = {"_id":  ObjectId(_id)}

      video = todos.find_one(_id)
      like = { "$set": { "deslike": video['deslike'] + 1 } }

      todos.update_one(_id, like)

      return True
    except Exception as e:
      print(e)
  
  def list_trending(self):
    theme_list = todos.find()
    video_list = todos.find()

    def get_my_key(obj):
      return obj['score']
      
    theme = []
    data = []
    score = []

    for themes in theme_list:
      theme.append(themes['theme'])

    for video in video_list:
      like = int(video['like'])
      deslike = int(video['deslike'])
      data.append({"theme": video['theme'],"scores":like - (deslike / 2)})

    theme = sorted(set(theme))

    for t in theme:
      scores = 0
      for d in data:
        if t == d['theme']:
          scores = scores + float(d['scores'])
          
      score.append({"theme": t, "score": scores})

    score.sort(key=get_my_key)
    score.reverse()

    return score