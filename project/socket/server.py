import socket
from threading import Thread
import atexit
import elgamal_mpc
import time

host = '127.0.0.1'
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(4)

def handleExit():
    broadcast('SHUTDOWN', '')
    s.close()

atexit.register(handleExit)

players = {}
n_players = 0

client = {}
n_clients = 0

def getClient():
    while True:
        conn, addr = s.accept()
        Thread(target = handleClient, args = (conn, )).start()

def handleClient(conn):
    global n_players
    global n_clients
    global client
    global players
    typ = conn.recv(512).decode('utf-8')
    name = 'none'

    print(typ)
    if typ == 'player' and n_players < 3:
        n_players += 1
        name = 'p' + str(n_players)
        players[name] = conn
    elif typ == 'client' and n_clients < 1:
        n_clients += 1
        name = 'c'
        client[name] = conn
    else:
        # boot the client (decline the connection)
        conn.send(bytes('SHUTDOWN', 'utf-8'))
        conn.close()
        return

    while True:
        msg = conn.recv(512).decode('utf-8')
        print(msg)
        if not msg:
            break
        if msg == '':
            continue
        broadcast(msg, name+": ")

    if typ == 'client':
        n_clients -= 1
        client.pop(name)
    elif typ == 'player':
        n_players -= 1
        players.pop(name)

    conn.send(bytes('SHUTDOWN', 'utf-8'))
    conn.close()

def broadcast(msg, prefix):
    for sock in players:
        players[sock].send(bytes(prefix + msg,'utf-8'))
    for sock in client:
        client[sock].send(bytes(prefix + msg,'utf-8'))

print('Started the Server')
Thread(target = getClient).start()

# Not sure if this would allow us to wait until
# we get 3 player connections and then start the keygen
# we might need another thread or something
#while not (n_players == 3):
    #continue

#key = elgamal_mpc.keygen()
#pub = key.pk
#priv = key.sk
#shares = sharing.secret_int_to_points(priv, 2, 3)

# TODO: broadcast public (object) and send individual shares and encrypted messages

#m1 = random.randrange(99999)
#m2 = random.randrange(99999)
#m3 = random.randrange(99999)

#a1, b1 = pub.encrypt(m1)
#a2, b2 = pub.encrypt(m2)
#tmp = key.decrypt(a1 * a2, b1 * b2)
#a3, b3 = pub.encrypt(pow(pub.g, tmp, pub.p))
#a4, b4 = pub.encrypt(pow(pub.g, m3, pub.p))

#tmp = key.decrypt(a3 * a4, b3 * b4)
#m1m2m3 = -1
#for i in range(1, 2 ** 64):
    #if (pow(pub.g, i, pub.p) == tmp):
        #m1m2m3 = i
        #break

# send m1m2m3 to client if they pay money
