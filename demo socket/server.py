import socket
import threading

HEADER = 1024
PORT = 2020
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!dc"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr) : 
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected :
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length : 
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE :
                connected = False

            print(f"[{addr}] {msg} ")
            conn.send("MSG recieved".encode(FORMAT))

    #after disconnected
    conn.close()

def start() :
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True :
        conn , addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}")

print("[STARTING] server is starting . . . . .")
start()


