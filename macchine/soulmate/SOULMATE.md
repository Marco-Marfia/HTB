# SOULMATE

Come prima cosa aggiungiamo il nome host al file /etc/hosts

![echo "10.10.11.86 soulmate.htb" | sudo tee -a /etc/hosts](./immagini/1-hostname.png)

Scansionando il target con nmap, troviamo le porte 22 con ssh e 80 con http

![nmap -sVC soulmate.htb](./immagini/2-nmap.png)

Sulla porta 80 c'è un sito dove è possibile iscriversi e modificare i propri dati, ma nulla di interessante

![http://soulmate.htb](./immagini/3-sito.png)

Enumerando i sottodomini troviamo ftp.soulamte.htb, aggiungiamolo al riga già creata dentro /etc/hosts. Per l'enumerazione è necessario usare l'opzione --append-domain, poichè il server web accetta solo richieste con il nome di dominio completo (FQDN)

![gobuster vhost --append-domain -u http://soulmate.htb -w /usr/share/wordlist/Seclist-master/Discovery/DNS/subdomains-top1million-5000.txt](./immagini/4-sottodominio.png)

Andiamo sul sito e troviamo l'applicazione CrushFTP, il quale è un server per il trasferimento dati dove si possono gestire anche gli utenti, direttamente da interfaccia web. Nel codice HTML notiamo una versione scritta più volte: 11.W.657

![http://ftp.soulmate.htb](./immagini/5-sito_ftp.png)

Cerchiamo con searchsploit delle vulnerabilità e troviamo un Authentication Bypass scritto in python. Questo sfrutta una race condition nel metodo di autenticazione per creare un utente admin (CVE-2025-31161)

![searchsploit crushftp](./immagini/6-searchsploit.png)

Copiamolo in una nostra cartella e lanciamolo sull'applicazione CrushFTP, dopo qualche tentativo riusciamo a creare un nostro utente

![python3 52295.py --port 80 --target ftp.soulmate.htb --exploit --new-user <username> --password <password>](./immagini/7-exploit.png)

Riusciamo ad entrare e andando nella pagina admin, poi user manager, l'utente ben vede la cartella del sito (webProd), copiamola e aggiungiamola al nostro utente poi salviamo

![login con utente creato](./immagini/8.0-crushftp1.png)
![file di utente ben](./immagini/8.1-crushftp2.png)
![file di utente creato](./immagini/8.2crushftp3.png)

Ora possiamo creare una reverse shell in php e caricarla nella cartella webProd

![https://www.revshells.com/](./immagini/9.0-rev_shell.png)
![upload file](./immagini/9.1-upload_shell.png)

Apriamo la porta con netcat sulla nostra macchina e cerchiamo la reverse shell nel browser, otteremo una shell come www-data

![nc -lnvp <porta>](./immagini/10.png)

Osserviamo le socket aperte e notiamo che sulla porta 2222 c'è un server SSH scritto in Erlang

![ss -lntp - nc 127.0.0.1 2222](./immagini/11-socket.png)

Cerchiamo le directory di Erlang e vediamo se c'è scritto qualcosa che ci può servire

![find / type d -name erlang 2>/dev/null](./immagini/12-erlang_dir.png)

Troviamo le credenziali dell'utente ben dentro il file /usr/local/lib/erlang_login/start.escript

![ben:HouseH0ldings998](./immagini/13-ben_cred.png)

Ci colleghiamo al target con ssh e le credenziali di ben e otteniamo la flag

![/home/ben/user.txt](./immagini/14-ben_flag.png)

Ci colleghiamo al servizio Erlang sulla porta 2222 con le credenziali di ben e otteniamo una shell Erlang come root

![ssh ben@127.0.0.1 -p 2222](./immagini/15-erlang_shell.png)

Per i comandi Erlang  rimando al sito ufficiale: https://www.erlang.org/docs/21/man/os#cmd-1

Ora possiamo prendere la flag di root

![os:cmd("ls /root/root.txt")](./immagini/16-root_flag.png)