import threading
import socket
import os
import time

PORT = 2020
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
PING_COMMAND = "!ping"
BLOCK_PING_COMMAND = "!blockping"
UNBLOCK_PING_COMMAND = "!allowping"
BLOCK_USER_COMMAND = "!block"
UNBLOCK_USER_COMMAND = "!unblock"
SHOW_LIST = "!list"
SHOW_BLOCKED_LIST = "!blocklist"
SHOW_BLOCKED_USER = "!blockuser"

names = input('Choose your names >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def client_receive():
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            if message == "names?":
                client.send(names.encode(FORMAT))
            elif message[0:22] == "[SERVER] Blocked user:":
                print(message)
                user = input("Select User from the block list: ")
                client.send(("-" + user).encode(FORMAT))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    ping_status = "true"
    while True:
        # message = f'{names} : {input("")}'
        message = input("")
        
        
        if message == DISCONNECT_MESSAGE:
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))  # encode and send the disconnect message
            break  # exit the loop to close the thread when the user types !dc
        
        if message.startswith("!"):
            if message == BLOCK_PING_COMMAND:
                ping_status = "false"
                print("You have blocked the connection.")
            elif message == UNBLOCK_PING_COMMAND:
                ping_status = "true"
                print("You have allowed the connection.")
            elif message == SHOW_LIST:
                client.send(SHOW_LIST.encode(FORMAT))
            elif message == PING_COMMAND :
                if ping_status == "true":
                    os.system("ping google.com")
                else:
                    print(f"You are currently blocking the connection.")
            elif message == SHOW_BLOCKED_LIST:
                client.send(SHOW_BLOCKED_LIST.encode(FORMAT))

            elif message == BLOCK_USER_COMMAND:
                client.send(SHOW_LIST.encode(FORMAT))
                user = input("Select User from the list: ")
                client.send(("@" + user).encode(FORMAT))
            elif message == UNBLOCK_USER_COMMAND:
                client.send(SHOW_BLOCKED_USER.encode(FORMAT))
                time.sleep(1)
            else:
                print(f"Invalid command: {message}")
            
        if ping_status == "true" and not message.startswith("!"):
            client.send(f'{names} : {message}'.encode(FORMAT))

        if ping_status == "false" and not message.startswith("!"):
            if message == "!ping":
                print(f"You are currently blocking the connection.")
            else:
                client.send(f'{names} : {message}'.encode(FORMAT))
            

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()