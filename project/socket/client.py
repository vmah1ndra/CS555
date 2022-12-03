import socket
from threading import Thread
import os

host = '127.0.0.1'
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def getMessage():
    while True:
        data = s.recv(512).decode('utf-8')
        if data.isdigit():
            data = int(data)
        print(data)
        if data == 'SHUTDOWN' or not data:
            s.close()
            os._exit(1)

print("Are you a player or a client?")
name = input().lower().strip()
while name != 'player' and name != 'client':
    print("Please enter player or client.")
    name = input().lower().strip()
s.send(bytes(name, 'utf-8'))

Thread(target = getMessage).start()

while True:
    data = input()
    s.send(bytes(data, 'utf-8'))

s.close()
