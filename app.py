from flask import Flask, render_template, request
from peewee import *
import datetime

db = SqliteDatabase('posts.db')
class Post(Model):
    id = PrimaryKeyField()
    date = DateTimeField(default = datetime.datetime.now)
    text = TextField()

    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Post], safe=True)

app = Flask(__name__)

@app.before_request
def before_request():
    initialize_db()

@app.teardown_request
def teardown_request(exception):
    db.close()
    Post.delete()
    
@app.route('/')
@app.route('/send', methods=['GET','POST'])
def send():
    if request.method == 'POST':
        Post.create(
            text = request.form['words']
        )
        return render_template('index.html',posts=Post.select().order_by(Post.date.desc()))

    return render_template('index.html',posts=Post.select().order_by(Post.date.desc()))

if __name__ == "__main__":
    app.run(debug=True)

  
