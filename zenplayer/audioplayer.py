from kivy.clock import Clock
from kivy.logger import Logger
from kivy.core.audio import SoundLoader


class Sound(object):
    """
    This class manages the playing audio as a Singleton
    """
    state = ""  # options= "", "stopped" or "playing", "seeking"
    _state_callbacks = []
    _sound = None  # The underlying Sound instance

    @staticmethod
    def _on_stop(*_args):
        Sound._set_state("stopped")

    @staticmethod
    def _set_state(state):
        """ Set the state value and fire all attached callbacks """
        print(f"_set_state fired: {state}.")
        if state != Sound.state:
            Sound.state = state
            for func in Sound._state_callbacks:
                func(state)

    @staticmethod
    def add_state_callback(callback):
        """ Add a callback to be fired when the state changes """
        Sound._state_callbacks.append(callback)

    @staticmethod
    def get_pos_length():
        """ Return a tuple of the length and position, or return 0, 0"""
        sound = Sound._sound
        if sound:
            try:
                return sound.get_pos(), sound._get_length()
            except Exception as e:
                Logger.warn("audioplayer.py: Failed to load sound, {0}".format(
                    e))
                return 0, 0
        else:
            return 0, 0

    @staticmethod
    def seek(pos):
        """ Set the sound to the specified position """
        if Sound._sound:
            Sound._sound.seek(pos)

    @staticmethod
    def stop():
        """ Stop any playing audio """
        if Sound._sound and Sound.state != "seeking":
            Sound._sound.stop()

    @staticmethod
    def play(filename="", volume=100):
        """
        Play the file specified by the filename. If on_stop is passed in,
        this function is called when the sound stops
        """
        Sound.stop()

        if filename:
            Sound._sound = SoundLoader.load(filename)
        if Sound._sound:
            print(f"Playing sound {filename}")
            Sound._sound.bind(on_stop=Sound._on_stop)
            Sound._sound.play()
            Sound._sound.volume = volume
            Sound._set_state("playing")

        else:
            Sound._set_state("")

    @staticmethod
    def set_position(value):
        """
        The position of the currently playing sound as a fraction between 0
        and 1.
        """
        sound = Sound._sound
        if sound:
            Clock.schedule_once(lambda dt: sound.seek(value * sound.length))
            Clock.schedule_once(lambda dt: sound.play())

    @staticmethod
    def set_volume(value):
        """ The volume of the currently playing sound. """
        if Sound._sound:
            Sound._sound.volume = value
