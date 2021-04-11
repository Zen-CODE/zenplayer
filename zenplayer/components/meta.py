"""
This module handles the fetching of track metadata via the mutagen library.
"""
# from mutagen.mp3 import MP3
from mutagen import File


class Metadata:
    """
    Managages the extraction of metadata from audio files
    """

    @staticmethod
    def _get_bitrate(info_obj):
        """
        Return the bitrate description given the mutagen bitrate object.
        """
        bitrate_mode = getattr(info_obj, "bitrate_mode", None)
        if bitrate_mode is None:
            return "unknown"
        val = int(bitrate_mode)
        return ["Unknown", "CBR", "VBR", "ABR"][val]

    @staticmethod
    def get(file_name):
        """
        Return a dictionary of technical metadat on the given file
        """
        info = File(file_name).info
        return{
            "length": info.length,
            "bitrate": info.bitrate // 1000,
            "bitrate_mode": Metadata._get_bitrate(info),
            "channels": info.channels,
            "sample_rate": info.sample_rate
        }


if __name__ == "__main__":
    data = Metadata.get("/home/fruitbat/Music/50 Cent/Get Rich Or Die Tryin'/"
                        "05 - In Da Club.mp3")
    print(f"data={data}")
    data = Metadata.get("/home/fruitbat/Music/Ace Of Base/Da Capo/01 - "
                        "Unspeakable.ogg")
    print(f"data={data}")
