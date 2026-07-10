from pwn import *

HOST = "154.57.164.65"
PORT = 30725
PASS2 = "12345678"

def request(io, user):
    io.sendlineafter(b"Enter your secure access key: ", PASS2.encode())
    io.sendlineafter(b"Enter your Agent Codename: ", user.encode())
    io.recvuntil(b"Encrypted transmission: ")
    ciphertext = io.recvline().strip().decode()
    return bytes.fromhex(ciphertext)

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))



io = remote(HOST, PORT)

cipher_a = request(io, "A")
n = len(cipher_a)
filler = n - len(b"Agent ")
plaintext_b = b"Agent " + b"A" * filler 
cipher_b = request(io, "A" * filler)

keystream = xor(plaintext_b, cipher_b[:n])

plaintext_a = xor(keystream, cipher_a)
print(plaintext_a.decode())


io.close()

