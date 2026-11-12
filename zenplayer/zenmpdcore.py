from mpd import MPDClient


class MPDCore:
    client: MPDClient | None = None

    @staticmethod
    def _ensure_client() -> MPDClient:
        """Ensure the MDPClient property is set and connected.
        Note:
            We take this approach to avoid the object management in streamlit
            whilst tying to preserve compatibility with ZenPlayer (Kivy)
        """
        if MPDCore.client is None:
            MPDCore.client = client = MPDClient()
            client.connect("127.0.0.1", 6600)
            # client.update()  # Run this occasionally to update MPD metadata
        else:
            try:
                MPDCore.client.ping()
            except Exception as e:  # noqa BL001
                print(f"ZenMPD: Error pinging MPDClient: {e}")
                try:
                    MPDCore.client.disconnect()
                except Exception as e:  # noqa BL001
                    print(f"ZenMPD: Error disconnecting MPDClient: {e}")
                MPDCore.client.connect("localhost", 6600)
        return MPDCore.client

    @staticmethod
    def pause():
        client = MPDCore._ensure_client()
        client.pause(1)

    @staticmethod
    def stop():
        client = MPDCore._ensure_client()
        client.stop()

    @staticmethod
    def stats() -> dict:
        client = MPDCore._ensure_client()
        return client.stats()

    @staticmethod
    def outputs() -> dict:
        client = MPDCore._ensure_client()
        return client.outputs()

    @staticmethod
    def listmounts() -> list[str]:
        client = MPDCore._ensure_client()
        mounts = client.listmounts()
        return [mount for mount in mounts]

    @staticmethod
    def status() -> dict:
        client = MPDCore._ensure_client()
        return client.status()

    @staticmethod
    def currentsong() -> dict:
        client = MPDCore._ensure_client()
        return client.currentsong()

    @staticmethod
    def addid(file_name: str, index: int) -> int:
        client = MPDCore._ensure_client()
        return client.addid(file_name, index)
