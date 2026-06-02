# Barrier

Scansioniamo il target con nmap e troviamo 6 porte aperte, di cui 5 con http e una con ssh. Prima di partire col analizzarle, aggiungiamo al file /etc/host una riga con ip ed i nomi barrier.vl e GitLab.barrier.vl

![](./images/1-nmap.png)

Partiamo con la porta 8080 è quella di default di tomcat, per entrare nelle pagine /manager/html e host-manager/html servono delle credenziali

![](./images/2-8080.png)

Le porte 9000 e 9443 hostano Authentik, una piattaforma che gestisce autenticazioni e autorizzazioni in modo centralizzato, per entrare richiede prima un'email o uno username e poi una password

![](./images/3-authentik.png)

Quando proviamo a collegarci con la porta 80 veniamo reindirizzati sulla porta 443, questa porta hosta GitLab. Proviamo a registrarci e loggarci, ma dice che il nostro account deve essere sbloccato dall'administrator

![](./images/4-GitLab-registration.png)

In basso a sinistra c'è un link, explore, che ci porta ad un repository dell'utente satoru, questo repo contiene uno script python. Nell'oggetto auth_data vediamo lo username satoru e come password degli asterischi
![](./images/5-first-repo.png)

Controlliamo i vecchi commit di questo repository e troviamo la password in chiaro di questo utente

![](./images/6-satoru-psw.png)

Colleghiamoci a GitLab con le nuove credenziali, troviamo un altro utente e nella pagina di help possiamo vedere che GitLab è alla versione 17.3.2, ma del resto non c'è nient'altro

![](./images/7_1-akadmin.png)
![](./images/7_2-help.png)

Loggiamoci su Authentik con l'utente satoru, qui troviamo due applicazioni, GitLab che conoscevamo già, e Guacamole che serve per connettersi a desktop e server remoti direttamente dal browser, senza dover installare nulla, ma per l'utente satoru non ci sono connessioni

![](./images/8_1-authentik.png)
![](./images/8_2-guacamole.png)

Cerchiamo degli exploit e GitLab a questa versione con SAML SSO abilitato, nel nostro caso Authentik, è vulnerabile alla CVE-2024-45409. Questa riguarda la libreria ruby-saml che usa un XML per l'autenticazione ed è possibile manipolarlo per autenticarsi con qualsiasi utente, troviamo questo PoC su GitHub che trasforma un XML in una risposta già pronta da inviare

![](./images/9_1-cve.png)
![](./images/9_2-poc.png)

Da GitLab clicchiamo su 'Single Sign On', intercettiamo la comunicazione con Burpsuite, e quando vediamo in una richiesta 'SAMLResponse', copiamolo dentro cyberchef e decodifichiamolo prima URL, poi base64 ed infine facciamo una decompressione DEFLATE con Raw Inflate per ottenere il file XML in chiaro, salviamolo su un file e passiamolo allo script trovato prima su GitHub per ottenere la SAMLResponse da copiare su Burpsuite

![](./images/10_1-saml-resp.png)
![](./images/10_2-cyberchef.png)
![](./images/10_3-saml.png)

Lasciamo continuare il flusso di autenticazione e veniamo reindirizzati su GitLab come akadmin

![](./images/11-admin-gitlab.png)

Clicchiamo su 'admin' in basso a sinista e fra le varie funzionalità vediamo che c'è un runner che viene eseguito dentro un docker, se è in pausa bisogna attivarlo


![](./images/12_runner.png)

Creiamo un progetto con il file .gitlab-ci.yml, assegniamo il runner al progetto e triggeriamo la pipeline con un commit, provando diversi comandi, con env troviamo AUTHENTIK_TOKEN, il quale serve per poter interrogare le API di Authentik


![](./images/13_1-env.png)
![](./images/13_2-resp.png)

Cerchiamo altri utenti attraverso le API e oltre a akadmin e satoru troviamo l'utente maki ed un utente di servizio

![](./images/14_1-api.png)
![](./images/14_2-maki.png)

Grazie al token come super user e alla capabilities 'can_impersonate' di Authentik, possiamo impersonare l'utente maki, possiamo vedere le capabilieties nel head del html della pagina di Authentik

![](./images/15_1-cap-raw.png)
![](./images/15_2-cap-json.png)

Otteniamo il token di maki con una chiamata alle API e mettiamolo nei cookie, ricarichiamo la pagina e siamo riusciti ad impersonarlo

![](./images/16_1-token-curl.png)
![](./images/16_2-impersonation.png)

Andiamo dentro l'app Guacamole per vedere che c'è una connessione, sfruttiamola per usare il terminale su questa macchina e prendere la prima flag

![](./images/17_1-conn.png)
![](./images/17_2-flag.png)

Nella nostra home non c'è nulla e nelle home degl'altri utenti non possiamo entrarci, fra i file di configurazione, troviamo quelli di Guacamole in /etc/guacamole e troviamo il file guacamole.properties, il quale rivela delle credenziali per un db MySQL locale

![](./images/18-guac-prop.png)

Colleghiamoci a questo servizio e troviamo il db guac_db che contiene diverse tabelle, dandoci un'occhiata, dentro guacamole_connection_parameter troviamo la chiave privata ssh dell'utente maki_adm e la passphrase

![](./images/19_1-db.png)

![](./images/19_2-ssh-key.png)

Salviamo la chiave ssh in un file, cambiamogli i permessi e connettiamoci a ssh, ci chiederà anche la passphrase

![](./images/20_1-permission.png)

![](./images/20_2-ssh.png)

Una volta dentro come maki_adm, nella home, nel file .bash-history troviamo il comando per farci diventare super user e la password

![](./images/21-su.png)

Lanciamo sudo su, incolliamo la password trovata per diventare root, ora possiamo prendere l'ultima flag

![](./images/22-flag.png)