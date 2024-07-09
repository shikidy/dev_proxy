import socket
from typing import Callable
from threading import Thread

import logging


logger = logging.getLogger("ClientProxy")
class ClientProxy:


    def __init__(self, server_ip: str, server_post: int) -> None:
        self._socket_ip = server_ip
        self._socket_port = server_post
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_ip, server_post))

    def start_in_thread(self, on_message_callback: Callable) -> Thread:
        t = Thread(target=self.observer, args=(on_message_callback,))
        t.start()
        return t
    
    def observer(self, callback: Callable):
        while 1:
            buffer = bytes()
            chunk = 1024

            while 1:
                readed = self.client.recv(chunk)
                buffer += readed
                if len(readed) != chunk: break
            callback(buffer)
            logger.debug(f"Recieved {buffer.hex()}")

    def send(self, data: bytes):
        self.client.send(data)
