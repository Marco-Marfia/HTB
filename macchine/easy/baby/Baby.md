
# BABY

Associamo all'ip un nome host

![echo '10.129.12.219 baby.htb' | sudo tee -a /etc/hosts](./immagini/1-hostname.png)

Scansioniamo il target con nmap, dalla porta 389 scopriamo che la macchina è all'interno di un dominio AD, aggiungiamo al file /etc/hosts anche il dominio baby.vl

![nmap -sV -oN scan.nmap baby.htb ](./immagini/2-scan.png)

Possiamo interrogare ldap con ldapsearch, ottenendo diverse info relative al dominio, dando un'occhiata agli utenti vediamo che Teresa Bell nel campo descrizione ha scritto qual'era la sua password iniziale, provando smb, winrm e xfreerdp3 non funziona, ma essendo una password impostata inizialmente, potrebbero averla usata anche con altri utenti 

![ldapsearch -x -H ldap://baby.vl -b "DC=baby,DC=vl" > ldap.info](./immagini/3_1-ldap-command.png)
![](./immagini/3_2-ldap-info.png)

Mettiamo i nomi utente, sono quelli in sAMAccountName, dentro un file e proviamo un password spraying su smb e vediamo che l'utente Caroline.Robinson deve ancora cambiare la password

![](./immagini/4_1-users-list.png)
![netexec smb baby.vl --shares -u users.txt  -p 'BabyStart123!' --continue-on-success](./immagini/4_2-smb-spray.png)

Con smbpasswd possiamo cambiare la password e metterne una a nostro piacimento

![smbpasswd -r baby.htb -U baby.vl\\Caroline.Robinson](./immagini/5-change-psw.png)

Ora possiamo entrare con questo utente e la nostra nuova password con winrm e prendere la prima flag

![evil-winrm -i baby.vl -u Caroline.Robinson -p 'NewPass123!'](./immagini/6-user-flag.png)

Essendo una macchina a dominio vediamo se c'è qualche path per una privilege escalation su bloodhound, usiamo bloodhound-python per ottenere tutte le info, i file json, questo comando comunica col target tramite ldap, riceve i dati via rete e li salva direttamente sulla nostra macchina. 
Purtroppo, cercando su bloodhound non troviamo nulla di interessante

![bloodhound-python -u Caroline.Robinson -p 'NewPass123!' -d baby.vl -ns 10.129.12.219 -c All](./immagini/7-bloodhound-python.png)

Diamo un'occhiata ai privilegi del nostro utente, abbiamo SeBackupPrivilege che ci permette di leggere il contenuto di qualsiasi file, possiamo entrare nella home directory di administrator ma non possiamo leggere la root flag. 
Quello che potremmo fare è ottenere il file criptato ntds.dit (il database di AD) e la chiave per decriptarlo, dentro la hive HKLM\SYSTEM. In questo modo potremmo leggere gli hash delle password di tutti gli utenti

![whoami /priv](./immagini/9-caroline-priv.png)

Ora creiamoci una cartella temporanea dove lavorare

![mkdir C:\temp](./immagini/10-temp-dir.png)

Salviamoci la hive HKLM/SYSTEM, che contiene la Boot Key che serve per decifrare i segreti dentro ntds.dit, e scarichiamola sulla kali

![reg save HKLM\SYSTEM C:\temp\SYSTEM](./immagini/11-system-reg.png)

Non possiamo ottenere direttamente il file ntds.dit, pechè è un file sempre in uso, quindi dobbiamo fare una copia del disco, che possiamo fare perchè siamo nel gruppo Backup Operators, con diskshadow. Ci serve questo script che fa uno snapshot del disco e lo monta sul disco virtuale z:

![](./immagini/12_1-shadow-script.png)
![diskshadow /s shadow.txt](./immagini/12_2-diskshadow.png)

Per copiare il file ntds.dit abbiamo bisogno di robocopy in backup mode '/b', per raggirare i permessi, dopodichè scarichiamolo sulla nostra kali 

![robocopy /b z:\Windows\NTDS\ C:\temp ntds.dit](./immagini/13-copy-file.png)

Con impacket possiamo prendere i file SYSTEM e ntds.dit per ottenere, fra le altre cose, gli hash delle password degli utenti

![impacket-secretsdump -ntds ntds.dit -system SYSTEM LOCAL](./immagini/14-hashes.png)

Usiamo l'hash di administrator per entrare con evil-winrm e prendere l'ultima flag

![evil-winrm -i baby.htb -u Administrator -H ee4457ae59f1e3fbd764e33d9cef123d](./immagini/15-root-flag.png)