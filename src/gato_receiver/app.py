import queue
import socket
import threading

from gato_receiver.configs import BUFFER_TIME, DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT, RECEIVE_WINDOW, SAMPLE_RATE
# from gato_receiver.gnuradio import gato_receiver_tcp
from gato_receiver.logger import LOGGER


class App:
    def __init__(self, target_ip=DEFAULT_SERVER_IP, target_port=DEFAULT_SERVER_PORT) -> None:
        self._stop_event = threading.Event()
        self.target_ip = target_ip
        self.target_port = target_port
        self.audio_buffer = queue.Queue(int(BUFFER_TIME * RECEIVE_WINDOW / SAMPLE_RATE))

    def run(self) -> None:
        # gnu_thread = threading.Thread(target=gato_receiver_tcp.main)
        # gnu_thread.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sdr_s:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_s:
                LOGGER.info("Waiting for SDR connection")
                sdr_s.connect(("127.0.0.1", 42069))
                LOGGER.info("Connected to SDR.")
                LOGGER.info("Waiting for server connection")
                server_s.connect((self.target_ip, self.target_port))
                LOGGER.info("Connected to server.")

                while True:
                    packet = sdr_s.recv(RECEIVE_WINDOW)
                    server_s.send(packet)
