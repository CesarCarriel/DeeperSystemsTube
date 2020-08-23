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