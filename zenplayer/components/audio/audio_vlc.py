"""
This module houses a VLC audio component that supports the Kivy `Sound`
interface.
"""
from kivy.core.audio import Sound, SoundLoader
from vlc import EventType, Instance, MediaPlayer
from kivy.clock import mainthread
from kivy.logger import Logger


class SoundVLCPlayer(Sound):
    '''
    A Kivy `Sound` object based on a VLC audio backend.
    '''

    instance = None

    @staticmethod
    def extensions():
        return ("mp3", "mp4", "flac", "mkv", "wav", "ogg", "m4a")

    def __init__(self, **kwargs):
        self._length = 0
        if self.instance is None:
            Logger.debug("SoundVLCPlayer: Creating an instance")
            SoundVLCPlayer.instance = Instance()
        self.player = None
        super().__init__(**kwargs)

    @mainthread
    def _track_finished(self, *args):
        """ Event fired when the track is finished. """
        if not self.loop:
            self.stop()
        else:
            self.seek(0.)
            self.player.play()

    def _load_player(self, filename):
        """ Unload the VLC Media player if it not already unloaded """
        self._unload_player()

        Logger.info("VLCPlayer: Loading player")
        self.player = player = self.instance.media_player_new()
        media = player.set_mrl(filename)
        player.event_manager().event_attach(
            EventType.MediaPlayerEndReached, self._track_finished)
        media.parse()  # Determine duration
        self._length = media.get_duration() / 1000.0
        media.release()

    def _unload_player(self):
        """ Unload the VLC Media player if it not already unloaded """
        if self.player is not None:
            Logger.info("VLCPlayer: Unloading player")
            self.player.event_manager().event_detach(
                EventType.MediaPlayerEndReached)
            if self.player.is_playing():
                self.player.stop()
            self.player.release()
            self.player = None

    def load(self):
        """
        Loads the Media player for the suitable `source` filename.

        *Note*

        There are various approach to loading the player, some of which cause
        problems after prolonged use. e.g.

            media = Instance().media_new(self.source)
            media.parse()  # Determine duration
            player = self._mediaplayer = media.player_new_from_media()

        Similarly, even this seems to give the same errors over time:

            media = Instance().media_new(self.source)
            player = self._mediaplayer = MediaPlayer(self.source)
            player.set_media(media)


        It seems we need to create a new instance for each track to get better
        reliability.
        """
        Logger.info("VLCPlayer: Entering load")
        self._load_player(self.source)
        self._set_volume(self.volume)

    def unload(self):
        """ Unload any instances of the player """
        self._unload_player()

    def play(self):
        """ Play the audio file """
        if self.state == 'play':
            super().play()
            return
        if self.player is None:
            self.load()

        self.player.play()
        self.state = 'play'
        super().play()

    def stop(self):
        """ Stop any currently playing audio file """
        if self.player and self.player.is_playing():
            self.player.pause()
        super().stop()

    def seek(self, position):
        """ Set the player to the given position in seconds """
        if self.player:
            value = position / self._length
            self.player.set_position(value)

    def get_pos(self):
        """ Return the position in seconds the currently playing track """
        if self.player is not None and self.state == "play":
            return self.player.get_position() * self._length
        return 0

    def on_volume(self, instance, volume):
        """
        Respond to the setting of the volume. This value is fraction between
        0 and 1.
         """
        self._set_volume(volume)

    def _set_volume(self, value):
        """
        The volume of the currently playing sound, where the value is between
        0 and 1.
        """
        if self.player:
            vol = 100 if abs(value) >= 1.0 else 100 * abs(value)
            self.player.audio_set_volume(int(vol))

    def _get_length(self):
        """ Getter method to fetch the track length """
        return self._length


if __name__ == "__main__":
    from time import sleep

    file = "/home/fruitbat/Music/Various/Music With Attitude/04 - " \
           "dEUS - Everybody's Weird.mp3"
    # Use the `KIVY_AUDIO=vlcplayer` setting in environment variables to use
    # our provider
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
