from vlc import MediaPlayer, EventType
from kivy.properties import OptionProperty, ObjectProperty
from kivy.event import EventDispatcher
from kivy.clock import mainthread
from logging import getLogger

logger = getLogger(__name__)


class Sound(EventDispatcher):
    """
    This class manages the playing of audio as a Singleton
    """
    state = OptionProperty("", options=["", "stopped", "playing", "paused"])
    player = ObjectProperty(None)
    """ Reference to the underlying vlc instance. """

    def _set_player(self, file_name):
        """ Create and set a new media player for the given file """
        logger.debug(f"Entering _set_player. file_name={file_name}")
        if self.player is not None:
            logger.debug("Detaching event and unloading.")
            self.player.event_manager().event_detach(
                EventType.MediaPlayerEndReached)
            self.player.stop()

        player = self.player = MediaPlayer(file_name)
        player.event_manager().event_attach(
            EventType.MediaPlayerEndReached, self._track_finished)

    @mainthread
    def _track_finished(self, *args):
        """ Event fired when the track is finished. """
        logger.debug(f"Entering _track_finished. state={self.state}")
        if self.state != "stopped":
            self.state = "stopped"

    def get_pos_length(self):
        """
        Return a tuple of the length and position, or return 0, 0

        Return:
            pos, length

            * pos: The current playing position, as a fraction between 0 and 1.
            * length: The length of the song in seconds.

        """
        logger.debug(f"Entering get_pos_length. player={self.player}")
        if self.player:
            return (self.player.get_position(),
                    self.player.get_length() / 1000.0)
        else:
            return 0.0, 0.0

    def stop(self):
        """ Stop any playing audio """
        logger.debug(f"Entering stop. player={self.player}")
        if self.player:
            self.player.stop()
            self.state = "stopped"

    def pause(self):
        """ Pause and resume the currently playing audio track. """
        logger.debug(f"Entering pause. state={self.state},"
                     f" player={self.player}")
        if self.state in ["playing", "paused"] and self.player:
            self.player.pause()
            self.state = "paused" if self.state == "playing" else "playing"

    def play(self, filename, volume=1, pos=0.0):
        """
        Play the file specified by the filename. If on_stop is passed in,
        this function is called when the sound stops
        """
        logger.debug(f"Entering play. player={self.player}")
        self._set_player(filename)
        self.set_volume(volume)
        self.player.play()
        if pos != 0.0:
            self.player.set_position(pos)
        self.state = "playing"

    def set_position(self, value):
        """
        The position of the currently playing sound as a fraction between 0
        and 1.
        """
        logger.debug(f"Entering set_position. player={self.player}")
        if self.player:
            self.player.set_position(value)

    def set_volume(self, value):
        """
        The volume of the currently playing sound, where the value is between
        0 and 1.
        """
        logger.debug(f"Entering set_volume. player={self.player}")
        if self.player:
            vol = 100 if abs(value) >= 1.0 else 100 * abs(value)
            self.player.audio_set_volume(int(vol))


if __name__ == "__main__":
    from time import sleep

    def get_sound():
        sound = Sound()
        sound.play("/home/fruitbat/Music/50 Cent/Get Rich Or Die Tryin'/"
                   "05 - In Da Club.mp3", 0, 0)
        return sound

    def test_volume():
        print("Testing volume...")
        sound = get_sound()
        sleep(2)
        sound.set_volume(0.5)
        sleep(1)
        sound.set_volume(0.25)
        sleep(1)
        sound.set_volume(1)
        sleep(1)

    def test_position():
        print("Testing positioning...")
        sound = get_sound()
        sound.set_position(0.5)
        sleep(2)
        sound.set_position(0)

    def test_get_pos_length():
        """ Testing position and length """
        sound = get_sound()
        pos, length = sound.get_pos_length()
        print(f"Position = {pos}, length={length}")

    def test_state_changes():
        print("Testing state changes...")

        def state_change(widget, value):
            print(f"Got state change {widget} to {value}")

        sound = get_sound()
        sound.set_volume(0.8)
        sound.bind(state=state_change)
        sound.pause()
        sleep(1.0)
        sound.pause()
        sleep(1.0)
        sound.stop()

    test_volume()
    test_position()
    test_get_pos_length()
    test_state_changes()

