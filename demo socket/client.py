import threading
import socket

PORT = 2020
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
names = input('Choose your names >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "names?":
                client.send(names.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = f'{names}: {input("")}'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()