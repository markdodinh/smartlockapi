from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
CORS(app)

open_requests = {}
access_control_list = {
    1 : 'user1',
    2 : 'user2',
    3 : 'user3',
    4 : 'user4',
    5 : 'user5',
    6 : 'user6'
}

@app.route('/open', methods = ['POST'])
def open():
    data = request.get_json()
    locker = data.get('locker', None)
    
    if locker is None or 'user' not in data:
        return('', 400)

    username = data['user']
    lockerId = int(locker)
    
    if lockerId not in access_control_list or access_control_list[lockerId] != username:
        return('', 403)

    open_requests[lockerId] = (username, datetime.now())
    return('', 200)

@app.route('/open', methods = ['GET'])
def poll_open():
    locker = request.args.get('locker', None, int)
    username = ''
    if locker in open_requests:
        obj = open_requests[locker]
        if (datetime.now() - obj[1]).total_seconds() > 12:
            username = ''
        else:
            username = open_requests[locker][0]
    return jsonify(username = username)

@app.route('/list', methods = ['GET'])
def list():
    arr = {}
    for locker in access_control_list.keys():
        arr['locker' + str(locker)] = locker in open_requests
        if locker in open_requests:
            obj = open_requests[locker]
            if (datetime.now() - obj[1]).total_seconds() > 12:
                 arr['locker' + str(locker)] = False
    return jsonify(arr)