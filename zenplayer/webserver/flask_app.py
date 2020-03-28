from flask import Flask


app = Flask(__name__)


class ZenWebController:
    """
    Main class dispatching commands to the active ZenPlayer controller object.
    """
    ctrl = None
    """
    Reference to the controller object.
    """
    @staticmethod
    def set_controller(ctrl):
        ZenWebController.ctrl = ctrl

    @staticmethod
    @app.route('/')
    def index():
        return "Hello from ZenPlayer"

    @staticmethod
    @app.route('/play_pause')
    def play_pause():
        """
        Play or pause the currently active player.
        ---
        tags:
            - ZenPlayer
        responses:
            200:
                description: Success if we have played or paused the current
                             player.
        """
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: ZenWebController.ctrl.play_pause())
        # ZenWebController.ctrl.play_pause()
        return "play_pause"


