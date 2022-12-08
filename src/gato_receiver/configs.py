import os

__BASE_DIR__ = os.path.join(
   os.path.dirname( __file__), "..", ".."
)
DEFAULT_SERVER_IP = "139.144.23.55"
DEFAULT_SERVER_PORT = 42069
RECEIVE_WINDOW = 2 ** 16
SAMPLE_RATE = 48000
BUFFER_TIME = 5
