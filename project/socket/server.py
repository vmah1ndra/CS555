import socket
import threading

HEADER = 64
FORMAT = 'utf-8'
LOCALHOST = "127.0.0.1"
PORT = 1234
ADDR = (LOCALHOST, PORT)
DISCONNECT_MSG = "[DISCONNECTED]"

c_list = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send(msg, conn):
    msg = str(msg).encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(msg)

def handle_client(conn, adr):
    print(f"Connected: {adr}")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[{adr}]: {msg}")
        
        send_msg = input(f"Server input to {adr} > ")
        if send_msg != "":
            send(send_msg, conn)
        

    conn.close()

def start():
    server.listen(5)
    while True:
        conn, adr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,adr))
        thread.start()
        print(f"Connection #{threading.active_count()-1}")
        c_list.append(conn)

print("Starting...")
start()

