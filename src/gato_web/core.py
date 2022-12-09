import numpy as np
import pyaudio
import queue
import socket
import threading

from gato_receiver.configs import BUFFER_TIME, RECEIVE_WINDOW, SAMPLE_RATE
from gato_web.configs import BLOCKSIZE


def receive(sock, q, stop_event):
    print("Started receiving")
    while True:
        if stop_event.is_set():
            print("Stopping thread")
            break

        try:
            q.put_nowait(sock.recv(RECEIVE_WINDOW))
        except queue.Full:
            continue


def play_audio(ip="", port=42069, preprocessing=None):
    q = queue.Queue(int(BUFFER_TIME * RECEIVE_WINDOW / SAMPLE_RATE))


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()

        conn, addr = s.accept()
        print("Connected")
        stop_event = threading.Event()

        recv_thread = threading.Thread(target=receive, args=(conn, q, stop_event))
        recv_thread.start()

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, output=True, frames_per_buffer=BLOCKSIZE)

        print("Initiating stream")
        while True:
            try:
                frame = q.get()
                frame_array = np.frombuffer(frame, dtype=np.float32)

                if preprocessing is not None:
                    frame_array = preprocessing(frame_array)

                stream.write(frame_array.tobytes())
            except:
                stop_event.set()
                break

    recv_thread.join()
