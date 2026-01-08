# EXPRESSWAY

Scansionando le porte tcp con nmap vediamo che è aperta solo la porta 22

![nmap -sVC 10.10.11.87](./images/1-porte_tcp.png)

Allora proviamo una scansione delle porte udp e vediamo la porta 500 aperta, questa porta usa il protocollo IKE per gestire l'autenticazione e lo scambio di chiavi nelle VPN IPsec

![nmap -sU -F -T4 10.10.11.87](./images/2porte_udp.png)

Facciamo una scansione aggressiva sul protocollo ike. Rivela un ID_USER_FQDN e un hash di 20 bytes, mettiamo l'hash in un file

![ike-scan -A 10.10.11.87](./images/3-ike_aggrssive.png)

Questo è l'hash della Pre-Shared Key (PSK) che usa un client vpn per collegarsi col server e si può craccare con psk-crack

![psk-crack hash.txt -d /usr/share/wordlists/rockyou.txt](./images/4-crack_hash.png)

Ora colleghiamoci a ssh con l'ID e l'hash craccato, otteniamo una shell come utente ike e possiamo prendere la user flag

![ssh ike@10.10.11.87](./images/5-user_flag.png)

Una volta dentro notiamo la versione di sudo. La funzione chroot() di questa versione è vulnerabile alla CVE-2025-32463, questa consiste nel caricare file di configurazione e shared libraries a discrezione dell'attaccante, portando ad ottenere i privilegi di root, cerchiamo questa versione con searchsploit e troviamo il file 52352.txt

![sudo --version](./images/6.1-sudo_version.png)

![searchsploit 1.9.17](./images/6.2-file_52352.png)

In fondo a questo file c'è l'exploit vero e proprio che possiamo copiare su un altro file (.sh), portarlo sul target e renderlo eseguibile

![](./images/7-exploit.png)

Una volta lanciato si ottiene la shell come utente root ed è possibile ottenere l'ultima flag

![./file.sh](./images/8-root_flag.png)
