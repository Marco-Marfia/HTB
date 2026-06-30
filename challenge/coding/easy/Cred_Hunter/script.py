# take in the number
raws = int(input()) 
emails = []
psws = []
pairs = []

for r in range(1, raws + 1):
    str = input()
    if("@cygnus" in str):
        emails.append(str)
    else:
        psws.append(str)

# calculate answer
for email in emails:
    name = email.split("@")[0][:-1]
    for psw in psws:
        if(name in psw):
            pairs.append((email,psw))

sort_cred = sorted(pairs, key=lambda x: (x[0], x[1]))


# print answer
for mail, psw in sort_cred:
    print(mail + " " + psw)
