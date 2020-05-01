"""
This module houses the Cloud Firestore functions, providing methods to read,
write and listen for data changes.
"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta
from threading import Thread
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
        Logger.info("NowPlaying: Writing state to cloud firestore...")

        def save_to_fs():
            """ Save to firestore """
            NowPlaying(artist=ctrl.artist, album=ctrl.album,
                       track=ctrl.track, state=ctrl.state,
                       machine=gethostname(),
                       datetime=datetime.now() - timedelta(hours=2)).save()

        Thread(target=save_to_fs).start()
