import socket

HEADER = 64
FORMAT = 'utf-8'
LOCALHOST = "127.0.0.1"
PORT = 1234
ADDR = (LOCALHOST, PORT)
DISCONNECT_MSG = "[DISCONNECTED]"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    msg = msg.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(msg)

while True:
    send_msg = input("Client input > ")
    if send_msg != "":
        send(send_msg)
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False

        print(f"[{ADDR}]: {msg}")
        