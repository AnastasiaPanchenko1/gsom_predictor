from flask import Flask, request

app = Flask(__name__)
@app.route("/")

def hello():
	return “Hello world”

if __name__ = '__main__':
	app.run(debug=True, port=5444, host='0.0.0.0')
