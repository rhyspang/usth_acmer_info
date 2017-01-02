from flask import Flask, jsonify
import json

from flask import render_template

app = Flask(__name__)


@app.route('/data/')
def hello_world():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
