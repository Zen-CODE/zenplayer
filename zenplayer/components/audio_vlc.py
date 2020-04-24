"""
This module houses a VLC audio component that supports the Kivy `Sound`
interface.
"""
from kivy.core.audio import Sound, SoundLoader
from vlc import MediaPlayer, EventType
from kivy.clock import mainthread
\

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
        player = self._mediaplayer = MediaPlayer(self.source)
        player.event_manager().event_attach(
            EventType.MediaPlayerEndReached, self._track_finished)
        self._set_volume(self.volume)
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
            value = position / (self._mediaplayer.get_length() / 1000.0)
            self._mediaplayer.set_position(value)

    def get_pos(self):
        """ Return the position of int the currently playing track """

        if self._mediaplayer is not None:
            return self._mediaplayer.get_position()
        return 0

    def on_volume(self, instance, volume):
        self.set_volume(volume)

    def _set_volume(self, value):
        """
        The volume of the currently playing sound, where the value is between
        0 and 1.
        """
        if self._mediaplayer:
            vol = 100 if abs(value) >= 1.0 else 100 * abs(value)
            self._mediaplayer.audio_set_volume(int(vol))

    def _get_length(self):
        if self._mediaplayer is not None:
            return self._mediaplayer.get_length() / 1000.0
        return super()._get_length()


if __name__ == "__main__":
    from time import sleep
    sound = VLCSound(source="/home/fruitbat/Music/Various/Music With Attitude/04 - "
                            "dEUS - Everybody's Weird.mp3")
    sound.load()
    if sound:
        sound.play()
        i = 0
        while i < 5:
            print("Sound found at %s" % sound.source)
            print("Sound is %.3f seconds" % sound.length)
            i += 1

        sound.stop()
        sleep(2)
        sound.play()
        sleep(2)
