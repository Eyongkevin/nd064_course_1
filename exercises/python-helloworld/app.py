from flask import Flask, jsonify, make_response
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/status')
def status():
    data = {"result": "Ok - healthy"}
    return make_response(jsonify(data), 200)

@app.route('/metrics')
def metric():
    data = {"UserCount": 140, "UserCountActive": 23}
    return make_response(jsonify(data), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
