from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello from ZenPlayer"


@app.route('/play_pause')
def play_pause():
    return "play_pause"


