from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

open_requests = {}
access_control_list = {
    1 : 'user1'
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

    open_requests[lockerId] = username
    return('', 200)

@app.route('/open', methods = ['GET'])
def poll_open():
    locker = request.args.get('locker', None, int)
    username = open_requests.pop(locker, None)
    if username is not None:
        return jsonify(username = username)
    return('', 200)