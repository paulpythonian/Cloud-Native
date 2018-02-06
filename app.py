from flask import Flask, jsonify, make_response, abort, request, render_template, session, redirect, url_for
from flask_cors import CORS, cross_origin
import json
import sqlite3
from time import strftime, gmtime
import pymongo
import random

connection = pymongo.MongoClient("mongodb://hsb0104:paul371621@cloud-native-cluster-shard-00-00-p1dsn.mongodb.net:27017,cloud-native-cluster-shard-00-01-p1dsn.mongodb.net:27017,cloud-native-cluster-shard-00-02-p1dsn.mongodb.net:27017/test?ssl=true&replicaSet=cloud-native-cluster-shard-0&authSource=admin")
def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'cloud_native' not in dbnames:
            db = connection.cloud_native.user
            db_tweets = connection.cloud_native.tweets
            db_api = connection.cloud_native.apirelease

            db.insert({
                "email": "sungbin.hong@icloud.com",
                "id": 32,
                "name": "Sung Bin Hong",
                "password": "@#psbH371621",
                "username": "hsb0104"
            })
            db_tweets.insert({
            "body": "New blog post,Launch your app with the AWS Startup Kit!  # AWS",
            "id": 18,
            "timestamp": "2017-03-11T06:39:40Z",
            "tweetedby": "eric.strom"
            })

            db_api.insert({
            "buildtime": "2017-01-01 10:00:00",
            "links": "/api/v1/users",
            "methods": "get, post, put, delete",
            "version": "v1"
            })
            db_api.insert({
            "buildtime": "2017-02-11 10:00:00",
            "links": "api/v2/tweets",
            "methods": "get, post",
            "version": "2017-01-10 10:00:00"
            })
            print("Database Initialize completed!")
        else:
            print("Database already Initialized")
    except:
        print("Database creation failed!")

app = Flask(__name__)
app.secret_key ='alsdfoiwjoij32oro23ro2nwanfownonlfksoi'
CORS(app)


def list_users():
    api_list = []
    db = connection.cloud_native.user
    for row in db.find():
        api_list.append(str(row))
    return jsonify({"user_list": api_list})



def list_user(user_id):
    api_list = []
    db = connection.cloud_native.users
    for i in db.find({'id': user_id}):
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'user_details': api_list})

def add_user(new_user):
    api_list = []
    print(new_user)
    db = connection.cloud_native.user
    user = db.find({'$or': [{"username":new_user['username']},
                            {"email":new_user['email']}]})
    for i in user:
        print(str(i))
        api_list.append(str(i))

    if api_list == []:
        db.insert(new_user)
        return "Success"
    else:
        abort(409)



def del_user(del_user):
    conn = sqlite3.connect('mydb.db')
    print('Opened database successfully')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users where username=?", (del_user,))
    data = cursor.fetchall()
    print("Data", data)
    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("DELETE FROM users where username=?", (del_user,))
        conn.commit()
        return "Success"


def upd_user(user):
    conn = sqlite3.connect('mydb.db')
    print('Opened database successfully');
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user['id'],))
    data = cursor.fetchall()
    print(data)
    if len(data) == 0:
        abort(404)
    else:
        key_list = user.keys()
        for i in key_list:
            if i != "id":
                print(user, i)
                cursor.execute("UPDATE users SET {0}=? WHERE id = ?".format(i), (user[i], user['id']))
                conn.commit()
        return "Success"



### tweet functions

def list_all_tweets():
    conn = sqlite3.connect('mydb.db')
    print("Opened database successfully")
    api_list = []
    cursor = conn.execute("SELECT username, body, tweet_time, id FROM tweets")
    data = cursor.fetchall()
    if data != 0:
        print('if runs')
        for row in data :
            tweets = {}
            tweets['Tweet By'] = row[0]
            tweets['Body'] = row[1]
            tweets['Timestamp'] = row[2]
            tweets['id'] = row[3]
            print("tweets:", tweets)
            api_list.append(tweets)
    else:
        print('else runs')
        return jsonify({'tweets_list':api_list})
    conn.close()
    return jsonify({'tweets_list': api_list})

def add_tweet(new_tweets):
    conn = sqlite3.connect('mydb.db')
    print("Opened database successfully")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (new_tweets['username'],))
    data = cursor.fetchall()

    if len(data) == 0:
        abort(404)
    else:
        cursor.execute("INSERT into tweets (username, body, tweet_time) VALUES (?,?,?)", (new_tweets['username'], new_tweets['body'], new_tweets['created_at']))
        conn.commit()
        return "Success"


def list_tweet(user_id):
    print(user_id)
    conn = sqlite3.connect('mydb.db')
    print("Opened database successfully")
    api_list = []
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tweets WHERE id=?', (user_id,))
    data = cursor.fetchall()
    print(data)
    if len(data) == 0:
        abort(400)
    else:
        user = {}
        user['id'] = data[0][0]
        user['username'] = data[0][1]
        user['body'] = data[0][2]
        user['tweet_time'] = data[0][3]
        api_list.append(user)
    conn.close()
    return jsonify({'tweet':api_list})





@app.route('/')
def main():
    return render_template('main.html')

@app.route('/addname')
def addname():
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        return redirect(url_for('main'))
    else:
        return render_template('addname.html', session=session)


@app.route('/adduser')
def adduser():
    return render_template('adduser.html')


@app.route('/addtweets')
def addtweetjs():
    return render_template('addtweets.html')

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('main'))





@app.route("/api/v1/info")
def home_index():
    api_list = []
    db = connection.cloud_native.apirelease
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'api_version': api_list}),200


@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users()


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)


@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)

    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json.get('name', ''),
        'password': request.json['password'],
        'id': random.randint(1, 1000)
    }
    return jsonify({'status': add_user(user)}), 201

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200


@app.route('/api/v1/users/<int:user_id>', methods={'PUT'})
def update_user(user_id):
    user = {}
    if not request.json:
        print(request.json)
        abort(400)
    user['id']=user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print(user)
    return jsonify({'status': upd_user(user)}),200




### Tweet routes

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_all_tweets()


@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet['username'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['created_at'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    print(user_tweet)
    return jsonify({'status': add_tweet(user_tweet)}), 200


@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def list_tweets(id):
    return list_tweet(id)


















@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)

@app.errorhandler(400)
def invaild_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    create_mongodatabase()
    app.run(host='0.0.0.0', port=8000, debug=True)

