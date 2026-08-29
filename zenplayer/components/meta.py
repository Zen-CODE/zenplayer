"""
This module handles the fetching of track metadata via the mutagen library.
"""

from typing import Any, TypedDict
from mutagen import File


class AudioMetadata(TypedDict):
    """Technical metadata for an audio file."""

    length: float
    bitrate: int
    bitrate_mode: str
    channels: int
    sample_rate: int


class Metadata:
    """
    Manages the extraction of metadata from audio files
    """

    _BITRATE_MODES: dict[int, str] = {
        0: "Unknown",
        1: "CBR",
        2: "VBR",
        3: "ABR",
    }

    @staticmethod
    def _get_bitrate(info_obj: Any) -> str:
        """
        Return the bitrate description given the mutagen bitrate object.
        """
        bitrate_mode = getattr(info_obj, "bitrate_mode", None)
        if bitrate_mode is None:
            return "Unknown"
        try:
            val = int(bitrate_mode)
            return Metadata._BITRATE_MODES.get(val, "Unknown")
        except (ValueError, TypeError):
            return "Unknown"

    @staticmethod
    def get(file_name: str) -> AudioMetadata:
        """
        Return a dictionary of technical metadata on the given file
        """
        default_meta: AudioMetadata = {
            "length": 0.0,
            "bitrate": 0,
            "bitrate_mode": "Unknown",
            "channels": 0,
            "sample_rate": 0,
        }
        if not file_name:
            return default_meta

        try:
            audio = File(file_name)
            if audio is None or getattr(audio, "info", None) is None:
                return default_meta

            info = audio.info
            raw_bitrate = getattr(info, "bitrate", 0) or 0
            return {
                "length": float(getattr(info, "length", 0.0) or 0.0),
                "bitrate": int(raw_bitrate // 1000),
                "bitrate_mode": Metadata._get_bitrate(info),
                "channels": int(getattr(info, "channels", 0) or 0),
                "sample_rate": int(getattr(info, "sample_rate", 0) or 0),
            }
        except Exception:
            return default_meta
