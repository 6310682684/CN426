import threading
import socket
from os import system
import subprocess

PORT = 2020
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
SHOW_LIST = "!list"
SHOW_OTHER_LIST = "!otherlist"
SHOW_BLOCKED_LIST = "!blocklist"
SHOW_BLOCKED_USER = "!blockuser"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
clients_list = []
name_list = []
block_list = {}

PING_COMMAND = "!ping"


def broadcast(message, sender=None):
    if sender:
        sender_name = name_list[clients_list.index(sender)].decode(FORMAT)
        if message.startswith(b"@"):
            print(message.decode(FORMAT))
            block_list[f"b'{sender_name}'"].append(message.decode(FORMAT)[1:])
            # print(block_list)
            sender.send(f'[SERVER] User "{message.decode(FORMAT)[1:]}" blocked by {sender_name}'.encode(FORMAT))
        elif message.startswith(b"-"):
            block_list[f"b'{sender_name}'"].remove(message.decode(FORMAT)[1:])
            # print(block_list)
            sender.send(f'[SERVER] Unblock "{message.decode(FORMAT)[1:]}"'.encode(FORMAT))
        elif message.startswith(b"!"):
            sender.send(f'[SERVER] Command "{message.decode(FORMAT)}" acknowledged by {sender_name}'.encode(FORMAT))
        else:
            for client in clients_list:
                if client != sender and sender_name not in block_list[f"{name_list[clients_list.index(client)]}"]:
                    client.send(message)
    else:
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
            broadcast(f'[SERVER] {names} has left the chat room!'.encode(FORMAT))
            name_list.remove(names)
            break
        
        elif message == SHOW_LIST.encode(FORMAT):
            names_str = ", ".join([name.decode(FORMAT) for name in name_list])
            client.send(f'[SERVER] Connected users: {names_str}'.encode(FORMAT))
        
        elif message == SHOW_OTHER_LIST.encode(FORMAT):
            new_name_list = []
            for name in name_list:
                if name != name_list[clients_list.index(client)]:
                    new_name_list.append(name)
            names_str = ", ".join([name.decode(FORMAT) for name in new_name_list])
            client.send(f'[SERVER] Other users: {names_str}'.encode(FORMAT))
        
        elif message == SHOW_BLOCKED_LIST.encode(FORMAT) or message == SHOW_BLOCKED_USER.encode(FORMAT):
            if len(block_list[f"{name_list[clients_list.index(client)]}"]) != 0:
                names_str = ", ".join([name for name in block_list[f"{name_list[clients_list.index(client)]}"]])
                if message == SHOW_BLOCKED_LIST.encode(FORMAT):
                    client.send(f'[SERVER] Blocked list: {names_str}'.encode(FORMAT))
                elif message == SHOW_BLOCKED_USER.encode(FORMAT):
                    client.send(f'[SERVER] Blocked user: {names_str}'.encode(FORMAT))
            else:
                client.send(f'[SERVER] No User Blocked'.encode(FORMAT))
        else:
            broadcast(message, sender=client)
        

# recieve clients' connections

def receive():
    while True:
        print('[SERVER] Server is running and listening ...')
        client, address = server.accept()
        print(f'[SERVER] connection is established with {str(address)}')
        client.send('names?'.encode(FORMAT))
        names = client.recv(HEADER)
        name_list.append(names)
        clients_list.append(client)
        block_list.update({f'{names}': []})
        print(block_list)
        print(f'[SERVER] The names of this client is {names.decode(FORMAT)}')
        broadcast(f'{names.decode(FORMAT)} has connected to the chat room \n'.encode(FORMAT))
        client.send('you are now connected!'.encode(FORMAT))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()