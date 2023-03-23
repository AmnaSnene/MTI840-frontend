from flask import Flask, request, jsonify, render_template
import zmq
app = Flask(__name__)

'''
context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/temp/", methods=["POST"])
def temp():
    if request.is_json:
        data = request.get_json()
        socket.send(b'data["temperature"]')
        return jsonify({'msg': 'success', 'température': data["temperature"]})
    else:
        return "No JSON data in request"

if __name__ == '__main__':
    app.run()
