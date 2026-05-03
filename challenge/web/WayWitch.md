# Way Witch

Dal sito possiamo solo inviare dei ticket, niente di più
![web site](./images/1-web-page.png)

Nel codice sorgente, nel file database.js, viene creata una tabella, chiamata tickets, dove viene inserita la flag
![create database](./images/2-db-flag.png)

Nello stesso file c'è anche una funzione che prende tutte le righe di quella tabella
![get tickets](./images/3-get-tickets.png)

Quella funzione viene chiamata in un solo punto nel progetto, durante una richiesta GET all'endpoint /tickets. Il token viene passato alla funzione getUsernameFromToken() che ritorna il nostro username, che per poter ottenere la flag, deve essere admin

![http get](./images/4-endpoint.png)

la funzione getUsernameFromToken(), decodifica il token JWT e ritorna lo username, c'è anche scritta la chiave segreta
![get username](./images/5-get-username.png)

Intercettando con burpsuite la richiesta GET /tickets e mandandola al repeater si vede il payload del token dove c'è la prop username, cambiamola in admin
![change payload](./images/6-jwt.png)

Poi nella tab JWT Editor creaiamo una chiave simmetrica con il secret trovato nel codice, visto che il token viene codificato e decodificato con la stessa chiave, e salviamola. Ci servirà per firmare il nuovo token
![Create key](./images/7-key.png)

Ora nel repeater firmiamo il nuovo token cliccando su 'sign' ed inviamo la richiesta. In questo modo otteremo come risposta tutte le righe dentro la tabella tickets, compresa la flag
![](./images/8-flag.png)