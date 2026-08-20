from bottle import route, run, request, static_file
from peewee import PostgresqlDatabase, Model, CharField,AutoField
from playhouse.db_url import connect
import os
from dotenv import load_dotenv
from bottle import hook, response

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With'



# Gets the absolute path of the folder where this script is saved
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

@route("/")
def hello():
    try:# Looks for "index.html" inside your project folder
        return static_file("index.html", root=PROJECT_ROOT)
    except:
        print("failed to load html")
@route("/script.js")
def script():
    try:
        return static_file("script.js",root=PROJECT_ROOT)
    except:
        print("failed to load js")



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


@route("/video",Method='get')
def getvideo():
    try:
        index=request.query.get('index')
        video = User.select(User.url).where(User.id == index).scalar()
        return {"video":video,"choice_a":User.select(User.choice_a).where(User.id == index).scalar(),"choice_b":User.select(User.choice_b).where(User.id == index).scalar(),"choice_c":User.select(User.choice_c).where(User.id == index).scalar(),"choice_d":User.select(User.choice_d).where(User.id == index).scalar(),"correct_answer":User.select(User.correct_answer).where(User.id == index).scalar()}
    except:
        print("failed server route")
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)