from flask import Flask

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def say_hello():
    """Returns a friendly hello"""
    return {"msg": "Hello from Flask"}
