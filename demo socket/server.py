import threading
import socket

PORT = 2020
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
clients_list = []
name_list = []


def broadcast(message):
    for client in clients_list:
        client.send(message)


# handle clients'connections

def handle_client(client):
    while True:

        message = client.recv(HEADER)
        # check if use command
        if message == DISCONNECT_MESSAGE.encode(FORMAT):
            index = clients_list.index(client)
            clients_list.remove(client)
            client.close()
            names = name_list[index]
            broadcast(f'{names} has left the chat room!'.encode(FORMAT))
            name_list.remove(names)
            break
        else : 
            broadcast(message)

        

# recieve clients' connections

def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('names?'.encode(FORMAT))
        names = client.recv(HEADER)
        name_list.append(names)
        clients_list.append(client)
        print(f'The names of this client is {names.decode(FORMAT)}')
        broadcast(f'{names.decode(FORMAT)} has connected to the chat room \n'.encode(FORMAT))
        client.send('you are now connected!'.encode(FORMAT))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()