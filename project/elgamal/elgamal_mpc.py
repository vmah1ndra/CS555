from pyseltongue import sharing
from Crypto.PublicKey import ElGamal
from Crypto import Random
import random
import libnum

class PubKey:
    def __init__(self, p, g, y):
        self.p = p
        self.g = g
        self.y = y

    def encrypt(self, m):
        k = random.randrange(2, self.p)
        a = pow(self.g, k, self.p)
        b = (m * pow(self.y, k, self.p)) % self.p
        return a, b

class PrivKey:
    def __init__(self, x):
        self.x = x

class KeyPair:
    def __init__(self, pk, sk):
        self.pk = pk
        self.sk = sk
    
    def decrypt(self, a, b):
        return (b * libnum.invmod(pow(a, self.sk.x, self.pk.p), self.pk.p)) % self.pk.p

def keygen():
    key = ElGamal.generate(512, Random.get_random_bytes)
    pk = PubKey(int(key.p), int(key.g), int(key.y))
    sk = PrivKey(int(key.x))
    return KeyPair(pk, sk)
