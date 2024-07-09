import logging
import socket
from typing import Callable
from threading import Thread


logger = logging.getLogger("ServerProxy")


class ServerProxy:

    def __init__(self, port: int) -> None:
        self.server = socket.socket()
        self.server.bind(('127.0.0.1', port))
        self.conn: socket.socket = None

    def start_listen_in_thread(self, callback: Callable) -> Thread:
        t = Thread(
            target=self.worker,
            args=(callback,)
        )
        t.start()
        return t

    def worker(self, callback: Callable) :
        logger.debug("Waiting game for connect...")
        self.server.listen(1)
        conn, addr = self.server.accept()
        self.conn = conn

        chunk = 1024
        while 1:
            buffer = bytes()
            while 1:
                readed = conn.recv(chunk)
                buffer += readed
                if len(readed) != chunk: break
            logger.debug(f"Recieved  {buffer.hex()}")
            callback(buffer)
    
    def send(self, data: bytes):
        self.conn.send(data)