from flask import Flask, jsonify, make_response
import logging

app = Flask(__name__)

@app.route("/")
def hello():
    app.logger.info("main endpoint was reached")
    return "Hello World!"

@app.route('/status')
def status():
    app.logger.info("status endpoint was reached")
    data = {"result": "Ok - healthy"}
    return make_response(jsonify(data), 200)

@app.route('/metrics')
def metric():
    app.logger.info("metric endpoint was reached")
    data = {"UserCount": 140, "UserCountActive": 23}
    return make_response(jsonify(data), 200)


if __name__ == "__main__":
    logging.basicConfig(filename="app.log", level=logging.DEBUG)
    app.run(host='0.0.0.0')
