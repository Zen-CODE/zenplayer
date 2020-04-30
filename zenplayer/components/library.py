from os import listdir
from os.path import join, isdir, basename, expanduser
from random import sample
from glob import glob
from random import choice


class Library:
    """
    Class for fetching information about our music library. This information
    is contained entirely in the folder names and structures.
    """

    def __init__(self):
        # self.path = expanduser("~/Music")
        # Create a symbolic link to this folder if it does not exist
        self.path = expanduser("~/Zen/Music")
        dirs = [name for name in listdir(self.path) if
                isdir(join(self.path, name))]
        artists = {}
        albums = []
        for artist in dirs:
            artists[artist] = []
            artist_path = join(self.path, artist)
            for album in listdir(artist_path):
                if isdir(join(artist_path, album)):
                    artists[artist].append(album)
                    albums.append((artist, album))

        self._artists = artists
        """ A dictionary of lists, where the key is the artist and the value
        the albums.
        """
        self._albums = albums
        """ A list of (artist, album) tuples. We store this only so we can find
        random albums all with an equal chance. The previous algorithm found a
        random artist, then a random album, favouring albums by artists with
        fewer albums.
        """

    def get_artists(self):
        """ Return a list of artists. """
        return sorted(list(self._artists.keys()))

    def get_random_artists(self, number):
        """ Return a random list of *number* artists. """
        artists = self.get_artists()
        return sample(artists, number)

    def get_random_albums(self, artist, number):
        """ Return a random list of *number* albums by *artist*. """
        albums = self.get_albums(artist)
        if albums:
            return sample(albums, number)
        else:
            raise (Exception("No albums found for {0}".format(artist)))

    def get_albums(self, artist):
        """ Return a list of albums for the *artist*. """
        return sorted(self._artists.get(artist, []))

    def get_album_cover(self, artist, album):
        """
        Return the full path to the album cover for the specified album or the
        default library image one does not exist.
        """
        path = join(self.path, artist, album)
        pattern = "cover.*"
        matches = glob(join(path, pattern))
        return matches[0] if matches else join(self.path, "default.png")

    def get_path(self, artist, album):
        """ Return the full path to the specified album. """
        return join(self.path, artist, album)

    def get_random_album(self):
        """
        Return the artist and album of a random album as an artist, album tuple
        """
        return choice(self._albums)

    @staticmethod
    def _get_any_matches(path, *exts):
        """ Return the first valid files matching the extensions
        in the path specified."""
        for ext in exts:
            matches = glob(join(path, ext))
            if matches:
                return matches
        return None

    def get_tracks(self, artist, album):
        """
        Return a list of the album tracks
        """

        def get_name(fname):
            """"Return the nice, cleaned name of the track"""
            return basename(fname)  # [:-4]

        path = join(self.path, artist, album)
        matches = self._get_any_matches(
            path, "*.mp3", "*.ogg", "*.m4a", "*.wma")
        if matches:
            return sorted([get_name(f) for f in matches])
        else:
            return []

    def search(self, term):
        """
        Search for all albums which match this term, either in the artist
        name of the album name, then return one on them randomly.

        Returns:
             A dictionary with the keys "artist", "album" and "path" as keys
             if found. Return an empty dictionary otherwise.
        """
        terms = term.lower().split(" ")
        matches = []
        for artist in self._artists.keys():
            for album in self._artists[artist]:
                if all([(artist + album).lower().find(t) > -1
                        for t in terms]):
                    matches.append(
                        {"artist": artist,
                         "album": album,
                         "path": self.get_path(artist, album)})
        return choice(matches) if matches else []
