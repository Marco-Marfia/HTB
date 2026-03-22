# BLUE 

Associato nome host a ip in /etc/hosts

![echo "10.129.6.209 blue.htb | sudo tee /etc/hosts"](./immagini/1-hostname.png)

Con una scansione nmap notiamo che abbiamo a che fare con una macchina Windows 7 con RPC, netbios e SMB

![nmap -sVC blue.htb -oN scan.nmap](./immagini/2-nmap.png)

Cercando un exploit per Windows 7 Professional 7601 vediamo che potrebbe essere vulnerabile ad eternalblue

![Windows 7 Professional 7601 exploit](./immagini/3-google-exploit.png)

Cerchiamo su msfconsole un exploit per eternalblue per windows 7

![search eternalblue](./immagini/4-select-exploit.png)

Impostiamo gli hosts, remoto e locale

![](./immagini/5-set-options.png)

Lanciando l'exploit riusciamo ad ottenere una shell come system

![](./immagini/6-get-shell.png)

Nella cartella C:\Users\haris\Desktop troviamo la user flag

![](./immagini/7-user-flag.png)

Nella cartella C:\Users\Administrator\Desktop troviamo la root flag

![](./immagini/8-root-flag.png)