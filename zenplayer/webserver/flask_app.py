from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello from ZenPlayer"


@app.route('/play_pause')
def play_pause():
    """
    Play or pause the currently active player.
    ---
    tags:
        - ZenPlayer
    responses:
        200:
            description: Success if we have played or paused the current player.
    """
    return "play_pause"


