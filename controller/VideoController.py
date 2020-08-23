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
    