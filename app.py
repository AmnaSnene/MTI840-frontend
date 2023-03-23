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
# intialisation
temp, max_temp = 0, 0
ingredient = ''

@app.route('/')
def index():
    return render_template('index.html', temp=temp, max_temp=max_temp, ingredient=ingredient)


@app.route("/temp/", methods=["POST"])
def publish_temperature():
    if request.is_json:
        data = request.get_json()
        global temp, max_temp
        temp = data["temperature"]
        max_temp = data["temperature_max"]
        return jsonify({'msg': 'success', 'température': temp})
    else:
        return "No JSON data in request"
@app.route("/ingredient/", methods=["POST"])
def publish_ingredient():
    if request.is_json:
        data = request.get_json()
        global ingredient
        ingredient = data["ingredient"]
        return jsonify({'msg': 'success', 'ingredient': ingredient})
    else:
        return "No JSON data in request"

if __name__ == '__main__':
    app.run()
