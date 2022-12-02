#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pyseltongue')
get_ipython().system('pip install pycryptodome')


# In[14]:


from pyseltongue import sharing
from Crypto.PublicKey import ElGamal
from Crypto import Random
import random
import libnum


# In[15]:


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


# In[16]:


class PrivKey:
    def __init__(self, x):
        self.x = x


# In[17]:


class KeyPair:
    def __init__(self, pk, sk):
        self.pk = pk
        self.sk = sk
    
    def decrypt(self, a, b):
        return (b * libnum.invmod(pow(a, self.sk.x, self.pk.p), self.pk.p)) % self.pk.p


# In[6]:


def keygen():
    key = ElGamal.generate(512, Random.get_random_bytes)
    pk = PubKey(int(key.p), int(key.g), int(key.y))
    sk = PrivKey(int(key.x))
    return KeyPair(pk, sk)


# In[8]:


key = keygen()


# In[9]:


pub = key.pk
priv = key.sk


# In[10]:


m1 = 15
a1, b1 = pub.encrypt(m1)

m2 = 20
a2, b2 = pub.encrypt(m2)

m3 = key.decrypt(a1 * a2, b1 * b2)
a3, b3 = pub.encrypt(pow(pub.g, m3, pub.p))

m4 = 3
a4, b4 = pub.encrypt(pow(pub.g, m4, pub.p))

tmp_m = key.decrypt(a3 * a4, b3 * b4)
m = -1
for i in range(1, 2 ** 64):
    if (pow(pub.g, i, pub.p) == tmp_m):
        m = i
        break


# In[13]:


shares = sharing.secret_int_to_points(priv.x, 2, 3)
print(sharing.points_to_secret_int(shares[0:2]))
print(sharing.points_to_secret_int(shares[0:3]))
print(sharing.points_to_secret_int(shares[0:1]))

