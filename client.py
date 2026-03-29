import socket
from gui import GameGUI

HOST,PORT='127.0.0.1',5556
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
GameGUI(client_socket).start()
