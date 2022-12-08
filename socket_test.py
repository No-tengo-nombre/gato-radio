import socket
# import sounddevice as sd
import pyaudio
import numpy as np
import struct
import threading
import queue
import time
import pickle
import sys


SAMPLE_RATE = 48000
WINDOW = 2 ** 16
BUFFER_TIME = 5
BLOCKSIZE = 2 ** 10


stop_event = threading.Event()


def receive(sock, q):
    print("Started receiving")
    while True:
        if stop_event.is_set():
            print("Stopping thread")
            break

        data = sock.recv(WINDOW)
        indices = np.arange(WINDOW)
        grouped_data = [data[i:i+4] for i in indices[::4] if data[i:i+4] != b""]

        try:
            q.put_nowait(b"".join(grouped_data))
        except queue.Full:
            print("O")
            continue

q = queue.Queue(int(BUFFER_TIME * WINDOW / SAMPLE_RATE))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 42069))
    print("Connected")
    output_event = threading.Event()

    recv_thread = threading.Thread(target=receive, args=(s, q))
    recv_thread.start()

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True, frames_per_buffer=BLOCKSIZE)

    print("Initiating stream")
    while True:
        try:
            frame = q.get_nowait()
            stream.write(frame)
        except:
            stop_event.set()
            break

recv_thread.join()
