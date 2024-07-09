import logging

from src.client import ClientProxy
from src.server import ServerProxy

logging.basicConfig(level=logging.DEBUG)

client = ClientProxy(ip, port)
server = ServerProxy(port)

def server_callback(data):
    client.send(data)

def client_callback(data):
    server.send(data)

t_server = server.start_listen_in_thread(server_callback)
t_client = client.start_in_thread(client_callback)

t_server.join()