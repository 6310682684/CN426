import socket
import threading

HEADER = 1024
PORT = 2020
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_msg(msg) : 
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)   
    send_length += b' ' *  (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048))
    
send_msg("Hello world!")
input()
send_msg("Hello world! 2")
input()
send_msg("Hello world! 3")
send_msg(DISCONNECT_MESSAGE)