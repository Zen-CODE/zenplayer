# from kivy.clock import Clock
# from kivy.logger import Logger
from vlc import MediaPlayer


class Sound(object):
    """
    This class manages the playing audio as a Singleton
    """
    state = ""  # options= "", "stopped" or "playing"
    _state_callbacks = []
    _player = None  # Reference to the underlying vlc instance


    @staticmethod
    def _set_state(state):
        """ Set the state value and fire all attached callbacks """
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
        # TODO
        # sound = Sound._sound
        # if sound:
        #     try:
        #         return sound.get_pos(), sound._get_length()
        #     except Exception as e:
        #         Logger.warn("audioplayer.py: Failed to load sound, {0}".format(
        #             e))
        #         return 0, 0
        # else:
        #     return 0, 0

    @staticmethod
    def seek(position):
        """ Set the sound to the specified position """
        # TODO
        # if Sound._sound:
        #     length = Sound._sound._get_length()
        #     if length > 0:
        #         print(f"Setting pos to {position * length}")
        #         Sound._sound.seek(position * length)

    @staticmethod
    def stop():
        """ Stop any playing audio """
        # TODO
        # if Sound._sound:
        #     Sound._sound.stop()
        #     Sound._sound.unload()

    @staticmethod
    def play(filename, volume=100, pos=0.0):
        """
        Play the file specified by the filename. If on_stop is passed in,
        this function is called when the sound stops
        """
        if Sound._player is not None:
            Sound._player.stop()

        Sound._player = player = MediaPlayer(filename)
        player.play()
        # TODO: Volume and pos settings


        # TODO
        # Sound.stop()

        # if filename:
        #     Sound._sound = SoundLoader.load(filename)
        # if Sound._sound:
        #     print(f"Playing sound {filename}")
        #     Sound._sound.bind(on_stop=Sound._on_stop)
        #     Sound._sound.play()
        #     Sound._sound.volume = volume
        #     if pos > 0.0:
        #         print(f"Seeking {pos}")
        #         Clock.schedule_once(lambda dt: Sound.seek(pos))

        #     Sound._set_state("playing")

        # else:
        #     Sound._set_state("")

    @staticmethod
    def set_position(value):
        """
        The position of the currently playing sound as a fraction between 0
        and 1.
        """
        # TODO
        # sound = Sound._sound
        # if sound:
        #     sound.seek(value * sound.length)

    @staticmethod
    def set_volume(value):
        """ The volume of the currently playing sound. """
        # TODO
        # if Sound._sound:
        #     Sound._sound.volume = value


if __name__ == "__main__":
    from time import sleep

    def test_cb(state):
        """ Test function for state callbacks """
        print(f"state changed: {state}")

    Sound.add_state_callback(test_cb)
    Sound.play("/home/fruitbat/Music/50 Cent/Get Rich Or Die Tryin'/"
               "05 - In Da Club.mp3")
    sleep(5000)


   # import vlc
    # from time import sleep

    # player = vlc.MediaPlayer("/home/fruitbat/Music/50 Cent/Get Rich Or Die Tryin'/05 - In Da Club.mp3")
    # player.play()
    # sleep(20)

