COMMON = ['THE', 'AND', 'TO', 'HTB', 'FLAG', 'THAT', 'THIS', 'OF', 'IS', 'YOU', 'YOUR', 'WITH']

def julius_decrypt(ct, shift):
    pt = ''
    for c in ct:
        if 'A' <= c <= 'Z':
            pt += chr(65 + (ord(c) - 65 - shift) % 26)
        elif c == '0':
            pt += ' '
        else:
            pt += c
    return pt

def score(msg):
    return sum(msg.upper().count(word) for word in COMMON)

ct = open('output.txt').read()
results = []

for shift in range(26):
    msg = julius_decrypt(ct, shift)
    results.append((score(msg), msg))

results.sort(reverse=True)

print(results[0][1])