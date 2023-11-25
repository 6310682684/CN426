import threading
import socket
import os

PORT = 2020
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
PING_COMMAND = "!ping"
names = input('Choose your names >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def client_receive():
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            if message == "names?":
                client.send(names.encode(FORMAT))
            else:
                print("\n" + message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        # message = f'{names} : {input("")}'
        message = input("[CLIENT] type message: ")
        if message == DISCONNECT_MESSAGE:
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))  # encode and send the disconnect message
            break  # exit the loop to close the thread when the user types !dc
        if message == PING_COMMAND:
            os.system("ping google.com")
        else:
            client.send(f'{names} : {message}'.encode(FORMAT))
        


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()