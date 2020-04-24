"""
This module houses a VLC audio component that supports the Kivy `Sound`
interface.
"""
from kivy.core.audio import Sound, SoundLoader
from vlc import MediaPlayer, EventType, Instance
from kivy.clock import mainthread


class VLCSound(Sound):
    '''
    A Kivy `Sound` object based on a VLC audio backend.
    '''

    @staticmethod
    def extensions():
        return ("mp3", "mp4", "flac", "mkv", "wav", "ogg", "m4a")

    def __init__(self, **kwargs):
        self._mediaplayer = None
        self._state = ""
        self._length = 0
        super().__init__(**kwargs)

    @mainthread
    def _track_finished(self, *args):
        """ Event fired when the track is finished. """
        if not self.loop:
            self.stop()
        else:
            self.seek(0.)
            self._mediaplayer.play()

    def _unload_vlc(self):
        """ Unload the VLC Media player if it not already unloaded """
        if self._mediaplayer is not None:
            self._mediaplayer.event_manager().event_detach(
                EventType.MediaPlayerEndReached)
            self._mediaplayer.stop()
        self._state = ""

    def load(self):
        """ Loads the Media player for the suitable `source` filename """
        self._unload_vlc()
        media = Instance().media_new(self.source)
        media.parse()  # Determine duration

        player = self._mediaplayer = media.player_new_from_media()
        player.event_manager().event_attach(
            EventType.MediaPlayerEndReached, self._track_finished)

        self._set_volume(self.volume)
        self._length = media.get_duration() / 1000.0
        self._state = 'paused'

    def unload(self):
        """ Unload any instances of the player """
        self._unload_vlc()

    def play(self):
        """ Play the audio file """
        if self._state == 'playing':
            super().play()
            return
        if self._mediaplayer is None:
            self.load()

        self._mediaplayer.play()
        self._state = 'playing'
        self.state = 'play'
        super().play()

    def stop(self):
        """ Stop any currently playing audio file """
        if self._mediaplayer and self._state == 'playing':
            self._mediaplayer.pause()
            self._state = 'paused'
            self.state = 'stop'
        super().stop()

    def seek(self, position):
        """ Set the player to the given position in second """
        if self._mediaplayer:
            value = position / self._length
            self._mediaplayer.set_position(value)

    def get_pos(self):
        """ Return the position of int the currently playing track """
        if self._mediaplayer is not None and self._state == "playing":
            return self._mediaplayer.get_position() * self._length
        return 0

    def on_volume(self, instance, volume):
        """ Respond to the setting of the volume """
        self._set_volume(volume)

    def _set_volume(self, value):
        """
        The volume of the currently playing sound, where the value is between
        0 and 1.
        """
        if self._mediaplayer:
            vol = 100 if abs(value) >= 1.0 else 100 * abs(value)
            self._mediaplayer.audio_set_volume(int(vol))

    def _get_length(self):
        """ Getter method to fetch the track length """
        return self._length


if __name__ == "__main__":
    from time import sleep

    file = "/home/fruitbat/Music/Various/Music With Attitude/04 - " \
           "dEUS - Everybody's Weird.mp3"
    if True:
        sound = VLCSound(source=file)
        sound.load()
    else:
        # Legit Kivy sound
        sound = SoundLoader.load(file)
    if sound:
        print("Loaded sound")
        sound.volume = 0.5
        sound.play()
        sound.seek(10)

        i = 0
        while True:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            print("Position is %.3f seconds" % sound.get_pos())
            sleep(2)
            i += 1

        sound.stop()
        sleep(2)
        sound.play()
        sleep(2)
    else:
        print("Failed to load sound")

    # from kivy.app import App
    # from kivy.uix.label import Label

    # class TestApp(App):
    #     def build(self):
    #         return Label(text="Test")

    # TestApp().run()