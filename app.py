from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungle9


app = Flask(__name__)

@app.route('/')
def home():
   users = db.users.find()
   return render_template('main.html', users = users)



if __name__ == '__main__':  
   app.run('0.0.0.0', port=5000, debug=True)


