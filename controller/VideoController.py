from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/deepersystemstube") #host uri
db = client.deepersystemstube                           #Select the database
todos = db.videos

class VideoController():
  def list_videos(self):
    try:
      return todos.find()
    except Exception as e:
      print(3)