import os
import subprocess
from urllib import response

import requests
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import json
from dotenv import load_dotenv
from peewee import PostgresqlDatabase, Model, CharField,AutoField
from playhouse.db_url import connect
try:
    dircetory = "C:/project/instagram clone/Instagram-Video-Downloader-API"
    result = subprocess.Popen(["node","index.js"], cwd = dircetory)
    print("started on port 3000")
except Exception as e:
    print(f"failed to launch api: {e} ")




url = "https://www.instagram.com/p/DcB9mMpCGSv/"
query_params = {"url": url}
choice_1 = "what is this"
choice_2 = "what is this"
choice_3 = "what is this"
choice_4 = "pick me"

response = requests.get("http://localhost:3000/igdl", params=query_params)
data = response.json()
print(response.status_code)
print(response.json())

video_url = data['url']['data'][0]['url']
video_bytes = requests.get(video_url).content
with open("reel.mp4", "wb") as f:
    f.write(video_bytes)
load_dotenv()  

cloudinary.config(
    cloud_name=os.getenv('cloudinary'),
    api_key=os.getenv('cloudinary_api_key'),
    api_secret=os.getenv('cloudinary_api_secret')
)

try:
    uploaded_video = cloudinary.uploader.upload(
        "reel.mp4",
        resource_type="video"
    )
    print(uploaded_video)
    cloudinary_video_url = uploaded_video['url']
    print("Cloudinary Video URL:", cloudinary_video_url)
except Exception as e:
    print(f"Error uploading video: {e}")
try:
    load_dotenv()
    db_string = os.getenv('database')

# Crash cleanly with a clear explanation if it's missing
    if not db_string:
        raise ValueError("Error: The 'database' environment variable is not set!")

    db = connect(db_string)
except:
    print("failed to load database")

class User(Model):
    id = AutoField(primary_key=True)                  # Primary key column
    url = CharField(unique=True)
    choice_a = CharField()
    choice_b = CharField()
    choice_c = CharField()
    choice_d = CharField()
    correct_answer = CharField(max_length=1)  # Assuming the correct answer is a single character (e.g., 'A', 'B', 'C', or 'D')
    class Meta:
        database = db
        table_name = "videos"
db.connect() 
# Tells Postgres the current position is 0, so the NEXT item inserted will be 1


new_video = User(url=cloudinary_video_url, choice_a=choice_1, choice_b=choice_2, choice_c=choice_3, choice_d=choice_4, correct_answer="d")
new_video.save()
subprocess.Popen.terminate(result)
