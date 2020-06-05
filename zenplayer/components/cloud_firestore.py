"""
This module houses the Cloud Firestore functions, providing methods to read,
write and listen for data changes.
"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta
from threading import Thread, Lock
from socket import gethostname
from components.paths import rel_to_base
from kivy.logger import Logger


class NowPlaying:
    """
    This class defines the model mapping the 'Now Playing' entries to the
    FireStore database table.

    Note: When instantiating this class, the constructor keyword arguments
          must contain at least the following keys:

            'artist', 'album', 'track', 'state', 'machine', 'datetime'
    """

    _client = None
    """ The singleton firestore client instance. """

    _now_playing = []
    """ A list of NowPlaying objects to execute in sequence.  We need to ensure
    they are processed in order as the 'start' and 'stopped' events happen
    very close together. If run in independent threads, they can write up in a
    non-detereministic order.
    """

    _lock = Lock()
    """ Reference to the threading Lock object """

    def __init__(self, **kwargs):
        if self._client is None:
            NowPlaying._client = self._get_client()
        self.props = kwargs

    @staticmethod
    def _get_client():
        """ Generate and return a FireStore client using the service account.
        """
        cred = credentials.Certificate(
            rel_to_base('keys', 'tunez-245820-047b7b31e116.json'))
        firebase_admin.initialize_app(cred)
        return firestore.client()

    def __repr__(self):
        return "<NowPlaying on {machine}: {artist},  {album}: {track}, state=" \
               "{state} @{datetime}".format(**self.props)

    def save(self):
        """ Store the item to Firestore """
        batch = self._client.batch()
        doc_ref = self._client.collection('tunez').document('now_playing')
        batch.set(doc_ref, self.props)

        # Now add to history
        hist_ref = doc_ref.collection(
            'history').document(self.props['datetime'].isoformat())
        batch.set(hist_ref, self.props)
        batch.commit()

    @staticmethod
    def get_last():
        """
        Retrieve the last entry from FireStore
        """
        if NowPlaying._client is None:
            NowPlaying._client = NowPlaying._get_client()
        users_ref = NowPlaying._client.collection('tunez')
        docs = [doc for doc in users_ref.stream()]
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))
        return docs

    def write_to_db(self, ctrl):
        """
        Write the current "Now Playing" status to our cloud FireStore. We do so
        in a background thread to try and avoid locking when we get stale
        transport errors.
        """
        Thread(target=lambda: self._write_to_db(ctrl)).start()

    def _write_to_db(self, ctrl):
        """
        Write to the firestore database
        """
        Logger.info("NowPlaying: Adding entry to the write queue.")
        with self._lock:
            self._now_playing.append(NowPlaying(
                artist=ctrl.artist, album=ctrl.album, track=ctrl.track,
                state=ctrl.state, machine=gethostname(),
                datetime=datetime.now() - timedelta(hours=2)))

        self._process_queue()

    def _process_queue(self):
        """ Process the 'now_playing' queue and write the entries to firebase.
        """
        Logger.info("NowPlaying: Precessing queue...")
        with self._lock:
            for item in self._now_playing[:]:
                try:
                    item.save()
                    self._now_playing.remove(item)
                except Exception as e:
                    Logger.error(f"cloud_firestore.py: Unable to save - {e}")

            Logger.info("NowPlaying: Queue precessing done. Closing thread...")