'''
https://www.olivieraubert.net/vlc/python-ctypes/doc/

MediaPlayer methods
===================
028: 'add_slave'
029: 'audio_get_channel'
030: 'audio_get_delay'
031: 'audio_get_mute'
032: 'audio_get_track'
033: 'audio_get_track_count'
034: 'audio_get_track_description'
035: 'audio_get_volume'
036: 'audio_output_device_enum'
037: 'audio_output_device_get'
038: 'audio_output_device_set'
039: 'audio_output_set'
040: 'audio_set_callbacks'
041: 'audio_set_channel'
042: 'audio_set_delay'
043: 'audio_set_format'
044: 'audio_set_format_callbacks'
045: 'audio_set_mute'
046: 'audio_set_track'
047: 'audio_set_volume'
    Args:
        volume: An integer between 0 and 100, specifying the percent.

048: 'audio_set_volume_callback'
049: 'audio_toggle_mute'
050: 'can_pause'
051: 'event_manager'
052: 'from_param'
053: 'get_agl'
054: 'get_chapter'
055: 'get_chapter_count'
056: 'get_chapter_count_for_title'
057: 'get_fps'
058: 'get_full_chapter_descriptions'
059: 'get_full_title_descriptions'
060: 'get_fullscreen'
061: 'get_hwnd'
062: 'get_instance'
063: 'get_length'
064: 'get_media'
065: 'get_nsobject'
066: 'get_position'
067: 'get_rate'
068: 'get_role'
069: 'get_state'
070: 'get_time'
071: 'get_title'
072: 'get_title_count'
073: 'get_xwindow'
074: 'has_vout'
075: 'is_playing'
076: 'is_seekable'
077: 'navigate'
078: 'next_chapter'
079: 'next_frame'
080: 'pause'
081: 'play'
082: 'previous_chapter'
083: 'program_scrambled'
084: 'release'
085: 'retain'
086: 'set_agl'
087: 'set_android_context'
088: 'set_chapter'
089: 'set_equalizer'
090: 'set_evas_object'
091: 'set_fullscreen'
092: 'set_hwnd'
093: 'set_media'
094: 'set_mrl'
095: 'set_nsobject'
096: 'set_pause'
097: 'set_position'
098: 'set_rate'
099: 'set_renderer'
100: 'set_role'
101: 'set_time'
102: 'set_title'
103: 'set_video_title_display'
104: 'set_xwindow'
105: 'stop'
106: 'toggle_fullscreen'
107: 'toggle_teletext'
108: 'video_get_adjust_float'
109: 'video_get_adjust_int'
110: 'video_get_aspect_ratio'
111: 'video_get_chapter_description'
112: 'video_get_crop_geometry'
113: 'video_get_cursor'
114: 'video_get_height'
115: 'video_get_logo_int'
116: 'video_get_marquee_int'
117: 'video_get_marquee_string'
118: 'video_get_scale'
119: 'video_get_size'
120: 'video_get_spu'
121: 'video_get_spu_count'
122: 'video_get_spu_delay'
123: 'video_get_spu_description'
124: 'video_get_teletext'
125: 'video_get_title_description'
126: 'video_get_track'
127: 'video_get_track_count'
128: 'video_get_track_description'
129: 'video_get_width'
130: 'video_set_adjust_float'
131: 'video_set_adjust_int'
132: 'video_set_aspect_ratio'
133: 'video_set_callbacks'
134: 'video_set_crop_geometry'
135: 'video_set_deinterlace'
136: 'video_set_format'
137: 'video_set_format_callbacks'
138: 'video_set_key_input'
139: 'video_set_logo_int'
140: 'video_set_logo_string'
141: 'video_set_marquee_int'
142: 'video_set_marquee_string'
143: 'video_set_mouse_input'
144: 'video_set_scale'
145: 'video_set_spu'
146: 'video_set_spu_delay'
147: 'video_set_subtitle_file'
148: 'video_set_teletext'
149: 'video_set_track'
150: 'video_take_snapshot'
151: 'video_update_viewpoint'
152: 'will_play'
__len__: 153

'''
