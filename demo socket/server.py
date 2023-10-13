import threading
import socket

PORT = 2020
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
clients = []
name_list = []


def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients'connections

def handle_client(client):
    while True:

        message = client.recv(1024)
        broadcast(message)
        if message == "!dc":
            index = clients.index(client)
            clients.remove(client)
            client.close()
            names = name_list[index]
            broadcast(f'{names} has left the chat room!'.encode('utf-8'))
            name_list.remove(names)
            
# Main function to receive the clients connection


def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('names?'.encode('utf-8'))
        names = client.recv(1024)
        name_list.append(names)
        clients.append(client)
        print(f'The names of this client is {names}'.encode('utf-8'))
        broadcast(f'{names} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()