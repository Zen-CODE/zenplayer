import socket


def get_local_ip_socket():
    """Determine the local IP address by connecting to an external server."""
    s = None
    try:
        # Create a temporary socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a known external address (doesn't actually send data)
        # 8.8.8.8 (Google's DNS) is a common choice
        s.connect(("8.8.8.8", 80))
        # Get the socket's own IP address
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"  # Fallback to loopback
    finally:
        if s:
            s.close()
    return IP


local_address = get_local_ip_socket()
ZENPLAYER_URL = f"http://{local_address}:5000"
ZENPLAYER = {}
ZENSLEEP = 5
