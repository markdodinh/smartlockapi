from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

open_requests = {}

@app.route('/open', methods = ['POST'])
def open():
    data = request.get_json()
    locker = data.get('locker', None)
    if locker is not None and 'user' in data:
        open_requests[int(locker)] = data['user']
        return('', 200)
    else:    
        return('', 400)

@app.route('/open', methods = ['GET'])
def poll_open():
    locker = request.args.get('locker', None, int)
    if locker is not None and locker in open_requests:
        return jsonify(username = open_requests[locker])
    return('', 204)