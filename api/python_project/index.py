from flask import Flask, jsonify, request, abort
import flask_sqlalchemy as fsql
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

HOSTNAME = '' # Host of your databases, e.g. 'localhost'
PORT = '' # Port of your databases, e.g. '3306'
DATABASE = '' # Name of your databases
USERNAME = '' # User's name of your databases
PASSWORD = '' # Password of your databases

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = fsql.SQLAlchemy(app)

valid_token = '' # (Optional) for token validation

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.Integer)
    subtype = db.Column(db.Integer)
    text = db.Column(db.Text)
    is_send = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)
    url = db.Column(db.Text)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    app_name = db.Column(db.Text)
    refer_text = db.Column(db.Text)
    artist = db.Column(db.Text)
    link_url = db.Column(db.Text)
    website_name = db.Column(db.Text)

    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

@app.route('/QueryByKeyword')
def querybykeywords():
    token = request.args.get('token')
    if(token!=valid_token):
        abort(403)
    key_word = request.args.get('key')
    page = int(request.args.get('page'))
    pagesize = int(request.args.get('pagesize'))
    offset = (page-1)*pagesize
    limit = pagesize
    sql = "SELECT * FROM `message` WHERE (text LIKE '%{}%') LIMIT {},{}".format(key_word, offset, limit)
    result_list = []
    size = 14
    keys = Message.__table__.columns.keys()
    result = db.session.execute(db.text(sql)).all()
    for item in result:
        new_dict = {}
        for i in range(size):
            new_dict[keys[i]] = item[i]
        result_list.append(new_dict)
    db.session.remove()
    return jsonify({"code":"200", "data":result_list})

@app.route('/QueryByTime')
def querybytime():
    token = request.args.get('token')
    if(token!=valid_token):
        abort(403)
    start_time = int(request.args.get('start'))
    end_time = int(request.args.get('end'))
    page = int(request.args.get('page'))
    pagesize = int(request.args.get('pagesize'))
    offset = (page-1)*pagesize
    limit = pagesize
    sql = "SELECT * FROM `message` WHERE (timestamp>={} and timestamp<{}) LIMIT {},{}".format(start_time, end_time, offset, limit)
    result_list = []
    size = 14
    keys = Message.__table__.columns.keys()
    result = db.session.execute(db.text(sql)).all()
    for item in result:
        new_dict = {}
        for i in range(size):
            new_dict[keys[i]] = item[i]
        result_list.append(new_dict)
    db.session.remove()
    return jsonify({"code":"200", "data":result_list})
    
if __name__=="__main__":
    app.debug = False
    app.run(port=2020,host="0.0.0.0")
    
